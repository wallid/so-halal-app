import logging
from src.models.product import BarcodeScanRequest, HalalStatusResponse, UploadProductImagesRequest
from src.models.enums import HalalStatus
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from src.db.redis import redis_client
from src.db.postgres import get_postgres_cursor
from src.services.halal_verification import verify_halal
from typing import List
import os
import requests
import base64

import openfoodfacts

# Set up the logger
logger = logging.getLogger(__name__)

router = APIRouter()
api = openfoodfacts.API(user_agent="sohalal/0.1 support@sohalal.ai", country="au", environment="org")


def is_information_sufficient(product_info: dict) -> bool:
    """
    Determines if the product information contains enough data to assess Halal status.
    The check relies solely on specific 'completed' states in the 'states' field.
    """
    # Get the 'states' field as a string
    states = product_info.get('states', '')

    # Check if any required states indicate completion
    required_states_completed = any(
        state in states for state in [
            "en:product-name-completed", 
            "en:ingredients-completed", 
            "en:categories-completed"
        ]
    )

    return required_states_completed



# src/api/routes.py
@router.post("/scan", response_model=HalalStatusResponse)
def scan_barcode(request: BarcodeScanRequest, cursor=Depends(get_postgres_cursor)):
    logger.info(f"Received barcode scan request for {request.barcode}")

    # 1. Check Redis cache
    product_data = redis_client.get(request.barcode)
    if product_data:
        product = eval(product_data)
        return HalalStatusResponse(
            barcode=request.barcode,
            brands=product.get('brands', ""),
            product_name=product['product_name'],
            status=HalalStatus(product['status']),
            reasons=product.get('reasons', []),
            source="internal"
        )

    # 2. Check PostgreSQL
    cursor.execute("SELECT product_name, status, reasons FROM products WHERE barcode = %s", (request.barcode,))
    product = cursor.fetchone()
    if product:
        redis_client.set(request.barcode, str(product))
        return HalalStatusResponse(
            barcode=request.barcode,
            product_name=product['product_name'],
            status=HalalStatus(product['status']),
            reasons=product['reasons'],
            source="internal"
        )

    # 3. Query OpenFoodFacts
    product_data = api.product.get(request.barcode, fields=["states","code", "product_name", "ingredients_text", "_keywords", "brands"])

    if product_data and not is_information_sufficient(product_data):
        return HalalStatusResponse(
            barcode=request.barcode,
            product_name=product_data.get('product_name'),
            status=HalalStatus.NOT_ENOUGH_INFORMATION,
            reasons=["Insufficient information in OpenFoodFacts data"],
            source="openfoodfacts"
        )

    if product_data and 'product_name' in product_data:
        product_info = product_data
        product_name = product_data.get('product_name', 'Unknown Product')
        product_brands = product_data.get('brands', 'Unknown Brand')

        # Perform Halal verification
        halal_verification = verify_halal(product_info)
        status = halal_verification['status']
        reasons = halal_verification['reasons']

        # Store in PostgreSQL
        cursor.execute(
            """
            INSERT INTO products (barcode, product_name, status, reasons)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (barcode) DO NOTHING
            """,
            (request.barcode, product_name, status, reasons)
        )

        # Cache in Redis
        redis_client.set(request.barcode, str({
            "product_name": product_name,
            "status": status.value,
            "reasons": reasons,
            "brands": product_brands,

        }))

        return HalalStatusResponse(
            barcode=request.barcode,
            product_name=product_name,
            brands=product_brands,
            status=status,
            reasons=reasons,
            source="openfoodfacts"
        )

    raise HTTPException(status_code=404, detail="Product not found")



@router.put("/product", response_model=dict)
async def create_update_product(
    barcode: str,
    product_front_image: UploadFile = File(...),
    product_ingredients_image: UploadFile = File(...),
):
    try:
        logger.info(f"Starting the creation/update process for product with barcode: {barcode}")
        
        # Create the product
        data = {'code': barcode}
        logger.info("Sending product creation request.")
        response = api.product.update(data)
        
        if response.status_code != 200:
            logger.error(f"Error creating product. Status code: {response.status_code}")
            raise HTTPException(status_code=400, detail="Error creating product")
        
        # Upload the product front image
        logger.info("Uploading product front image.")
        response = upload_product_image(barcode, product_front_image, image_field=IMAGE_FIELDS.FRONT_EN)
        
        # Upload the product ingredients image
        logger.info("Uploading product ingredients image.")
        response = upload_product_image(barcode, product_ingredients_image, image_field=IMAGE_FIELDS.INGREDIENTS_EN)
        
        # Perform OCR on the ingredients image
        logger.info("Performing OCR on product ingredients image.")
        response = get_product_ingredients_ocr(barcode, 1, image_field=IMAGE_FIELDS.INGREDIENTS_EN, ocr_engine=OCR_ENGINES.GOOGLE_CLOUD_VISION)
        
        # Update the product with ingredients text
        logger.info("Updating product with OCR results.")
        data = {
            'code': barcode,
            'ingredients_text': response['ingredients_text_from_image'],
        }
        response = api.product.update(data)
        
        if response.status_code != 200:
            logger.error(f"Error updating product with ingredients text. Status code: {response.status_code}")
            raise HTTPException(status_code=400, detail="Error creating product")
        
        logger.info(f"Product creation/update process completed for barcode: {barcode}")
        
        return {"detail": "Product updated successfully"}
    except Exception as e:
        logger.exception(f"An error occurred during the product creation/update process for barcode: {barcode}")
        raise HTTPException(status_code=500, detail=str(e))

# Image field constants
class IMAGE_FIELDS:
    FRONT_EN = "front_en"
    INGREDIENTS_EN = "ingredients_en"
    NUTRITION_EN = "nutrition_en"
    PACKAGING_EN = "packaging_en"
    OTHER = "other"

class OCR_ENGINES:
    GOOGLE_CLOUD_VISION = "google_cloud_vision"
    TESSERACT = "tesseract"

def get_product_ingredients_ocr(barcode: str, image_id: int, image_field: str = IMAGE_FIELDS.INGREDIENTS_EN, ocr_engine: str = OCR_ENGINES.GOOGLE_CLOUD_VISION):
    logger.info(f"Performing OCR for barcode: {barcode}, image field: {image_field}")
    url = "https://world.openfoodfacts.org/cgi/ingredients.pl"
    params = {
        "id": image_field,
        "code": barcode,
        "process_image": image_id,
        "ocr_engine": ocr_engine,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200 or response.json().get('status') == 1:
        logger.error(f"Error performing OCR. Status code: {response.status_code}, Response: {response.text}")
        raise HTTPException(status_code=400, detail="Error performing OCR on image")
    
    logger.info("OCR process completed successfully.")
    return response.json()

def upload_product_image(barcode: str, file: UploadFile, image_field: str = IMAGE_FIELDS.FRONT_EN):
    logger.info(f"Uploading image for barcode: {barcode}, image field: {image_field}")
    url = "https://world.openfoodfacts.org/cgi/product_image_upload.pl"
    file_content = file.file.read()
    files = {
        f"imgupload_{image_field}": (file.filename, file_content, file.content_type),
    }
    data = {
        "code": barcode,
        "imagefield": image_field,
    }

    response = requests.post(url, data=data, files=files)
    if response.status_code != 200:
        logger.error(f"Error uploading image. Status code: {response.status_code}, Response: {response.text}")
        raise HTTPException(status_code=400, detail="Error uploading image")
    
    logger.info("Image uploaded successfully.")
    return response.json()
