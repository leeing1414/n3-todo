from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    login_id: str = Field(..., min_length=1)
    name: str
    role: str = Field(default="member")
    department_id: str | None = None
    title: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    timezone: str | None = Field(default="Asia/Seoul")
    password: str = Field(..., min_length=8)


class UserUpdateRequest(BaseModel):
    login_id: str | None = None
    name: str | None = None
    role: str | None = None
    department_id: str | None = None
    title: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    is_active: bool | None = None


class UserPasswordUpdateRequest(BaseModel):
    password: str = Field(..., min_length=8)
