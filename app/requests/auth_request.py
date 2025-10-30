from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User sign-in email")
    password: str = Field(..., description="User password", min_length=8)
