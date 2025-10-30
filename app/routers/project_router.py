from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.base.base_response import BaseResponse
from app.dependencies.auth import get_current_user
from app.requests.project_request import ProjectCreateRequest, ProjectUpdateRequest
from app.responses.dashboard_response import DashboardResponse
from app.responses.project_response import (
    ProjectListResponse,
    ProjectResponse,
    ProjectWithTasksResponse,
    TaskListResponse,
)
from app.schemas.models import UserDTO
from app.services.dashboard_service import DashboardService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: ProjectCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> ProjectResponse:
    project = await ProjectService.create_project(request, actor_id=current_user.id)
    return ProjectResponse(status_code=status.HTTP_201_CREATED, detail="Project created", data=project)


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    department_id: str | None = Query(default=None),
    statuses: list[str] | None = Query(default=None),
) -> ProjectListResponse:
    projects = await ProjectService.list_projects(department_id=department_id, statuses=statuses)
    return ProjectListResponse(status_code=status.HTTP_200_OK, detail="Project list", data=projects)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str = Path(...)) -> ProjectResponse:
    project = await ProjectService.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectResponse(status_code=status.HTTP_200_OK, detail="Project detail", data=project)


@router.get("/{project_id}/full", response_model=ProjectWithTasksResponse)
async def get_project_full(project_id: str = Path(...)) -> ProjectWithTasksResponse:
    detail = await ProjectService.get_project_detail(project_id)
    return ProjectWithTasksResponse(status_code=status.HTTP_200_OK, detail="Project full detail", data=detail)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    request: ProjectUpdateRequest,
    project_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> ProjectResponse:
    success = await ProjectService.update_project(project_id, request, actor_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    project = await ProjectService.get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectResponse(status_code=status.HTTP_200_OK, detail="Project updated", data=project)


@router.delete("/{project_id}")
async def delete_project(
    project_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await ProjectService.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Project deleted", data={"deleted": True})


@router.get("/{project_id}/tasks", response_model=TaskListResponse)
async def list_project_tasks(project_id: str = Path(...)) -> TaskListResponse:
    tasks = await TaskService.list_tasks(project_id)
    return TaskListResponse(status_code=status.HTTP_200_OK, detail="Project tasks", data=tasks)


@router.get("/{project_id}/stats")
async def project_stats(project_id: str = Path(...)) -> BaseResponse[dict]:
    stats = await TaskService.stats(project_id)
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Project stats", data=stats)


@router.get("/dashboard/summary", response_model=DashboardResponse)
async def dashboard_summary() -> DashboardResponse:
    summary = await DashboardService.get_summary()
    return DashboardResponse(status_code=status.HTTP_200_OK, detail="Dashboard summary", data=summary)
