from pydantic import BaseModel, Field

from app.base.base_response import BaseResponse


class TokenDTO(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer")
    expires_in: int = Field(..., description="Expiration in seconds")


class TokenResponse(BaseResponse[TokenDTO]):
    pass
