from typing import List

from app.base.base_response import BaseResponse
from app.schemas.models import DepartmentDTO


class DepartmentResponse(BaseResponse[DepartmentDTO]):
    pass


class DepartmentListResponse(BaseResponse[List[DepartmentDTO]]):
    pass
