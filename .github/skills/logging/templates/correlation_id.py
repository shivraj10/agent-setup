"""Correlation ID scaffold — request tracing across Lambda / FastAPI."""

import uuid
from contextvars import ContextVar

import structlog
from fastapi import Request

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def set_correlation_id(request_id: str | None = None) -> str:
    cid = request_id or str(uuid.uuid4())
    correlation_id.set(cid)
    structlog.contextvars.bind_contextvars(correlation_id=cid)
    return cid


# --- Lambda handler usage ---
def lambda_handler(event, context):
    set_correlation_id(context.aws_request_id)
    ...


# --- FastAPI middleware usage ---
async def correlation_middleware(request: Request, call_next):
    cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    set_correlation_id(cid)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response
