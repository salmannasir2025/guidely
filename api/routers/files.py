import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import uuid
from datetime import datetime, timezone

from .. import database, ocr, config
from ..auth import get_current_active_user, User
from ..schemas.files import FileResponse

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    dependencies=[Depends(get_current_active_user)]
)

@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_active_user)):
    """Upload a file and store it in the database."""
    try:
        # Generate a unique ID for the file
        file_id = str(uuid.uuid4())
        
        # Create file metadata
        file_data = {
            "id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": 0,  # Will be updated after reading the file
            "user_id": current_user.email,
            "upload_date": datetime.now(timezone.utc),
            "is_processed": False
        }
        
        # Read the file content
        content = await file.read()
        file_size = len(content)
        
        # Validation: File size
        if file_size > config.settings.file_upload_max_size:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Max size is {config.settings.file_upload_max_size / 1024 / 1024}MB"
            )
            
        # Validation: Content Type
        if file.content_type not in config.settings.allowed_file_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file.content_type} not allowed. Supported types: {', '.join(config.settings.allowed_file_types)}"
            )
            
        file_data["size"] = file_size
        
        # Save file metadata and content to database
        db_file_id = await database.save_file_metadata(file_data, content=content)
        if not db_file_id:
            raise HTTPException(status_code=500, detail="Failed to save file metadata")
        
        # Process the file with OCR if it's an image
        if file.content_type.startswith("image/"):
            try:
                # Use the content bytes for OCR if possible, or reset position
                # Since we already have content in memory, we can use it.
                # However, extract_text_from_image expects an UploadFile.
                # Let's seek(0) as it is in the original code.
                await file.seek(0)
                ocr_text = await ocr.extract_text_from_image(file)
                await database.update_file_ocr_text(db_file_id, ocr_text)
                file_data["ocr_text"] = ocr_text
                file_data["is_processed"] = True
            except ocr.OCRError as e:
                logging.error(f"OCR processing error: {e}")
                # We continue even if OCR fails, as the file is still uploaded
        
        return FileResponse(
            id=file_id,
            filename=file.filename,
            upload_date=file_data["upload_date"],
            is_processed=file_data["is_processed"]
        )
    except Exception as e:
        logging.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.get("/", response_model=List[FileResponse])
async def get_user_files(current_user: User = Depends(get_current_active_user)):
    """Get all files uploaded by the current user."""
    files = await database.get_user_files(current_user.email)
    return [
        FileResponse(
            id=str(file["_id"]),
            filename=file["filename"],
            upload_date=file["upload_date"],
            is_processed=file["is_processed"]
        ) for file in files
    ]

@router.get("/{file_id}")
async def get_file(file_id: str, current_user: User = Depends(get_current_active_user)):
    """Get a specific file by ID."""
    file = await database.get_file_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if the file belongs to the current user
    if file["user_id"] != current_user.email:
        raise HTTPException(status_code=403, detail="Not authorized to access this file")
    
    return {
        "id": str(file["_id"]),
        "filename": file["filename"],
        "content_type": file["content_type"],
        "size": file["size"],
        "upload_date": file["upload_date"],
        "is_processed": file["is_processed"],
        "ocr_text": file.get("ocr_text")
    }