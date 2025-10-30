from fastapi import APIRouter, HTTPException, status

from app.requests.auth_request import LoginRequest, RegisterRequest
from app.responses.auth_response import TokenResponse
from app.responses.user_response import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    token = await AuthService.login(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return TokenResponse(
        status_code=status.HTTP_200_OK,
        detail="Login successful",
        data=token,
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(request: RegisterRequest) -> UserResponse:
    user = await AuthService.register(request)
    return UserResponse(
        status_code=status.HTTP_201_CREATED,
        detail="User registered successfully",
        data=user,
    )
