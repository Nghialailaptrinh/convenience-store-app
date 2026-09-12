from dataclasses import dataclass
from uuid import UUID


@dataclass
class Customer:
    id: UUID
    name: str
    email: str
