from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, List

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
        from_attributes = True

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

class PaginatedUsers(BaseModel):
    total: int
    total_pages: int
    page: int
    limit: int
    users: List[UserOut]

class PagingInfo(BaseModel):
    page: int
    size: int
    totalItems: int
    totalPages: int
    hasNext: bool

class UserListResponse(BaseModel):
    paging: PagingInfo
    users: List[UserOut]