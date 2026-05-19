"""Lambda handler scaffold — thin handler that delegates to a service."""

import os

import structlog
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = structlog.get_logger()
_service = None  # Replace with: MyService()


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """Process incoming events."""
    logger.info("handler_invoked", record_count=len(event.get("Records", [])))
    batch_failures = []
    for record in event.get("Records", []):
        try:
            msg = MyModel.model_validate_json(record["body"])
            _service.process(msg)
        except Exception as e:
            logger.error("record_failed", message_id=record["messageId"], error=str(e))
            batch_failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": batch_failures}
