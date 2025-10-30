from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.base.base_response import BaseResponse
from app.dependencies.auth import get_current_user
from app.requests.company_request import CompanyCreateRequest, CompanyUpdateRequest
from app.responses.company_response import CompanyListResponse, CompanyResponse
from app.schemas.models import UserDTO
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    request: CompanyCreateRequest,
    current_user: UserDTO = Depends(get_current_user),
) -> CompanyResponse:
    company = await CompanyService.create_company(request, actor_id=current_user.id)
    return CompanyResponse(status_code=status.HTTP_201_CREATED, detail="Company created", data=company)


@router.get("", response_model=CompanyListResponse)
async def list_companies() -> CompanyListResponse:
    companies = await CompanyService.list_companies()
    return CompanyListResponse(status_code=status.HTTP_200_OK, detail="Company list", data=companies)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: str = Path(...)) -> CompanyResponse:
    company = await CompanyService.get_company(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return CompanyResponse(status_code=status.HTTP_200_OK, detail="Company detail", data=company)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    request: CompanyUpdateRequest,
    company_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> CompanyResponse:
    success = await CompanyService.update_company(company_id, request, actor_id=current_user.id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    company = await CompanyService.get_company(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return CompanyResponse(status_code=status.HTTP_200_OK, detail="Company updated", data=company)


@router.delete("/{company_id}")
async def delete_company(
    company_id: str = Path(...),
    current_user: UserDTO = Depends(get_current_user),
) -> BaseResponse[dict[str, bool]]:
    success = await CompanyService.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return BaseResponse(status_code=status.HTTP_200_OK, detail="Company deleted", data={"deleted": True})
