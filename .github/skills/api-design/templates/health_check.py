"""Health check endpoint scaffold."""

import os

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", status_code=200)
async def health():
    return {"status": "healthy", "version": os.getenv("APP_VERSION", "unknown")}
