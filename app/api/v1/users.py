from datetime import datetime

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.database.database import get_session
from app.schemas.common import APIResponse, PaginatedResponse
from app.schemas.users import UserCreate, UserUpdate
from app.services.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users_paginated,
    update_user,
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
    print("Se hace la peticion\n\n")
    user = create_user(user_create, session)
    print(f"el user resultado {user}")
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


@router.put("/{user_id}", response_model=APIResponse)
def update_user_fields(
    user_id: int,
    update_data: UserUpdate,
    session: Session = Depends(get_session),
):
    user = update_user(user_id, update_data, session)
    return APIResponse(
        status="success",
        data=user.model_dump(),
        message="User updated successfully.",
        response_time=datetime.now(),
    )


@router.delete("/{user_id}", response_model=APIResponse)
def delete_user_endpoint(
    user_id: int, session: Session = Depends(get_session)
):
    delete_user(user_id, session)

    return APIResponse(
        status="success",
        data=None,
        message=f"User with ID {user_id} deleted successfully.",
        response_time=datetime.now(),
    )
