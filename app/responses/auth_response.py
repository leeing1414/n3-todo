from pydantic import BaseModel, Field

from app.base.base_response import BaseResponse


class TokenDTO(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer")
    expires_in: int = Field(..., description="Expiration in seconds")
    user_id: str = Field(..., description="Identifier of the authenticated user")
    nickname: str = Field(..., description="Display name of the authenticated user")
    department: str | None = Field(
        default=None, description="Department label of the authenticated user"
    )


class TokenResponse(BaseResponse[TokenDTO]):
    pass
