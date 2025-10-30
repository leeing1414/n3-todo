from dataclasses import asdict
from typing import Any

from bson import ObjectId

from app.db.mongo_db import db
from app.documents.company_document import CompanyDocument
from app.utils.mongo_helpers import serialize_document


class CompanyCollection:
    _collection = db["companies"]

    @classmethod
    async def create_indexes(cls) -> None:
        await cls._collection.create_index("name", unique=True)

    @classmethod
    async def insert(cls, document: CompanyDocument) -> ObjectId:
        payload = asdict(document)
        result = await cls._collection.insert_one(payload)
        return result.inserted_id

    @classmethod
    async def find_by_id(cls, company_id: str) -> dict[str, Any] | None:
        document = await cls._collection.find_one({"_id": ObjectId(company_id)})
        return serialize_document(document) if document else None

    @classmethod
    async def find_many(cls) -> list[dict[str, Any]]:
        cursor = cls._collection.find().sort("created_at", -1)
        items = await cursor.to_list(length=500)
        return [serialize_document(item) for item in items]

    @classmethod
    async def update(cls, company_id: str, data: dict[str, Any]) -> bool:
        result = await cls._collection.update_one({"_id": ObjectId(company_id)}, {"$set": data})
        return result.modified_count > 0

    @classmethod
    async def delete(cls, company_id: str) -> bool:
        result = await cls._collection.delete_one({"_id": ObjectId(company_id)})
        return result.deleted_count > 0
