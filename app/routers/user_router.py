from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.base.base_response import BaseResponse
from app.dependencies.auth import get_current_user
from app.requests.user_request import (
    UserCreateRequest,
    UserPasswordUpdateRequest,
    UserUpdateRequest,
)
from app.responses.user_response import UserListResponse, UserResponse
from app.schemas.models import UserDTO
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> UserResponse:
    user = await UserService.create_user(request, actor_id=current_user.id)
    return UserResponse(status_code=status.HTTP_201_CREATED, detail="User created", data=user)


@router.get("", response_model=UserListResponse)
async def list_users(department_id: str | None = Query(default=None)) -> UserListResponse:
    users = await UserService.list_users(department_id=department_id)
    return UserListResponse(status_code=status.HTTP_200_OK, detail="User list", data=users)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserDTO = Depends(get_current_user)) -> UserResponse:
    return UserResponse(status_code=status.HTTP_200_OK, detail="Current user", data=current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str = Path(...)) -> UserResponse:
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(status_code=status.HTTP_200_OK, detail="User detail", data=user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    request: UserUpdateRequest,
    user_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> UserResponse:
    success = await UserService.update_user(user_id, request, actor_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(status_code=status.HTTP_200_OK, detail="User updated", data=user)


@router.patch("/{user_id}/password")
async def update_user_password(
    request: UserPasswordUpdateRequest,
    user_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await UserService.update_password(user_id, request)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Password updated", data={"updated": True})


@router.delete("/{user_id}")
async def delete_user(
    user_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="User deleted", data={"deleted": True})
