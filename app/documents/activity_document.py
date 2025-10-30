import dataclasses
from datetime import datetime

from bson import ObjectId

from app.base.base_document import AuditDocument
from app.schemas.enums import ActivityAction


@dataclasses.dataclass(kw_only=True, frozen=True)
class ActivityDocument(AuditDocument):
    project_id: ObjectId | None = None
    task_id: ObjectId | None = None
    actor_id: ObjectId | None = None
    action: ActivityAction = ActivityAction.updated
    detail: str | None = None
    occurred_at: datetime = dataclasses.field(default_factory=datetime.utcnow)
