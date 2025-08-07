from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import secrets

from ..auth import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_user,
    get_password_hash
)
from ..config import settings
from ..database import user_collection
from ..schemas import AskRequest, AskResponse
from ..schemas.auth import Token, UserCreate, User, PasswordResetRequest, PasswordReset

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    """Register a new user."""
    return await create_user(user)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get access token using username (email) and password."""
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

# Add these imports
from ..schemas.auth import PasswordResetRequest, PasswordReset
import secrets
from datetime import datetime, timedelta

# Add these endpoints
@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest):
    """Send a password reset link to the user's email."""
    user = await get_user(request.email)
    if not user:
        # Don't reveal that the email doesn't exist
        return {"message": "If your email is registered, you will receive a password reset link."}
    
    # Generate a secure token
    reset_token = secrets.token_urlsafe(32)
    
    # Store the token in the database with an expiration time
    expiration = datetime.utcnow() + timedelta(hours=1)
    await user_collection.update_one(
        {"email": request.email},
        {"$set": {"reset_token": reset_token, "reset_token_expires": expiration}}
    )
    
    # In a real application, you would send an email with the reset link
    # For this example, we'll just return the token
    return {
        "message": "If your email is registered, you will receive a password reset link.",
        "debug_token": reset_token  # Remove this in production
    }

@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset):
    """Reset a user's password using a reset token."""
    # Find the user with the given token
    user = await user_collection.find_one({
        "reset_token": reset_data.token,
        "reset_token_expires": {"$gt": datetime.utcnow()}
    })
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Update the password and remove the reset token
    hashed_password = get_password_hash(reset_data.new_password)
    await user_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"hashed_password": hashed_password},
            "$unset": {"reset_token": "", "reset_token_expires": ""}
        }
    )
    
    return {"message": "Password has been reset successfully"}