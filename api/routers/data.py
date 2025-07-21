from fastapi import APIRouter, Depends, HTTPException
from typing import List

from .. import database
from ..auth import get_current_active_user, User
from ..schemas import HistoryItem, HistoryResponse, FeedbackRequest

router = APIRouter(
    prefix="/data",
    tags=["Data"],
    dependencies=[Depends(get_current_active_user)]
)

@router.get("/history", response_model=HistoryResponse)
async def get_history(current_user: User = Depends(get_current_active_user)):
    """
    Retrieves the last 10 interactions for the currently authenticated user.
    """
    history_items = await database.get_user_history(current_user.email)
    return HistoryResponse(history=history_items)

@router.delete("/history")
async def delete_history(current_user: User = Depends(get_current_active_user)):
    """
    Deletes all interaction history for the currently authenticated user.
    """
    deleted_count = await database.delete_user_history(current_user.email)
    if deleted_count > 0:
        return {"message": f"Successfully deleted {deleted_count} history items."}
    else:
        return {"message": "No history found to delete."}

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest, current_user: User = Depends(get_current_active_user)):
    """
    Logs user feedback (up-vote or down-vote) for a specific query-answer pair.
    """
    # Ensure the feedback is being submitted for the logged-in user
    if request.user_id != current_user.email:
        raise HTTPException(status_code=403, detail="Cannot submit feedback for another user.")
    
    await database.log_feedback(request)
    return {"message": "Feedback submitted successfully."}