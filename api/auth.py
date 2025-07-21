from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .database import user_collection
from .config import settings
from .schemas.auth import User, UserCreate, TokenData

# Password hashing context using Argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# OAuth2 scheme for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

async def get_user(email: str) -> Optional[dict]:
    """Get user from database."""
    if user_collection:
        if user_dict := await user_collection.find_one({"email": email}):
            return user_dict
    return None

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user."""
    if user_dict := await get_user(email):
        if verify_password(password, user_dict["hashed_password"]):
            return User(
                email=user_dict["email"],
                full_name=user_dict.get("full_name"),
                is_active=user_dict.get("is_active", True)
            )
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    if user_dict := await get_user(token_data.email):
        return User(
            email=user_dict["email"],
            full_name=user_dict.get("full_name"),
            is_active=user_dict.get("is_active", True)
        )
    raise credentials_exception

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def create_user(user: UserCreate) -> User:
    """Create a new user."""
    # Check if user already exists
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_doc = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
        "is_active": True
    }
    
    # Insert into database
    if user_collection:
        await user_collection.insert_one(user_doc)
    else:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    return User(**user_doc)