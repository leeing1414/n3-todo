from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.enums import (
    ActivityAction,
    ProjectPriority,
    ProjectRisk,
    ProjectStatus,
    SubtaskStatus,
    TaskPriority,
    TaskStatus,
    UserRole,
)


class CompanyDTO(BaseModel):
    id: str
    name: str
    description: str | None = None
    domain: str | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class DepartmentDTO(BaseModel):
    id: str
    company_id: str
    name: str
    description: str | None = None
    lead_id: str | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class UserDTO(BaseModel):
    id: str
    email: str
    name: str
    role: UserRole
    department: str | None = None
    department_id: str | None = None
    title: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool
    timezone: str | None = None
    created_at: datetime
    updated_at: datetime


class ProjectDTO(BaseModel):
    id: str
    title: str
    description: str | None = None
    department_id: str
    status: ProjectStatus
    priority: ProjectPriority
    risk_level: ProjectRisk
    progress: float
    start_date: datetime | None = None
    end_date: datetime | None = None
    assignee_id: str | None = None
    content: str | None = None
    references: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    member_ids: list[str] = Field(default_factory=list)
    watcher_ids: list[str] = Field(default_factory=list)
    department_name: str | None = None
    created_at: datetime
    updated_at: datetime


class TaskDTO(BaseModel):
    id: str
    project_id: str
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    progress: float
    start_date: datetime | None = None
    due_date: datetime | None = None
    assignee_id: str | None = None
    content: str | None = None
    references: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    checklist: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class SubtaskDTO(BaseModel):
    id: str
    task_id: str
    title: str
    content: str | None = None
    status: SubtaskStatus
    assignee_id: str | None = None
    order: int
    due_date: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ActivityDTO(BaseModel):
    id: str
    project_id: str | None = None
    task_id: str | None = None
    actor_id: str | None = None
    action: ActivityAction
    detail: str | None = None
    occurred_at: datetime
    created_at: datetime
    updated_at: datetime


class DashboardSummaryDTO(BaseModel):
    project_total: int
    active_projects: int
    overdue_tasks: int
    upcoming_deadlines: list[dict[str, Any]]
    project_status_distribution: list[dict[str, Any]]
    task_status_distribution: list[dict[str, Any]]
    department_workload: list[dict[str, Any]]
    recent_activities: list[ActivityDTO]
