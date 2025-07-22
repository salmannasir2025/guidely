import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

import motor.motor_asyncio
from .config import settings
from .schemas import AskRequest, AskResponse, FeedbackRequest, HistoryItem

client: motor.motor_asyncio.AsyncIOMotorClient = None
db = None
interaction_collection = None
feedback_collection = None
user_collection = None
file_collection = None


async def initialize_database():
    """Initializes the database connection and collections."""
    global client, db, interaction_collection, feedback_collection, user_collection, file_collection
    try:
        logging.info("Initializing database connection...")
        client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongo_connection_string
        )
        db = client[settings.mongo_db_name]
        interaction_collection = db.get_collection(
            settings.mongo_interactions_collection
        )
        feedback_collection = db.get_collection(settings.mongo_feedback_collection)
        user_collection = db.get_collection(settings.mongo_users_collection)
        file_collection = db.get_collection("files")
        
        # Create unique index on email field for users collection
        if user_collection:
            await user_collection.create_index("email", unique=True)
        
        # Create compound index for user history queries for performance
        if interaction_collection:
            await interaction_collection.create_index(
                [("user_id", 1), ("timestamp", -1)]
            )
            
        # Create index for file uploads
        if file_collection:
            await file_collection.create_index("user_id")
            
        logging.info("Database connection initialized successfully.")
    except Exception as e:
        logging.error(
            "Failed to initialize database connection.", extra={"error": str(e)}
        )


async def log_interaction(
    user_id: str, request: AskRequest, response: AskResponse
):
    """Logs a user query and the system's response to the database."""
    if not interaction_collection:
        logging.warning("Database not available. Skipping interaction log.")
        return

    log_document = {
        "user_id": user_id,
        "mode": request.mode,
        "query": request.query,
        "language_code": request.language_code,
        "answer": response.answer,
        "source": response.source,
        "timestamp": datetime.now(timezone.utc),
    }
    try:
        await interaction_collection.insert_one(log_document)
    except Exception as e:
        logging.error(
            "Failed to log interaction.",
            extra={"user_id": user_id, "query": request.query, "error": str(e)},
        )


async def get_user_history(user_id: str) -> List[HistoryItem]:
    """Retrieves the last 10 interactions for a given user."""
    if not interaction_collection:
        logging.warning("Database not available. Cannot retrieve history.")
        return []

    try:
        # Find documents for the user, sort by most recent, and limit to 10
        cursor = (
            interaction_collection.find({"user_id": user_id})
            .sort("timestamp", -1)
            .limit(10)
        )

        history_docs = await cursor.to_list(length=10)
        return [HistoryItem(**doc) for doc in history_docs]
    except Exception as e:
        logging.error(
            "Failed to retrieve user history.",
            extra={"user_id": user_id, "error": str(e)},
        )
        return []


async def delete_user_history(user_id: str) -> int:
    """Deletes all interactions for a given user and returns the count of deleted documents."""
    if not interaction_collection:
        logging.warning("Database not available. Cannot delete history.")
        return 0

    try:
        result = await interaction_collection.delete_many({"user_id": user_id})
        deleted_count = result.deleted_count
        logging.info(
            "User history deleted successfully.",
            extra={"user_id": user_id, "deleted_count": deleted_count},
        )
        return deleted_count
    except Exception as e:
        logging.error(
            "Failed to delete user history.",
            extra={"user_id": user_id, "error": str(e)},
        )
        return 0


async def check_db_connection() -> bool:
    """Checks if the database client can connect to the server."""
    if not client:
        return False
    try:
        # The 'hello' command is the modern, lightweight way to check connection status.
        await client.admin.command("hello")
        return True
    except Exception:
        return False


async def log_feedback(request: FeedbackRequest) -> None:
    """Logs user feedback to the database."""
    if not feedback_collection:
        logging.warning("Database not available. Skipping feedback log.")
        return

    log_document = {
        "user_id": request.user_id,
        "query": request.query,
        "answer": request.answer,
        "feedback_type": request.feedback_type,
        "timestamp": datetime.now(timezone.utc),
    }
    try:
        await feedback_collection.insert_one(log_document)
        logging.info(
            "Feedback logged successfully.",
            extra={"user_id": request.user_id, "feedback": request.feedback_type},
        )
    except Exception as e:
        logging.error(
            "Failed to log feedback.",
            extra={"user_id": request.user_id, "error": str(e)},
        )


# Add these functions for file management
async def save_file_metadata(file_data: dict) -> str:
    """Saves file metadata to the database and returns the file ID."""
    if not file_collection:
        logging.warning("Database not available. Cannot save file metadata.")
        return None
        
    try:
        result = await file_collection.insert_one(file_data)
        return str(result.inserted_id)
    except Exception as e:
        logging.error(
            "Failed to save file metadata.",
            extra={"user_id": file_data["user_id"], "error": str(e)}
        )
        return None

async def get_user_files(user_id: str):
    """Retrieves all files uploaded by a user."""
    if not file_collection:
        logging.warning("Database not available. Cannot retrieve files.")
        return []
        
    try:
        cursor = file_collection.find({"user_id": user_id})
        files = await cursor.to_list(length=100)
        return files
    except Exception as e:
        logging.error(
            "Failed to retrieve user files.",
            extra={"user_id": user_id, "error": str(e)}
        )
        return []

async def get_file_by_id(file_id: str):
    """Retrieves a file by its ID."""
    if not file_collection:
        logging.warning("Database not available. Cannot retrieve file.")
        return None
        
    try:
        from bson import ObjectId
        file = await file_collection.find_one({"_id": ObjectId(file_id)})
        return file
    except Exception as e:
        logging.error(
            "Failed to retrieve file.",
            extra={"file_id": file_id, "error": str(e)}
        )
        return None

async def update_file_ocr_text(file_id: str, ocr_text: str):
    """Updates the OCR text for a file."""
    if not file_collection:
        logging.warning("Database not available. Cannot update file.")
        return False
        
    try:
        from bson import ObjectId
        result = await file_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": {"ocr_text": ocr_text, "is_processed": True}}
        )
        return result.modified_count > 0
    except Exception as e:
        logging.error(
            "Failed to update file OCR text.",
            extra={"file_id": file_id, "error": str(e)}
        )
        return False
