import dataclasses
from datetime import datetime

from bson import ObjectId

from app.base.base_document import AuditDocument
from app.schemas.enums import SubtaskStatus


@dataclasses.dataclass(kw_only=True, frozen=True)
class SubtaskDocument(AuditDocument):
    task_id: ObjectId
    title: str
    content: str | None = None
    status: SubtaskStatus = SubtaskStatus.todo
    assignee_id: ObjectId | None = None
    order: int = 0
    due_date: datetime | None = None
