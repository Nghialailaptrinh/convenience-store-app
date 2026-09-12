class ValidationException(Exception):
    def __init__(self, errors: dict[str, list[str]]) -> None:
        super().__init__("Request validation failed")
        self.errors = errors
