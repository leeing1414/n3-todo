from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    role: str = Field(default="member")
    department_id: str | None = None
    title: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    timezone: str | None = Field(default="Asia/Seoul")
    password: str = Field(..., min_length=8)


class UserUpdateRequest(BaseModel):
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
