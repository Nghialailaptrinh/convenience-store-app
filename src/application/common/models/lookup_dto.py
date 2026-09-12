from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class LookupDto:
    id: UUID
    title: str
