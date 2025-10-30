from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.enums import TaskPriority, TaskStatus


class TaskCreateRequest(BaseModel):
    project_id: str
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    progress: float = Field(default=0.0, ge=0, le=100)
    start_date: datetime | None = None
    due_date: datetime | None = None
    assignee_id: str | None = None
    content: str | None = None
    references: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    checklist: list[str] = Field(default_factory=list)


class TaskUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    progress: float | None = Field(default=None, ge=0, le=100)
    start_date: datetime | None = None
    due_date: datetime | None = None
    assignee_id: str | None = None
    content: str | None = None
    references: list[str] | None = None
    tags: list[str] | None = None
    checklist: list[str] | None = None
