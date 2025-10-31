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
        existing_indexes = await cls._collection.index_information()
        if "email_1" in existing_indexes:
            await cls._collection.drop_index("email_1")
        await cls._collection.create_index("login_id", unique=True, sparse=True)
        await cls._collection.create_index("department_id")

    @classmethod
    async def insert(cls, document: UserDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_raw_by_login_id(cls, login_id: str) -> dict[str, Any] | None:
        query = {"$or": [{"login_id": login_id}, {"email": login_id}]}
        return await cls._collection.find_one(query)

    @classmethod
    async def find_raw_by_id(cls, user_id: str) -> dict[str, Any] | None:
        return await cls._collection.find_one({"_id": ObjectId(user_id)})

    @classmethod
    @staticmethod
    def _normalize(document: dict[str, Any] | None) -> dict[str, Any] | None:
        if document is None:
            return None
        normalized = document.copy()
        login_id = normalized.get("login_id") or normalized.get("email")
        if login_id is not None:
            normalized["login_id"] = login_id
        normalized.pop("email", None)
        return normalized

    @classmethod
    async def find_by_login_id(cls, login_id: str) -> dict[str, Any] | None:
        document = await cls.find_raw_by_login_id(login_id)
        normalized = cls._normalize(document)
        return serialize_document(normalized) if normalized else None

    @classmethod
    async def find_by_id(cls, user_id: str) -> dict[str, Any] | None:
        document = await cls.find_raw_by_id(user_id)
        normalized = cls._normalize(document)
        return serialize_document(normalized) if normalized else None

    @classmethod
    async def find_many(
        cls, *, department_id: str | None = None
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {}
        if department_id:
            query["department_id"] = ObjectId(department_id)
        cursor = cls._collection.find(query).sort("name", 1)
        items = await cursor.to_list(length=1000)
        results: list[dict[str, Any]] = []
        for item in items:
            normalized = cls._normalize(item)
            if not normalized:
                continue
            serialized = serialize_document(normalized)
            if serialized:
                results.append(serialized)
        return results

    @classmethod
    async def update(cls, user_id: str, data: dict[str, Any]) -> bool:
        data = data.copy()
        if "email" in data and "login_id" not in data:
            data["login_id"] = data.pop("email")
        else:
            data.pop("email", None)
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
