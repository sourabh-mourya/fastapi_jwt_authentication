from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# 1. Base User Schema (Common fields)
class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    name: str = Field(..., min_length=2, max_length=50)
    role: str = Field(default="user")

# 2. Registration ke liye (Input)
class RegisterUser(UserBase):
    password: str = Field(..., min_length=8, description="Password should be at least 8 chars")
    address: Optional[str] = None
    mobile: str = Field(..., pattern=r"^\+?1?\d{9,15}$") # Phone number validation
    created_at: datetime = Field(default_factory=datetime.utcnow)

# 3. Login ke liye (Input) - Minimal fields
class LoginUser(BaseModel):
    email: EmailStr
    password: str

# 4. Response ke liye (Output) - Isme password nahi bhejenge
class UserResponse(UserBase):
    id: int # Database ID
    created_at: datetime
    
    class Config:
        from_attributes = True # SQLAlchemy ke saath connect karne ke liye