import dataclasses
from bson import ObjectId

from app.base.base_document import AuditDocument


@dataclasses.dataclass(kw_only=True, frozen=True)
class DepartmentDocument(AuditDocument):
    company_id: ObjectId
    name: str
    description: str | None = None
    lead_id: ObjectId | None = None
    tags: list[str] = dataclasses.field(default_factory=list)
