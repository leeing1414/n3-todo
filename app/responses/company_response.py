from typing import List

from app.base.base_response import BaseResponse
from app.schemas.models import CompanyDTO


class CompanyResponse(BaseResponse[CompanyDTO]):
    """Response envelope for a single company"""

    pass


class CompanyListResponse(BaseResponse[List[CompanyDTO]]):
    """Response envelope for company collections"""

    pass
