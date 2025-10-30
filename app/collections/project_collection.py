from dataclasses import asdict
from datetime import datetime
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.project_document import ProjectDocument
from app.utils.mongo_helpers import serialize_document


class ProjectCollection:
    _collection = db["projects"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index("department_id")
        await cls._collection.create_index("status")
        await cls._collection.create_index("tags")

    @classmethod
    async def insert(cls, document: ProjectDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_by_id(cls, project_id: str) -> dict[str, Any] | None:
        document = await cls._collection.find_one({"_id": ObjectId(project_id)})
        return serialize_document(document)

    @classmethod
    async def find_many(
        cls,
        *,
        department_id: str | None = None,
        statuses: list[str] | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {}
        if department_id:
            query["department_id"] = ObjectId(department_id)
        if statuses:
            query["status"] = {"$in": statuses}
        cursor = (
            cls._collection.find(query)
            .sort([("priority", -1), ("start_date", 1)])
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        return [serialize_document(item) for item in items]

    @classmethod
    async def update(cls, project_id: str, data: dict[str, Any]) -> bool:
        if "member_ids" in data and data["member_ids"] is not None:
            data["member_ids"] = [ObjectId(member) for member in data["member_ids"] if member]
        if "watcher_ids" in data and data["watcher_ids"] is not None:
            data["watcher_ids"] = [ObjectId(member) for member in data["watcher_ids"] if member]
        if "assignee_id" in data:
            data["assignee_id"] = ObjectId(data["assignee_id"]) if data["assignee_id"] else None
        data["updated_at"] = datetime.utcnow()
        result = await cls._collection.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": data},
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, project_id: str) -> bool:
        result = await cls._collection.delete_one({"_id": ObjectId(project_id)})
        return result.deleted_count > 0

    @classmethod
    async def count(cls, query: dict[str, Any] | None = None) -> int:
        return await cls._collection.count_documents(query or {})

    @classmethod
    async def stats_by_status(cls) -> list[dict[str, Any]]:
        pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$project": {"status": "$_id", "count": 1, "_id": 0}},
        ]
        cursor = cls._collection.aggregate(pipeline)
        return [item async for item in cursor]

    @classmethod
    async def stats_by_department(cls) -> list[dict[str, Any]]:
        pipeline = [
            {"$group": {"_id": "$department_id", "count": {"$sum": 1}}},
            {
                "$project": {
                    "department_id": {"$toString": "$_id"},
                    "count": 1,
                    "_id": 0,
                }
            },
        ]
        cursor = cls._collection.aggregate(pipeline)
        return [item async for item in cursor]
