from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.schemas.enums import ProjectPriority, ProjectRisk, ProjectStatus


class ProjectCreateRequest(BaseModel):
    title: str
    description: str | None = None
    department_id: str = Field(..., description="Owning department id")
    status: ProjectStatus = ProjectStatus.planned
    priority: ProjectPriority = ProjectPriority.medium
    risk_level: ProjectRisk = ProjectRisk.low
    progress: float = Field(default=0.0, ge=0, le=100)
    start_date: datetime | None = None
    end_date: datetime | None = None
    assignee_id: str | None = None
    content: str | None = None
    references: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    member_ids: List[str] = Field(default_factory=list)
    watcher_ids: List[str] = Field(default_factory=list)
    department_name: str | None = None


class ProjectUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ProjectStatus | None = None
    priority: ProjectPriority | None = None
    risk_level: ProjectRisk | None = None
    progress: float | None = Field(default=None, ge=0, le=100)
    start_date: datetime | None = None
    end_date: datetime | None = None
    assignee_id: str | None = None
    content: str | None = None
    references: list[str] | None = None
    tags: list[str] | None = None
    member_ids: List[str] | None = None
    watcher_ids: List[str] | None = None
    department_name: str | None = None
