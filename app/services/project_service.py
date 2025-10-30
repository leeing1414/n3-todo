from bson import ObjectId

from app.collections.project_collection import ProjectCollection
from app.collections.task_collection import TaskCollection
from app.documents.project_document import ProjectDocument
from app.requests.project_request import ProjectCreateRequest, ProjectUpdateRequest
from app.schemas.enums import ActivityAction
from app.schemas.models import ProjectDTO
from app.services import mappers
from app.services.activity_service import ActivityService
from app.services.subtask_service import SubtaskService


class ProjectService:
    @staticmethod
    async def create_project(
        request: ProjectCreateRequest, *, actor_id: str | None = None
    ) -> ProjectDTO:
        document = ProjectDocument(
            title=request.title,
            description=request.description,
            department_id=ObjectId(request.department_id),
            status=request.status,
            priority=request.priority,
            risk_level=request.risk_level,
            progress=request.progress,
            start_date=request.start_date,
            end_date=request.end_date,
            assignee_id=ObjectId(request.assignee_id) if request.assignee_id else None,
            content=request.content,
            references=request.references,
            tags=request.tags,
            member_ids=[ObjectId(member) for member in request.member_ids],
            watcher_ids=[ObjectId(member) for member in request.watcher_ids],
            department_name=request.department_name,
            created_by=actor_id,
            updated_by=actor_id,
        )
        inserted_id = await ProjectCollection.insert(document)
        created = await ProjectCollection.find_by_id(str(inserted_id))
        if not created:
            raise RuntimeError("Failed to load project after creation")
        await ActivityService.log(
            project_id=str(inserted_id),
            actor_id=actor_id,
            action=ActivityAction.created,
            detail=f"Project '{request.title}' created",
        )
        return mappers.map_project(created)

    @staticmethod
    async def list_projects(
        *, department_id: str | None = None, statuses: list[str] | None = None
    ) -> list[ProjectDTO]:
        documents = await ProjectCollection.find_many(
            department_id=department_id, statuses=statuses
        )
        return [mappers.map_project(doc) for doc in documents]

    @staticmethod
    async def get_project(project_id: str) -> ProjectDTO | None:
        document = await ProjectCollection.find_by_id(project_id)
        return mappers.map_project(document) if document else None

    @staticmethod
    async def get_project_detail(project_id: str) -> dict:
        project = await ProjectCollection.find_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        tasks = await TaskCollection.find_by_project(project_id)
        enriched_tasks = []
        for task in tasks:
            subtasks = await SubtaskService.list_subtasks(task["id"])
            enriched_tasks.append(
                {
                    "task": mappers.map_task(task).model_dump(),
                    "subtasks": [subtask.model_dump() for subtask in subtasks],
                }
            )
        activities = await ActivityService.recent_for_project(project_id, limit=20)
        return {
            "project": mappers.map_project(project).model_dump(),
            "tasks": enriched_tasks,
            "activities": activities,
        }

    @staticmethod
    async def update_project(
        project_id: str, request: ProjectUpdateRequest, *, actor_id: str | None = None
    ) -> bool:
        payload = request.model_dump(exclude_none=True)
        if actor_id:
            payload["updated_by"] = actor_id
        updated = await ProjectCollection.update(project_id, payload)
        if updated:
            await ActivityService.log(
                project_id=project_id,
                actor_id=actor_id,
                action=ActivityAction.updated,
                detail=f"Project '{project_id}' updated",
            )
        return updated

    @staticmethod
    async def delete_project(project_id: str) -> bool:
        deleted = await ProjectCollection.delete(project_id)
        if deleted:
            await ActivityService.log(
                project_id=project_id,
                actor_id=None,
                action=ActivityAction.updated,
                detail="Project deleted",
            )
        return deleted

    @staticmethod
    async def stats() -> dict:
        status = await ProjectCollection.stats_by_status()
        department = await ProjectCollection.stats_by_department()
        return {"status": status, "department": department}
