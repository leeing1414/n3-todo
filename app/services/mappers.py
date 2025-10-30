from typing import Any

from app.schemas.models import (
    ActivityDTO,
    CompanyDTO,
    DepartmentDTO,
    ProjectDTO,
    SubtaskDTO,
    TaskDTO,
    UserDTO,
)


def _filter_payload(payload: dict[str, Any], allowed: set[str]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key in allowed}


def map_company(raw: dict[str, Any]) -> CompanyDTO:
    allowed = {
        "id",
        "name",
        "description",
        "domain",
        "tags",
        "created_at",
        "updated_at",
    }
    return CompanyDTO(**_filter_payload(raw, allowed))


def map_department(raw: dict[str, Any]) -> DepartmentDTO:
    allowed = {
        "id",
        "company_id",
        "name",
        "description",
        "lead_id",
        "tags",
        "created_at",
        "updated_at",
    }
    return DepartmentDTO(**_filter_payload(raw, allowed))


def map_user(raw: dict[str, Any]) -> UserDTO:
    allowed = {
        "id",
        "email",
        "name",
        "role",
        "department_id",
        "title",
        "phone",
        "avatar_url",
        "is_active",
        "timezone",
        "created_at",
        "updated_at",
    }
    return UserDTO(**_filter_payload(raw, allowed))


def map_project(raw: dict[str, Any]) -> ProjectDTO:
    allowed = {
        "id",
        "title",
        "description",
        "department_id",
        "status",
        "priority",
        "risk_level",
        "progress",
        "start_date",
        "end_date",
        "assignee_id",
        "content",
        "references",
        "tags",
        "member_ids",
        "watcher_ids",
        "department_name",
        "created_at",
        "updated_at",
    }
    return ProjectDTO(**_filter_payload(raw, allowed))


def map_task(raw: dict[str, Any]) -> TaskDTO:
    allowed = {
        "id",
        "project_id",
        "title",
        "description",
        "status",
        "priority",
        "progress",
        "start_date",
        "due_date",
        "assignee_id",
        "content",
        "references",
        "tags",
        "checklist",
        "created_at",
        "updated_at",
    }
    return TaskDTO(**_filter_payload(raw, allowed))


def map_subtask(raw: dict[str, Any]) -> SubtaskDTO:
    allowed = {
        "id",
        "task_id",
        "title",
        "content",
        "status",
        "assignee_id",
        "order",
        "due_date",
        "created_at",
        "updated_at",
    }
    return SubtaskDTO(**_filter_payload(raw, allowed))


def map_activity(raw: dict[str, Any]) -> ActivityDTO:
    allowed = {
        "id",
        "project_id",
        "task_id",
        "actor_id",
        "action",
        "detail",
        "occurred_at",
        "created_at",
        "updated_at",
    }
    return ActivityDTO(**_filter_payload(raw, allowed))
