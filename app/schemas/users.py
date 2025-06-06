from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel

from app.models.user import RoleEnum


class UserCreate(SQLModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleEnum
    active: Optional[bool] = True


class UserRead(SQLModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleEnum
    created_at: datetime
    updated_at: datetime
    active: bool


class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[RoleEnum] = None
    active: Optional[bool] = None
