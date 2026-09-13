class UnauthenticatedError(Exception):
    def __init__(self) -> None:
        super().__init__("Authentication required")
