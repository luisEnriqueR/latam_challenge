from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.database.database import get_session
from app.schemas.common import APIResponse
from app.schemas.user import PaginatedResponse, UserCreate
from app.services.users import (
    create_user,
    get_user_by_id,
    get_users_paginated,
)

router = APIRouter()


@router.post(
    "/",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_endpoint(
    user_create: UserCreate, session: Session = Depends(get_session)
):
    user = create_user(user_create, session)
    return APIResponse(
        status="success",
        data=user.model_dump(),
        message="User created successfully.",
        response_time=datetime.now(),
    )


@router.get("/{user_id}", response_model=APIResponse)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(user_id, session)
    return APIResponse(
        status="success",
        data=user.model_dump(),
        message="User fetched successfully.",
        response_time=datetime.now(),
    )


@router.get("/", response_model=PaginatedResponse)
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session),
):
    users, total = get_users_paginated(session, page, limit)
    return PaginatedResponse(
        status="success",
        data=[user.model_dump() for user in users],
        total=total,
        page=page,
        limit=limit,
        message="Users fetched successfully.",
        response_time=datetime.now(),
    )
