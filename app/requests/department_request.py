from pydantic import BaseModel, Field


class DepartmentCreateRequest(BaseModel):
    company_id: str = Field(..., description="Owning company identifier")
    name: str = Field(..., description="Department name")
    description: str | None = None
    lead_id: str | None = Field(default=None, description="Department lead user id")
    tags: list[str] = Field(default_factory=list)


class DepartmentUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    lead_id: str | None = None
    tags: list[str] | None = None
