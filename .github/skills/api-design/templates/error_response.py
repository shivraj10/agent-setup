"""Error response models — standardised error shapes for all APIs."""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    error: str  # machine-readable code: "VALIDATION_ERROR"
    message: str  # human-readable summary
    details: list[ErrorDetail] = []
