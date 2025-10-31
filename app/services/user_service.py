from bson import ObjectId

from app.collections.user_collection import UserCollection
from app.documents.user_document import UserDocument
from app.requests.user_request import (
    UserCreateRequest,
    UserPasswordUpdateRequest,
    UserUpdateRequest,
)
from app.schemas.enums import UserRole
from app.schemas.models import UserDTO
from app.services import mappers
from app.utils.security import hash_password, verify_password


class UserService:
    @staticmethod
    async def create_user(request: UserCreateRequest, *, actor_id: str | None = None) -> UserDTO:
        document = UserDocument(
            login_id=request.login_id,
            name=request.name,
            role=UserRole(request.role),
            department_id=ObjectId(request.department_id)
            if request.department_id
            else None,
            title=request.title,
            phone=request.phone,
            avatar_url=request.avatar_url,
            department=None,
            timezone=request.timezone,
            password_hash=hash_password(request.password),
            created_by=actor_id,
            updated_by=actor_id,
        )
        inserted_id = await UserCollection.insert(document)
        created = await UserCollection.find_by_id(str(inserted_id))
        if not created:
            raise RuntimeError("Failed to load user after creation")
        return mappers.map_user(created)

    @staticmethod
    async def list_users(*, department_id: str | None = None) -> list[UserDTO]:
        documents = await UserCollection.find_many(department_id=department_id)
        return [mappers.map_user(doc) for doc in documents]

    @staticmethod
    async def get_user(user_id: str) -> UserDTO | None:
        document = await UserCollection.find_by_id(user_id)
        return mappers.map_user(document) if document else None

    @staticmethod
    async def update_user(
        user_id: str, request: UserUpdateRequest, *, actor_id: str | None = None
    ) -> bool:
        payload = request.model_dump(exclude_none=True)
        if actor_id:
            payload["updated_by"] = actor_id
        return await UserCollection.update(user_id, payload)

    @staticmethod
    async def update_password(user_id: str, request: UserPasswordUpdateRequest) -> bool:
        password_hash = hash_password(request.password)
        return await UserCollection.update(user_id, {"password_hash": password_hash})

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        return await UserCollection.delete(user_id)

    @staticmethod
    async def authenticate(login_id: str, password: str) -> UserDTO | None:
        raw_user = await UserCollection.find_raw_by_login_id(login_id)
        if not raw_user:
            return None
        password_hash = raw_user.get("password_hash")
        if not password_hash or not verify_password(password, password_hash):
            return None
        sanitized = await UserCollection.find_by_id(str(raw_user["_id"]))
        return mappers.map_user(sanitized) if sanitized else None
