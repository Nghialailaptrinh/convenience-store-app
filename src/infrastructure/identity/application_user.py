from dataclasses import dataclass, field


@dataclass(frozen=True)
class ApplicationUser:
    """Local identity account. Customer remains a separate Domain concept."""

    id: str
    email: str
    password_hash: str = field(repr=False)
