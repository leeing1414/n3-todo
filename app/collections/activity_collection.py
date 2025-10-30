from dataclasses import asdict
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.activity_document import ActivityDocument
from app.utils.mongo_helpers import serialize_document


class ActivityCollection:
    _collection = db["activities"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index("project_id")
        await cls._collection.create_index("task_id")
        await cls._collection.create_index("occurred_at")

    @classmethod
    async def insert(cls, document: ActivityDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def recent_for_project(cls, project_id: str, limit: int = 20) -> list[dict[str, Any]]:
        cursor = (
            cls._collection.find({"project_id": ObjectId(project_id)})
            .sort("occurred_at", -1)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        return [serialize_document(item) for item in items]

    @classmethod
    async def recent_global(cls, limit: int = 20) -> list[dict[str, Any]]:
        cursor = cls._collection.find().sort("occurred_at", -1).limit(limit)
        items = await cursor.to_list(length=limit)
        return [serialize_document(item) for item in items]
