from datetime import datetime, timezone

from app.collections.project_collection import ProjectCollection
from app.collections.task_collection import TaskCollection
from app.schemas.enums import ProjectStatus
from app.schemas.models import DashboardSummaryDTO
from app.services import mappers
from app.services.activity_service import ActivityService


class DashboardService:
    @staticmethod
    async def get_summary() -> DashboardSummaryDTO:
        now = datetime.now(tz=timezone.utc)
        total_projects = await ProjectCollection.count()
        active_projects = await ProjectCollection.count(
            {"status": {"$in": [ProjectStatus.planned.value, ProjectStatus.in_progress.value]}}
        )
        overdue_tasks = await TaskCollection.count_overdue(now)
        upcoming_deadlines = await TaskCollection.find_upcoming(now, limit=10)
        project_status_distribution = await ProjectCollection.stats_by_status()
        task_status_distribution = await TaskCollection.stats_all_status()
        department_workload = await ProjectCollection.stats_by_department()
        recent_raw = await ActivityService.recent(limit=15)
        recent_activities = [mappers.map_activity(item) for item in recent_raw]
        return DashboardSummaryDTO(
            project_total=total_projects,
            active_projects=active_projects,
            overdue_tasks=overdue_tasks,
            upcoming_deadlines=upcoming_deadlines,
            project_status_distribution=project_status_distribution,
            task_status_distribution=task_status_distribution,
            department_workload=department_workload,
            recent_activities=recent_activities,
        )
