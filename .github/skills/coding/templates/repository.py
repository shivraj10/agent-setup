"""Repository scaffold — all external I/O lives here."""

import os

import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.getenv("TABLE_NAME", "")


class MessageRepository:
    def __init__(self) -> None:
        self._table = boto3.resource("dynamodb").Table(TABLE_NAME)

    def save(self, message: "Message") -> None:
        try:
            self._table.put_item(
                Item=message.model_dump(),
                ConditionExpression="attribute_not_exists(pk)",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise DuplicateMessageError(message.id) from e
            raise
