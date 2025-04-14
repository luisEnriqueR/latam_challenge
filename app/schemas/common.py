from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class APIResponse(BaseModel):
    status: str
    data: Optional[Union[dict, list]] = None
    message: Optional[str] = None
    response_time: datetime
