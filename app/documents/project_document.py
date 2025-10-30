import dataclasses
from datetime import datetime

from bson import ObjectId

from app.base.base_document import AuditDocument
from app.schemas.enums import ProjectPriority, ProjectRisk, ProjectStatus


@dataclasses.dataclass(kw_only=True, frozen=True)
class ProjectDocument(AuditDocument):
    title: str
    description: str | None
    department_id: ObjectId
    status: ProjectStatus = ProjectStatus.planned
    priority: ProjectPriority = ProjectPriority.medium
    risk_level: ProjectRisk = ProjectRisk.low
    progress: float = 0.0
    start_date: datetime | None = None
    end_date: datetime | None = None
    assignee_id: ObjectId | None = None
    content: str | None = None
    references: list[str] = dataclasses.field(default_factory=list)
    tags: list[str] = dataclasses.field(default_factory=list)
    member_ids: list[ObjectId] = dataclasses.field(default_factory=list)
    watcher_ids: list[ObjectId] = dataclasses.field(default_factory=list)
    department_name: str | None = None
