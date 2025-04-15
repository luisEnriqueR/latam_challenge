from datetime import datetime
from typing import Any, List, Optional, Union

from pydantic import BaseModel


class APIResponse(BaseModel):
    status: str
    data: Optional[Union[dict, list]] = None
    message: Optional[str] = None
    response_time: datetime


class PaginatedResponse(BaseModel):
    status: str
    data: List[Any]
    total: int
    page: int
    limit: int
    message: Optional[str]
    response_time: datetime
