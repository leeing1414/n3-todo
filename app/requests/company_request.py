from pydantic import BaseModel, Field


class CompanyCreateRequest(BaseModel):
    name: str = Field(..., description="Company name")
    description: str | None = Field(default=None, description="Short summary")
    domain: str | None = Field(default=None, description="Primary email / service domain")
    tags: list[str] = Field(default_factory=list, description="Optional labels for filtering")


class CompanyUpdateRequest(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    domain: str | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
