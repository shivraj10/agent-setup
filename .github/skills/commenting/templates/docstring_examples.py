"""Module docstring template.

This module contains [CLASS_NAME], which [PRIMARY_RESPONSIBILITY].
"""


class ExampleService:
    """Orchestrates [DOMAIN] processing between [DEPENDENCY_A] and [DEPENDENCY_B].

    Attributes:
        gateway: External provider client.
        repository: DynamoDB record store.
    """

    def __init__(self, gateway, repository) -> None:
        """Initialise with external dependencies.

        Args:
            gateway: External provider client.
            repository: DynamoDB record store.
        """
        self.gateway = gateway
        self.repository = repository

    def process(self, request: "RequestModel") -> "ResultModel":
        """Process a request through the gateway and persist the result.

        Validates the request, sends it to the gateway, and saves
        the transaction record.

        Args:
            request: Validated request with required fields.

        Returns:
            ResultModel with transaction ID and status.

        Raises:
            InvalidInputError: If input fails validation.
            GatewayTimeoutError: If gateway doesn't respond after retries.
        """
        ...
