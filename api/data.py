from fastapi import APIRouter, Request

from .. import database
from ..limiter import default_rate_limit, limiter
from ..schemas import FeedbackRequest, HistoryResponse

router = APIRouter()


@router.get("/history/{user_id}", response_model=HistoryResponse, tags=["User Data"])
@limiter.limit(default_rate_limit)
async def get_history(request: Request, user_id: str):
    history_data = await database.get_user_history(user_id)
    return HistoryResponse(history=history_data)


@router.delete("/history/{user_id}", status_code=204, tags=["User Data"])
@limiter.limit("5/minute")
async def clear_history(request: Request, user_id: str):
    await database.delete_user_history(user_id)
    return


@router.post("/feedback", status_code=201, tags=["User Data"])
@limiter.limit(default_rate_limit)
async def submit_feedback(request: Request, body: FeedbackRequest):
    await database.log_feedback(body)
    return {"message": "Feedback received"}