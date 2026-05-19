"""Pydantic v2 model scaffold — data shapes with validation."""

from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Message(BaseModel):
    id: str = Field(..., description="Unique message ID")
    payload: dict
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def validate_payload_not_empty(self) -> "Message":
        if not self.payload:
            raise ValueError("payload cannot be empty")
        return self
