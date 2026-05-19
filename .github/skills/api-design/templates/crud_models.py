"""CRUD model scaffold — separate Create, Update, and Response models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DonorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    age_group: str


class DonorUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class DonorResponse(BaseModel):
    id: str
    name: str
    email: str
    age_group: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
