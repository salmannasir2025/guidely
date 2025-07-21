from fastapi import APIRouter, Request, Depends

from .. import database
from ..limiter import default_rate_limit, limiter
from ..schemas.core import FeedbackRequest, HistoryResponse
from ..auth import get_current_active_user, User

router = APIRouter(
    prefix="/data",
    tags=["User Data"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/history", response_model=HistoryResponse)
@limiter.limit(default_rate_limit)
async def get_history(request: Request, current_user: User = Depends(get_current_active_user)):
    history_data = await database.get_user_history(current_user.email)
    return HistoryResponse(history=history_data)


@router.delete("/history", status_code=204)
@limiter.limit("5/minute")
async def clear_history(request: Request, current_user: User = Depends(get_current_active_user)):
    await database.delete_user_history(current_user.email)
    return


@router.post("/feedback", status_code=201)
@limiter.limit(default_rate_limit)
async def submit_feedback(request: Request, body: FeedbackRequest, current_user: User = Depends(get_current_active_user)):
    body.user_id = current_user.email  # Override user_id with authenticated user's email
    await database.log_feedback(body)
    return {"message": "Feedback received"}
