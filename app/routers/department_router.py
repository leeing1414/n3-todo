from fastapi import APIRouter, Depends, HTTPException, Query, Path, status

from app.base.base_response import BaseResponse
from app.dependencies.auth import get_current_user
from app.requests.department_request import (
    DepartmentCreateRequest,
    DepartmentUpdateRequest,
)
from app.responses.department_response import (
    DepartmentListResponse,
    DepartmentResponse,
)
from app.schemas.models import UserDTO
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    request: DepartmentCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> DepartmentResponse:
    department = await DepartmentService.create_department(request, actor_id=current_user.id)
    return DepartmentResponse(status_code=status.HTTP_201_CREATED, detail="Department created", data=department)


@router.get("", response_model=DepartmentListResponse)
async def list_departments(company_id: str | None = Query(default=None)) -> DepartmentListResponse:
    departments = await DepartmentService.list_departments(company_id=company_id)
    return DepartmentListResponse(status_code=status.HTTP_200_OK, detail="Department list", data=departments)


@router.patch("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    request: DepartmentUpdateRequest,
    department_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> DepartmentResponse:
    success = await DepartmentService.update_department(department_id, request, actor_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    department = await DepartmentService.get_department(department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return DepartmentResponse(status_code=status.HTTP_200_OK, detail="Department updated", data=department)


@router.delete("/{department_id}")
async def delete_department(
    department_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await DepartmentService.delete_department(department_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Department deleted", data={"deleted": True})
