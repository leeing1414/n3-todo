import dataclasses

from app.base.base_document import AuditDocument


@dataclasses.dataclass(kw_only=True, frozen=True)
class CompanyDocument(AuditDocument):
    name: str
    description: str | None = None
    domain: str | None = None
    tags: list[str] = dataclasses.field(default_factory=list)
