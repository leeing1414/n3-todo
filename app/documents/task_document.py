import dataclasses
from datetime import datetime

from bson import ObjectId

from app.base.base_document import AuditDocument
from app.schemas.enums import TaskPriority, TaskStatus


@dataclasses.dataclass(kw_only=True, frozen=True)
class TaskDocument(AuditDocument):
    project_id: ObjectId
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    progress: float = 0.0
    start_date: datetime | None = None
    due_date: datetime | None = None
    assignee_id: ObjectId | None = None
    content: str | None = None
    references: list[str] = dataclasses.field(default_factory=list)
    tags: list[str] = dataclasses.field(default_factory=list)
    checklist: list[str] = dataclasses.field(default_factory=list)
