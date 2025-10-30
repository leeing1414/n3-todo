from typing import List

from app.base.base_response import BaseResponse
from app.schemas.models import ActivityDTO, ProjectDTO, TaskDTO


class ProjectResponse(BaseResponse[ProjectDTO]):
    pass


class ProjectListResponse(BaseResponse[List[ProjectDTO]]):
    pass


class ProjectWithTasksResponse(BaseResponse[dict]):
    pass


class ActivityListResponse(BaseResponse[List[ActivityDTO]]):
    pass


class TaskListResponse(BaseResponse[List[TaskDTO]]):
    pass
