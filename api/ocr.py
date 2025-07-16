import logging
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from google.cloud import vision

client: vision.ImageAnnotatorClient = None

def initialize_ocr_client():
    """Initializes the Google Cloud Vision client."""
    global client
    try:
        client = vision.ImageAnnotatorClient()
    except Exception as e:
        logging.error(f"Failed to initialize Google Vision client: {e}")

class OCRError(Exception):
    """Custom exception for errors during the OCR process."""
    pass

async def extract_text_from_image(file: UploadFile) -> str:
    """
    Extracts text from an image file using the Google Cloud Vision API.
    Returns the extracted text as a string. Returns an empty string if no text is found.
    """
    if not client:
        logging.error("Google Vision client is not available.")
        raise OCRError("Google Vision client is not initialized.")

    try:
        # Asynchronously read the file content from the UploadFile object
        content = await file.read()

        # Construct the image object for the Vision API
        image = vision.Image(content=content)

        # Perform text detection in a thread pool to avoid blocking the event loop.
        response = await run_in_threadpool(client.text_detection, image=image)

        if response.error.message:
            logging.error(f"Google Vision API error: {response.error.message}")
            raise OCRError(f"Google Vision API returned an error: {response.error.message}")

        # The first annotation is typically the full detected text block.
        return response.text_annotations[0].description if response.text_annotations else ""

    except Exception as e:
        logging.error(f"An error occurred during OCR processing for file '{file.filename}': {e}")
        raise OCRError(f"An unexpected error occurred during OCR processing: {e}")

def check_vision_client() -> bool:
    """Checks if the Vision API client is initialized."""
    return client is not None