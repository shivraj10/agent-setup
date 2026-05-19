"""Timing wrapper scaffold — measure operation duration."""

import time

import structlog

logger = structlog.get_logger()


async def run(self, request):
    t0 = time.perf_counter()
    try:
        result = await self._execute(request)
        logger.info(
            "operation_completed",
            tab=request.tab,
            duration_ms=round((time.perf_counter() - t0) * 1000),
        )
        return result
    except Exception as exc:
        logger.error(
            "operation_failed",
            tab=request.tab,
            duration_ms=round((time.perf_counter() - t0) * 1000),
            error=str(exc),
            exc_info=True,
        )
        raise
