from bson import ObjectId

from app.collections.activity_collection import ActivityCollection
from app.documents.activity_document import ActivityDocument
from app.schemas.enums import ActivityAction
from app.services import mappers


class ActivityService:
    @staticmethod
    async def log(
        *,
        project_id: str | None = None,
        task_id: str | None = None,
        actor_id: str | None = None,
        action: ActivityAction,
        detail: str | None = None,
    ) -> None:
        document = ActivityDocument(
            project_id=ObjectId(project_id) if project_id else None,
            task_id=ObjectId(task_id) if task_id else None,
            actor_id=ObjectId(actor_id) if actor_id else None,
            action=action,
            detail=detail,
            created_by=actor_id,
            updated_by=actor_id,
        )
        await ActivityCollection.insert(document)

    @staticmethod
    async def recent_for_project(project_id: str, limit: int = 20):
        documents = await ActivityCollection.recent_for_project(project_id, limit)
        return [mappers.map_activity(doc) for doc in documents]

    @staticmethod
    async def recent(limit: int = 20):
        documents = await ActivityCollection.recent_global(limit)
        return [mappers.map_activity(doc) for doc in documents]
