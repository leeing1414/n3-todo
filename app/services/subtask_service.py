from bson import ObjectId

from app.collections.subtask_collection import SubtaskCollection
from app.documents.subtask_document import SubtaskDocument
from app.requests.subtask_request import SubtaskCreateRequest, SubtaskUpdateRequest
from app.schemas.enums import ActivityAction
from app.schemas.models import SubtaskDTO
from app.services import mappers
from app.services.activity_service import ActivityService


class SubtaskService:
    @staticmethod
    async def create_subtask(
        request: SubtaskCreateRequest, *, actor_id: str | None = None
    ) -> SubtaskDTO:
        document = SubtaskDocument(
            task_id=ObjectId(request.task_id),
            title=request.title,
            content=request.content,
            status=request.status,
            assignee_id=ObjectId(request.assignee_id) if request.assignee_id else None,
            order=request.order,
            due_date=request.due_date,
            created_by=actor_id,
            updated_by=actor_id,
        )
        inserted_id = await SubtaskCollection.insert(document)
        created = await SubtaskCollection.find_by_id(str(inserted_id))
        if not created:
            raise RuntimeError("Failed to load subtask after creation")
        await ActivityService.log(
            task_id=request.task_id,
            actor_id=actor_id,
            action=ActivityAction.created,
            detail=f"Subtask '{request.title}' created",
        )
        return mappers.map_subtask(created)

    @staticmethod
    async def get_subtask(subtask_id: str) -> SubtaskDTO | None:
        document = await SubtaskCollection.find_by_id(subtask_id)
        return mappers.map_subtask(document) if document else None

    @staticmethod
    async def list_subtasks(task_id: str) -> list[SubtaskDTO]:
        documents = await SubtaskCollection.find_by_task(task_id)
        return [mappers.map_subtask(doc) for doc in documents]

    @staticmethod
    async def update_subtask(
        subtask_id: str, request: SubtaskUpdateRequest, *, actor_id: str | None = None
    ) -> bool:
        existing = await SubtaskCollection.find_by_id(subtask_id)
        if not existing:
            return False
        payload = request.model_dump(exclude_none=True)
        if actor_id:
            payload["updated_by"] = actor_id
        updated = await SubtaskCollection.update(subtask_id, payload)
        if updated:
            await ActivityService.log(
                task_id=existing["task_id"],
                actor_id=actor_id,
                action=ActivityAction.updated,
                detail=f"Subtask '{subtask_id}' updated",
            )
        return updated

    @staticmethod
    async def delete_subtask(subtask_id: str) -> bool:
        existing = await SubtaskCollection.find_by_id(subtask_id)
        if not existing:
            return False
        deleted = await SubtaskCollection.delete(subtask_id)
        if deleted:
            await ActivityService.log(
                task_id=existing["task_id"],
                actor_id=None,
                action=ActivityAction.updated,
                detail="Subtask deleted",
            )
        return deleted

    @staticmethod
    async def reorder(task_id: str, ordered_ids: list[str]) -> None:
        await SubtaskCollection.reorder(task_id, ordered_ids)
