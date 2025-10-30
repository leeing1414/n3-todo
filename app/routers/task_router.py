from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.base.base_response import BaseResponse
from app.dependencies.auth import get_current_user
from app.requests.task_request import TaskCreateRequest, TaskUpdateRequest
from app.responses.task_response import TaskListResponse, TaskResponse
from app.schemas.models import UserDTO
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> TaskResponse:
    task = await TaskService.create_task(request, actor_id=current_user.id)
    return TaskResponse(status_code=status.HTTP_201_CREATED, detail="Task created", data=task)


@router.get("/calendar", response_model=TaskListResponse)
async def calendar_tasks(
    start: datetime = Query(...),
    end: datetime = Query(...),
) -> TaskListResponse:
    tasks = await TaskService.calendar(start, end)
    return TaskListResponse(status_code=status.HTTP_200_OK, detail="Calendar tasks", data=tasks)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str = Path(...)) -> TaskResponse:
    task = await TaskService.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse(status_code=status.HTTP_200_OK, detail="Task detail", data=task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    request: TaskUpdateRequest,
    task_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> TaskResponse:
    success = await TaskService.update_task(task_id, request, actor_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task = await TaskService.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse(status_code=status.HTTP_200_OK, detail="Task updated", data=task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await TaskService.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Task deleted", data={"deleted": True})
