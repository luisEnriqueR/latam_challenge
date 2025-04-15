import logging
from datetime import datetime
from typing import List, Tuple

from sqlalchemy import func
from sqlmodel import Session, select

from app.exceptions.user_exceptions import (
    EmailAlreadyExists,
    NoFieldsToUpdate,
    UsernameAlreadyExists,
    UserNotFound,
)
from app.models.user import User
from app.schemas.users import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)


def create_user(user_create: UserCreate, session: Session) -> User:
    existing_user = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()
    if existing_user:
        logger.warning(
            f"Attempt to create user with username {user_create.username}, but already exists"
        )
        raise UsernameAlreadyExists()

    existing_email = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()
    if existing_email:
        logger.warning(
            f"Attempt to create user with email {user_create.email}, but already exists"
        )
        raise EmailAlreadyExists()

    user = User(
        **user_create.model_dump(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User with ID {user.id} has been created")
    return user


def get_user_by_id(user_id: int, session: Session) -> UserRead:
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
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


def update_user(
    user_id: int, update_data: UserUpdate, session: Session
) -> User:
    user = session.get(User, user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found for update")
        raise UserNotFound(user_id)

    changes_made = 0
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if value:
            setattr(user, key, value)
            changes_made += 1

    if changes_made == 0:
        logger.warning(
            f"There are nochanges for user with ID {user_id}"
        )
        raise NoFieldsToUpdate()

    user.updated_at = datetime.now()

    session.add(user)
    session.commit()
    session.refresh(user)
    logger.info(f"User with ID {user_id} updated")
    return user


def delete_user(user_id: int, session: Session) -> None:
    user = session.get(User, user_id)
    if not user:
        logger.warning(
            f"User with ID {user_id} not found for deletion"
        )
        raise UserNotFound(user_id)

    session.delete(user)
    session.commit()
    logger.info(f"User with ID {user_id} deleted")
