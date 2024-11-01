from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(strict=True)
    
    id: int
    username: str
    password: bytes
    email: EmailStr

    is_active: bool


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

    is_active: bool = True


class UserUpdate(BaseModel):
    pass

