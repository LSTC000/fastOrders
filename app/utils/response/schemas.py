from enum import Enum

from .details import Details

from pydantic import BaseModel


class StatusType(Enum):
    success: str = 'success'
    error: str = 'error'


class BaseAPIResponse(BaseModel):
    status: StatusType = StatusType.success
    data: dict = {}
    detail: str = Details.success_status
