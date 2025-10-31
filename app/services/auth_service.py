from datetime import timedelta

from fastapi import HTTPException, status

from app.collections.user_collection import UserCollection
from app.documents.user_document import UserDocument
from app.requests.auth_request import LoginRequest, RegisterRequest
from app.responses.auth_response import TokenDTO
from app.schemas.enums import UserRole
from app.schemas.models import UserDTO
from app.services import mappers
from app.services.user_service import UserService
from app.utils.security import create_access_token, hash_password


class AuthService:
    @staticmethod
    async def login(request: LoginRequest) -> TokenDTO | None:
        user = await UserService.authenticate(request.identifier, request.password)
        if not user:
            return None
        expires = timedelta(minutes=60)
        token = create_access_token(
            subject=user.id,
            additional_claims={"role": user.role.value, "login_id": user.login_id},
            expires_delta=expires,
        )
        return TokenDTO(
            access_token=token,
            expires_in=int(expires.total_seconds()),
            user_id=user.id,
            nickname=user.name,
            department=user.department,
        )

    @staticmethod
    async def register(request: RegisterRequest) -> UserDTO:
        existing = await UserCollection.find_raw_by_login_id(request.identifier)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 아이디입니다.",
            )
        document = UserDocument(
            login_id=request.identifier,
            name=request.name,
            role=UserRole.member,
            department=request.department,
            password_hash=hash_password(request.password),
        )
        inserted_id = await UserCollection.insert(document)
        created = await UserCollection.find_by_id(str(inserted_id))
        if not created:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="사용자 정보를 불러오지 못했습니다.",
            )
        return mappers.map_user(created)
