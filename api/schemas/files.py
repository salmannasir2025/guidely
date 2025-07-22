from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FileUpload(BaseModel):
    """Schema for file uploads."""
    id: str
    filename: str
    content_type: str
    size: int
    user_id: str
    upload_date: datetime
    ocr_text: Optional[str] = None
    is_processed: bool = False


class FileResponse(BaseModel):
    """Schema for file response."""
    id: str
    filename: str
    upload_date: datetime
    is_processed: bool