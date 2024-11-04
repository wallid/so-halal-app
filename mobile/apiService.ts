import { Platform } from 'react-native';

export enum HalalStatus {
  HALAL = 'halal',
  NOT_HALAL = 'not_halal',
  HALAL_GIVEN_INGREDIENTS = 'halal_given_ingredients',
  NOT_ENOUGH_INFORMATION = 'not_enough_information',
  UNKNOWN = 'unknown',
}

export interface ProductData {
  barcode: string;
  product_name: string;
  brands: string;
  ingredients_text: string | null;
  status: HalalStatus;
  reasons?: string[]; // Optional reasons why the product has a certain halal status
  haram_items_found?: string[]; // Any haram items found, if applicable
}

export interface ApiResponse {
  barcode: string;
  product_name: string;
  brands?: string;
  status: HalalStatus;
  reasons?: string[]; // Optional error or status message
  haram_items_found?: string[];
}

// Replace with your local FastAPI URL
const LOCAL_API_URL = 'http://192.168.0.39:8000/api/v1/barcode/scan';
const UPLOAD_IMAGES_ENDPOINT_URL = 'http://192.168.0.39:8000/api/v1/barcode/upload-images';

export const fetchProductData = async (barcode: string): Promise<ProductData | null> => {
  try {
    // Call the local FastAPI endpoint
    const response = await fetch(`${LOCAL_API_URL}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ barcode }), // Send the barcode in the request body
    });

    if (!response.ok) {
      console.error('Failed to fetch product data:', response.statusText);
      return null;
    }

    const data: ApiResponse = await response.json();

    // Assuming the FastAPI server returns status 200 and valid product data
    return {
      barcode: data.barcode || barcode,
      product_name: data.product_name || 'Unknown product',
      brands: data.brands || 'Unknown brand',
      ingredients_text: null, // Adjust this if your FastAPI includes ingredients
      status: data.status || HalalStatus.UNKNOWN, // Use the halal status enum
      reasons: data.reasons || [], // Reasons for the specific halal status
      haram_items_found: data.haram_items_found || [], // Haram items, if any
    };
  } catch (error) {
    console.error('Error fetching product data:', error);
    return null;
  }
};

export const uploadProductImages = async (
  barcode: string,
  images: any[]
): Promise<boolean> => {
  try {
    const formData = new FormData();

    images.forEach((image, index) => {
      const uri = image.uri;
      const uriParts = uri.split('.');
      const fileType = uriParts[uriParts.length - 1];

      formData.append('files', {
        uri: Platform.OS === 'android' ? uri : uri.replace('file://', ''),
        name: `image_${index}.${fileType}`,
        type: `image/${fileType}`,
      } as any);
    });

    const response = await fetch(
      `${UPLOAD_IMAGES_ENDPOINT_URL}?barcode=${encodeURIComponent(barcode)}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      }
    );

    if (!response.ok) {
      console.error('Failed to upload images:', response.statusText);
      return false;
    }

    const data = await response.json();
    console.log('Upload response:', data);
    return true;
  } catch (error) {
    console.error('Error uploading images:', error);
    return false;
  }
};
