from dataclasses import asdict
from datetime import datetime
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.subtask_document import SubtaskDocument
from app.utils.mongo_helpers import serialize_document


class SubtaskCollection:
    _collection = db["subtasks"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index("task_id")
        await cls._collection.create_index([("task_id", 1), ("order", 1)], unique=True)

    @classmethod
    async def insert(cls, document: SubtaskDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_by_id(cls, subtask_id: str) -> dict[str, Any] | None:
        document = await cls._collection.find_one({"_id": ObjectId(subtask_id)})
        return serialize_document(document)

    @classmethod
    async def find_by_task(cls, task_id: str) -> list[dict[str, Any]]:
        cursor = (
            cls._collection.find({"task_id": ObjectId(task_id)}).sort("order", 1)
        )
        items = await cursor.to_list(length=1000)
        return [serialize_document(item) for item in items]

    @classmethod
    async def update(cls, subtask_id: str, data: dict[str, Any]) -> bool:
        if "assignee_id" in data and data["assignee_id"]:
            data["assignee_id"] = ObjectId(data["assignee_id"])
        elif "assignee_id" in data and data["assignee_id"] is None:
            data["assignee_id"] = None
        data["updated_at"] = datetime.utcnow()
        result = await cls._collection.update_one(
            {"_id": ObjectId(subtask_id)}, {"$set": data}
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, subtask_id: str) -> bool:
        result = await cls._collection.delete_one({"_id": ObjectId(subtask_id)})
        return result.deleted_count > 0

    @classmethod
    async def reorder(cls, task_id: str, ordered_ids: list[str]) -> None:
        for order, subtask_id in enumerate(ordered_ids):
            await cls._collection.update_one(
                {"_id": ObjectId(subtask_id), "task_id": ObjectId(task_id)},
                {"$set": {"order": order, "updated_at": datetime.utcnow()}},
            )
