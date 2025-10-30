import dataclasses
from datetime import datetime, timezone

from bson import ObjectId


@dataclasses.dataclass(kw_only=True, frozen=True)
class BaseDocument:
    """Base MongoDB document with an immutable ObjectId."""

    _id: ObjectId = dataclasses.field(default_factory=ObjectId)

    @property
    def id(self) -> str:
        return str(self._id)


@dataclasses.dataclass(kw_only=True, frozen=True)
class AuditDocument(BaseDocument):
    """Base document that tracks creation and update metadata."""

    created_at: datetime = dataclasses.field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    updated_at: datetime = dataclasses.field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
    created_by: str | None = None
    updated_by: str | None = None

    def with_updated(self, *, updated_by: str | None = None) -> "AuditDocument":
        return dataclasses.replace(
            self,
            updated_at=datetime.now(tz=timezone.utc),
            updated_by=updated_by,
        )
