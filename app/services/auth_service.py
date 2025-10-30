from datetime import timedelta

from app.requests.auth_request import LoginRequest
from app.responses.auth_response import TokenDTO
from app.services.user_service import UserService
from app.utils.security import create_access_token


class AuthService:
    @staticmethod
    async def login(request: LoginRequest) -> TokenDTO | None:
        user = await UserService.authenticate(request.email, request.password)
        if not user:
            return None
        expires = timedelta(minutes=60)
        token = create_access_token(
            subject=user.id,
            additional_claims={"role": user.role.value, "email": user.email},
            expires_delta=expires,
        )
        return TokenDTO(access_token=token, expires_in=int(expires.total_seconds()))
