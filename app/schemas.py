from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime
# from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
  
    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        from_attributes = True



class User(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]
