from dataclasses import dataclass
from datetime import datetime

from domain.common.base_entity import BaseEntity


@dataclass(kw_only=True)
class BaseAuditableEntity(BaseEntity):
    """Audit fields for future persistence adapters; values are not populated automatically."""

    created: datetime | None = None
    created_by: str | None = None
    last_modified: datetime | None = None
    last_modified_by: str | None = None
