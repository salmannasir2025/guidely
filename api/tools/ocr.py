import logging
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from google.cloud import vision
from .base import BaseTool

class OCRTool(BaseTool):
    """Tool for extracting text from images via Google Vision."""

    def __init__(self):
        try:
            self._client = vision.ImageAnnotatorClient()
        except Exception as e:
            logging.error(f"Failed to initialize Google Vision client: {e}")
            self._client = None

    def get_name(self) -> str:
        return "ocr"

    def get_description(self) -> str:
        return "Extracts text from image files using Google Cloud Vision."

    async def execute(self, file: UploadFile = None, **kwargs) -> str:
        if not self._client:
            raise Exception("Google Vision client not initialized")
        if not file:
            return ""
            
        try:
            content = await file.read()
            image = vision.Image(content=content)
            response = await run_in_threadpool(self._client.text_detection, image=image)
            
            if response.error.message:
                raise Exception(f"Vision API Error: {response.error.message}")
                
            return (
                response.text_annotations[0].description
                if response.text_annotations
                else ""
            )
        except Exception as e:
            logging.error(f"OCRTool Error: {e}")
            return ""
