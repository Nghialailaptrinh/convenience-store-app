from dataclasses import dataclass
from uuid import UUID


@dataclass
class Category:
    id: UUID
    name: str
