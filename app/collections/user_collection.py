from dataclasses import asdict
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.user_document import UserDocument
from app.utils.mongo_helpers import serialize_document


class UserCollection:
    _collection = db["users"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index("email", unique=True)
        await cls._collection.create_index("department_id")

    @classmethod
    async def insert(cls, document: UserDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_raw_by_email(cls, email: str) -> dict[str, Any] | None:
        return await cls._collection.find_one({"email": email})

    @classmethod
    async def find_raw_by_id(cls, user_id: str) -> dict[str, Any] | None:
        return await cls._collection.find_one({"_id": ObjectId(user_id)})

    @classmethod
    async def find_by_email(cls, email: str) -> dict[str, Any] | None:
        document = await cls.find_raw_by_email(email)
        return serialize_document(document) if document else None

    @classmethod
    async def find_by_id(cls, user_id: str) -> dict[str, Any] | None:
        document = await cls.find_raw_by_id(user_id)
        return serialize_document(document) if document else None

    @classmethod
    async def find_many(
        cls, *, department_id: str | None = None
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {}
        if department_id:
            query["department_id"] = ObjectId(department_id)
        cursor = cls._collection.find(query).sort("name", 1)
        items = await cursor.to_list(length=1000)
        return [serialize_document(item) for item in items]

    @classmethod
    async def update(cls, user_id: str, data: dict[str, Any]) -> bool:
        if "department_id" in data:
            data["department_id"] = (
                ObjectId(data["department_id"]) if data["department_id"] else None
            )
        result = await cls._collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": data}
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, user_id: str) -> bool:
        result = await cls._collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
