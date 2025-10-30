from fastapi import APIRouter, Query

from app.responses.project_response import ActivityListResponse
from app.services.activity_service import ActivityService

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("/recent", response_model=ActivityListResponse)
async def recent_activities(limit: int = Query(default=20, ge=1, le=100)) -> ActivityListResponse:
    activities = await ActivityService.recent(limit=limit)
    return ActivityListResponse(status_code=200, detail="Recent activities", data=activities)
