from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    message: str    

class ErrorRsponse(BaseModel): 
    message: str   

class RoleBase(BaseModel):
    name: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    roles: Optional[List[str]] = None
