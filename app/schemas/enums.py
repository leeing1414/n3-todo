from enum import Enum


class ProjectStatus(str, Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    on_hold = "on_hold"
    cancelled = "cancelled"


class ProjectPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ProjectRisk(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    blocked = "blocked"
    done = "done"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class SubtaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    member = "member"


class ActivityAction(str, Enum):
    created = "created"
    updated = "updated"
    status_changed = "status_changed"
    comment = "comment"
    attachment_added = "attachment_added"
