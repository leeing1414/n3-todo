from typing import Generic, TypeVar

from pydantic import BaseModel, Field

TData = TypeVar('TData')


class BaseResponse(BaseModel, Generic[TData]):
    """Base API response envelope used across the service."""

    status_code: int = Field(..., description="HTTP status code for the response")
    detail: str = Field(..., description="Human readable message with extra details")
    data: TData | None = Field(default=None, description="Payload returned by the endpoint")
