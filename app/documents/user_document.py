import dataclasses

from bson import ObjectId

from app.base.base_document import AuditDocument
from app.schemas.enums import UserRole


@dataclasses.dataclass(kw_only=True, frozen=True)
class UserDocument(AuditDocument):
    email: str
    name: str
    role: UserRole
    department_id: ObjectId | None = None
    title: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool = True
    timezone: str | None = "Asia/Seoul"
    password_hash: str | None = None
