from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class UserOut(BaseModel):
    id: int
    created_at: datetime 
    email:EmailStr
    
    class Config:
        orm_mode = True
        

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime    
    owner_id:int
    owner: UserOut
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    

class Token(BaseModel):
    token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
