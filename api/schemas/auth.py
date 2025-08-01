from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    """Enumeration for user roles."""
    REGISTERED = "registered"
    ADMIN = "admin"


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for data stored in the JWT token payload."""
    email: Optional[str] = None


class UserBase(BaseModel):
    """Base schema for user properties."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration, includes password."""
    password: str = Field(..., min_length=8, description="User password")


class User(UserBase):
    """
    Schema for user information returned by the API.
    Does not include sensitive information like the password.
    """
    id: int
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class PasswordResetRequest(BaseModel):
    """Schema for requesting a password reset."""
    email: EmailStr


    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.REGISTERED
    file_uploads: List[str] = []  # List of file IDs uploaded by the user


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for password reset."""
    token: str
    new_password: str = Field(..., min_length=8)


class User(BaseModel):
    """Schema for user information."""
    email: EmailStr
    full_name: Optional[str] =