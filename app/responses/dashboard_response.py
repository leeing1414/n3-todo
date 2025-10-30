from app.base.base_response import BaseResponse
from app.schemas.models import DashboardSummaryDTO


class DashboardResponse(BaseResponse[DashboardSummaryDTO]):
    pass
