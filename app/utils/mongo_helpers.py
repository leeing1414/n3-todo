import dataclasses
from typing import Any, TypeVar

from bson import ObjectId

TDocument = TypeVar("TDocument")


def to_object_id(value: str | ObjectId | None) -> ObjectId | None:
    if value is None:
        return None
    if isinstance(value, ObjectId):
        return value
    return ObjectId(value)


def document_asdict(document: Any) -> dict[str, Any]:
    data = dataclasses.asdict(document)
    data["_id"] = document._id
    return data


def _serialize_value(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize_value(val) for key, val in value.items()}
    return value


def serialize_document(document: dict[str, Any] | None) -> dict[str, Any] | None:
    if document is None:
        return None
    result = {key: _serialize_value(value) for key, value in document.items()}
    if "_id" in result:
        result["id"] = result.pop("_id")
    return result
