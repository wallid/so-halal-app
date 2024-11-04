from pydantic import BaseModel
from typing import List, Optional
from src.models.enums import HalalStatus

class BarcodeScanRequest(BaseModel):
    barcode: str

class HalalStatusResponse(BaseModel):
    barcode: str
    product_name: str
    brands: str = ""
    is_halal: bool
    source: str
    reasons: list[str] = []
# src/models/product.py
from pydantic import BaseModel
from typing import List, Optional
from src.models.enums import HalalStatus

class HalalStatusResponse(BaseModel):
    barcode: str
    product_name: Optional[str] = None
    brands: Optional[str] = None
    status: HalalStatus
    reasons: List[str]
    source: str


class UploadProductImagesRequest(BaseModel):
    barcode: str
    file: List[bytes]

