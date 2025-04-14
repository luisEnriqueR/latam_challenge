from datetime import datetime
from typing import List, Tuple

from sqlalchemy import func
from sqlmodel import Session, select

from app.exceptions.user_exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotFound,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserRead


def create_user(user_create: UserCreate, session: Session) -> User:
    existing_user = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if existing_user:
        raise UsernameAlreadyExists()

    existing_email = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()
    if existing_email:
        raise EmailAlreadyExists()

    user = User(
        **user_create.model_dump(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_id(user_id: int, session: Session) -> UserRead:
    user = session.get(User, user_id)
    if not user:
        raise UserNotFound(user_id)
    return user


def get_users_paginated(
    session: Session, page: int = 1, limit: int = 10
) -> Tuple[List[User], int]:
    offset = (page - 1) * limit
    statement = select(User).offset(offset).limit(limit)
    users = session.exec(statement).all()

    total = session.exec(select(func.count()).select_from(User)).one()
    return users, total
