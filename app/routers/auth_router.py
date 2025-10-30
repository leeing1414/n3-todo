from fastapi import APIRouter, HTTPException, status

from app.requests.auth_request import LoginRequest
from app.responses.auth_response import TokenDTO, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    token = await AuthService.login(request)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(status_code=status.HTTP_200_OK, detail="Login successful", data=token)
