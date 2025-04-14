from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    role: RoleEnum
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())
    active: bool = True
