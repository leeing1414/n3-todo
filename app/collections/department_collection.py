from dataclasses import asdict
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.department_document import DepartmentDocument
from app.utils.mongo_helpers import serialize_document


class DepartmentCollection:
    _collection = db["departments"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index(
            [("company_id", 1), ("name", 1)], unique=True
        )

    @classmethod
    async def insert(cls, document: DepartmentDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_by_id(cls, department_id: str) -> dict[str, Any] | None:
        document = await cls._collection.find_one({"_id": ObjectId(department_id)})
        return serialize_document(document)

    @classmethod
    async def find_by_company(cls, company_id: str) -> list[dict[str, Any]]:
        cursor = (
            cls._collection.find({"company_id": ObjectId(company_id)})
            .sort("name", 1)
        )
        items = await cursor.to_list(length=500)
        return [serialize_document(item) for item in items]

    @classmethod
    async def find_all(cls) -> list[dict[str, Any]]:
        cursor = cls._collection.find().sort("name", 1)
        items = await cursor.to_list(length=1000)
        return [serialize_document(item) for item in items]

    @classmethod
    async def update(cls, department_id: str, data: dict[str, Any]) -> bool:
        if "lead_id" in data:
            data["lead_id"] = ObjectId(data["lead_id"]) if data["lead_id"] else None
        result = await cls._collection.update_one(
            {"_id": ObjectId(department_id)}, {"$set": data}
        )
        return result.modified_count > 0

    @classmethod
    async def delete(cls, department_id: str) -> bool:
        result = await cls._collection.delete_one({"_id": ObjectId(department_id)})
        return result.deleted_count > 0
