from dataclasses import asdict
from datetime import datetime
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.task_document import TaskDocument
from app.utils.mongo_helpers import serialize_document


class TaskCollection:
    _collection = db["tasks"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index("project_id")
        await cls._collection.create_index("status")
        await cls._collection.create_index("assignee_id")
        await cls._collection.create_index("due_date")

    @classmethod
    async def insert(cls, document: TaskDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_by_id(cls, task_id: str) -> dict[str, Any] | None:
        document = await cls._collection.find_one({"_id": ObjectId(task_id)})
        return serialize_document(document)

    @classmethod
    async def find_by_project(cls, project_id: str) -> list[dict[str, Any]]:
        cursor = (
            cls._collection.find({"project_id": ObjectId(project_id)})
            .sort([("priority", -1), ("due_date", 1)])
        )
        items = await cursor.to_list(length=1000)
        return [serialize_document(item) for item in items]

    @classmethod
    async def find_for_calendar(cls, start: datetime, end: datetime) -> list[dict[str, Any]]:
        cursor = cls._collection.find(
            {"due_date": {"$gte": start, "$lte": end}}
        ).sort("due_date", 1)
        items = await cursor.to_list(length=1000)
        return [serialize_document(item) for item in items]

    @classmethod
    async def find_overdue(cls, now: datetime, limit: int = 10) -> list[dict[str, Any]]:
        cursor = (
            cls._collection.find(
                {
                    "due_date": {"$lt": now},
                    "status": {"$nin": ["done"]},
                }
            )
            .sort("due_date", 1)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        return [serialize_document(item) for item in items]

    @classmethod
    async def find_upcoming(cls, now: datetime, limit: int = 10) -> list[dict[str, Any]]:
        cursor = (
            cls._collection.find(
                {
                    "due_date": {"$gte": now},
                    "status": {"$nin": ["done"]},
                }
            )
            .sort("due_date", 1)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        return [serialize_document(item) for item in items]

    @classmethod
    async def update(cls, task_id: str, data: dict[str, Any]) -> bool:
        if "assignee_id" in data and data["assignee_id"]:
            data["assignee_id"] = ObjectId(data["assignee_id"])
        elif "assignee_id" in data and data["assignee_id"] is None:
            data["assignee_id"] = None
        data["updated_at"] = datetime.utcnow()
        result = await cls._collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": data}
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, task_id: str) -> bool:
        result = await cls._collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    @classmethod
    async def stats_by_status(cls, project_id: str) -> list[dict[str, Any]]:
        pipeline = [
            {"$match": {"project_id": ObjectId(project_id)}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$project": {"status": "$_id", "count": 1, "_id": 0}},
        ]
        cursor = cls._collection.aggregate(pipeline)
        return [item async for item in cursor]

    @classmethod
    async def stats_by_priority(cls, project_id: str) -> list[dict[str, Any]]:
        pipeline = [
            {"$match": {"project_id": ObjectId(project_id)}},
            {"$group": {"_id": "$priority", "count": {"$sum": 1}}},
            {"$project": {"priority": "$_id", "count": 1, "_id": 0}},
        ]
        cursor = cls._collection.aggregate(pipeline)
        return [item async for item in cursor]

    @classmethod
    async def stats_all_status(cls) -> list[dict[str, Any]]:
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$project": {"status": "$_id", "count": 1, "_id": 0}},
        ]
        cursor = cls._collection.aggregate(pipeline)
        return [item async for item in cursor]

    @classmethod
    async def count_overdue(cls, now: datetime) -> int:
        return await cls._collection.count_documents(
            {"due_date": {"$lt": now}, "status": {"$nin": ["done"]}}
        )
