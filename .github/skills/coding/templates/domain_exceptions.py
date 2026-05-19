"""Domain exception scaffold — base and derived exceptions."""


class AppBaseError(Exception):
    """Base for all application exceptions."""


class ItemNotFoundError(AppBaseError):
    def __init__(self, item_id: str) -> None:
        super().__init__(f"Item not found: {item_id}")
        self.item_id = item_id
