from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str | None = None
    phone: str | None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
