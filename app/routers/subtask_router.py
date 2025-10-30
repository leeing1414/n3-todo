from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from app.base.base_response import BaseResponse
from app.dependencies.auth import get_current_user
from app.requests.subtask_request import SubtaskCreateRequest, SubtaskUpdateRequest
from app.responses.subtask_response import SubtaskResponse
from app.responses.task_response import SubtaskListResponse
from app.schemas.models import UserDTO
from app.services.subtask_service import SubtaskService

router = APIRouter(prefix="/subtasks", tags=["Subtasks"])


@router.post("", response_model=SubtaskResponse, status_code=status.HTTP_201_CREATED)
async def create_subtask(
    request: SubtaskCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> SubtaskResponse:
    subtask = await SubtaskService.create_subtask(request, actor_id=current_user.id)
    return SubtaskResponse(status_code=status.HTTP_201_CREATED, detail="Subtask created", data=subtask)


@router.get("/task/{task_id}", response_model=SubtaskListResponse)
async def list_subtasks(task_id: str = Path(...)) -> SubtaskListResponse:
    subtasks = await SubtaskService.list_subtasks(task_id)
    return SubtaskListResponse(status_code=status.HTTP_200_OK, detail="Subtask list", data=subtasks)


@router.patch("/{subtask_id}", response_model=SubtaskResponse)
async def update_subtask(
    request: SubtaskUpdateRequest,
    subtask_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> SubtaskResponse:
    success = await SubtaskService.update_subtask(subtask_id, request, actor_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtask not found")
    subtask = await SubtaskService.get_subtask(subtask_id)
    if not subtask:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtask not found")
    return SubtaskResponse(status_code=status.HTTP_200_OK, detail="Subtask updated", data=subtask)


@router.delete("/{subtask_id}")
async def delete_subtask(
    subtask_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await SubtaskService.delete_subtask(subtask_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtask not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Subtask deleted", data={"deleted": True})


@router.post("/{task_id}/reorder")
async def reorder_subtasks(
    task_id: str = Path(...),
    ordered_ids: List[str] = Body(..., embed=True, description="Ordered list of subtask ids"),
) -> BaseResponse[dict[str, bool]]:
    await SubtaskService.reorder(task_id, ordered_ids)
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Subtasks reordered", data={"reordered": True})
