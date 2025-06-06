import logging
from datetime import datetime

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.app_exceptions import AppException

logger = logging.getLogger(__name__)


def exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": None,
            "message": exc.message,
            "response_time": datetime.now().isoformat(),
        },
    )


def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning(
        f"422 Validation error at {request.method} {request.url.path}: {exc.errors()}"
    )
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "data": exc.errors(),
            "message": "Validation error",
            "response_time": datetime.now().isoformat(),
        },
    )
