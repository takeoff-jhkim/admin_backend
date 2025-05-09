from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: UserRole
    nickname: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class UpdateUserRole(BaseModel):
    role: UserRole

class UserCreate(BaseModel):
    email: str
    name: str
    role: str = "user"
    nickname: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str