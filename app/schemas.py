from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass
    

class PostResponse(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class User(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
  
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
