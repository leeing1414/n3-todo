from datetime import datetime

from pydantic import BaseModel

from app.schemas.enums import SubtaskStatus


class SubtaskCreateRequest(BaseModel):
    task_id: str
    title: str
    content: str | None = None
    status: SubtaskStatus = SubtaskStatus.todo
    assignee_id: str | None = None
    order: int = 0
    due_date: datetime | None = None


class SubtaskUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None
    status: SubtaskStatus | None = None
    assignee_id: str | None = None
    order: int | None = None
    due_date: datetime | None = None
