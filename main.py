from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.v1 import users
from app.core.exception_handler import (
    exception_handler,
    validation_exception_handler,
)
from app.core.logging_config import setup_logging
from app.database.init_db import init_db
from app.exceptions.app_exceptions import AppException

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Latam Airlines Code Challenge", lifespan=lifespan
)


@app.exception_handler(AppException)
def custom_exception_handler(request, exc):
    return exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
def handle_422(request, exc):
    return validation_exception_handler(request, exc)


app.include_router(users.router, prefix="/api/v1/users")
