from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Dict, List
from ..auth import get_current_active_user
from ..schemas.auth import User
from ..database import user_collection
from ..utils.vault import vault
import logging

router = APIRouter(
    prefix="/users/me/keys",
    tags=["user keys"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_api_key(
    provider: str = Body(..., embed=True),
    key: str = Body(..., embed=True),
    current_user: User = Depends(get_current_active_user)
):
    """
    Encrypt and store a third-party API key for the user.
    """
    valid_providers = ["openai", "gemini", "anthropic", "deepseek"]
    if provider.lower() not in valid_providers:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not supported.")

    try:
        # Encrypt the key with user binding
        encrypted_key = vault.encrypt_api_key(key, str(current_user.id))
        
        # Update user document
        await user_collection.update_one(
            {"email": current_user.email},
            {"$set": {f"api_keys.{provider.lower()}": encrypted_key}}
        )
        
        return {"message": f"API key for {provider} successfully saved."}
    except Exception as e:
        logging.error(f"Error saving API key: {e}")
        raise HTTPException(status_code=500, detail="Failed to save API key.")

@router.get("/")
async def list_api_keys(current_user: User = Depends(get_current_active_user)):
    """
    List providers for which the user has stored keys (names only).
    """
    keys = current_user.api_keys or {}
    return {"providers": list(keys.keys())}

@router.delete("/{provider}")
async def delete_api_key(
    provider: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove a stored API key.
    """
    if not current_user.api_keys or provider.lower() not in current_user.api_keys:
        raise HTTPException(status_code=404, detail="Key not found.")

    await user_collection.update_one(
        {"email": current_user.email},
        {"$unset": {f"api_keys.{provider.lower()}": ""}}
    )
    
    return {"message": f"API key for {provider} removed."}
