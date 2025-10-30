from datetime import datetime

from bson import ObjectId

from app.collections.task_collection import TaskCollection
from app.documents.task_document import TaskDocument
from app.requests.task_request import TaskCreateRequest, TaskUpdateRequest
from app.schemas.enums import ActivityAction
from app.schemas.models import TaskDTO
from app.services import mappers
from app.services.activity_service import ActivityService


class TaskService:
    @staticmethod
    async def create_task(request: TaskCreateRequest, *, actor_id: str | None = None) -> TaskDTO:
        document = TaskDocument(
            project_id=ObjectId(request.project_id),
            title=request.title,
            description=request.description,
            status=request.status,
            priority=request.priority,
            progress=request.progress,
            start_date=request.start_date,
            due_date=request.due_date,
            assignee_id=ObjectId(request.assignee_id) if request.assignee_id else None,
            content=request.content,
            references=request.references,
            tags=request.tags,
            checklist=request.checklist,
            created_by=actor_id,
            updated_by=actor_id,
        )
        inserted_id = await TaskCollection.insert(document)
        created = await TaskCollection.find_by_id(str(inserted_id))
        if not created:
            raise RuntimeError("Failed to load task after creation")
        await ActivityService.log(
            project_id=request.project_id,
            task_id=str(inserted_id),
            actor_id=actor_id,
            action=ActivityAction.created,
            detail=f"Task '{request.title}' created",
        )
        return mappers.map_task(created)

    @staticmethod
    async def list_tasks(project_id: str) -> list[TaskDTO]:
        documents = await TaskCollection.find_by_project(project_id)
        return [mappers.map_task(doc) for doc in documents]

    @staticmethod
    async def get_task(task_id: str) -> TaskDTO | None:
        document = await TaskCollection.find_by_id(task_id)
        return mappers.map_task(document) if document else None

    @staticmethod
    async def update_task(
        task_id: str, request: TaskUpdateRequest, *, actor_id: str | None = None
    ) -> bool:
        payload = request.model_dump(exclude_none=True)
        if actor_id:
            payload["updated_by"] = actor_id
        updated = await TaskCollection.update(task_id, payload)
        if updated:
            await ActivityService.log(
                task_id=task_id,
                actor_id=actor_id,
                action=ActivityAction.updated,
                detail=f"Task '{task_id}' updated",
            )
        return updated

    @staticmethod
    async def delete_task(task_id: str) -> bool:
        deleted = await TaskCollection.delete(task_id)
        if deleted:
            await ActivityService.log(
                task_id=task_id,
                actor_id=None,
                action=ActivityAction.updated,
                detail="Task deleted",
            )
        return deleted

    @staticmethod
    async def stats(project_id: str) -> dict:
        return {
            "status": await TaskCollection.stats_by_status(project_id),
            "priority": await TaskCollection.stats_by_priority(project_id),
        }

    @staticmethod
    async def calendar(start: datetime, end: datetime) -> list[TaskDTO]:
        documents = await TaskCollection.find_for_calendar(start, end)
        return [mappers.map_task(doc) for doc in documents]
