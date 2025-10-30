from typing import List

from app.base.base_response import BaseResponse
from app.schemas.models import SubtaskDTO, TaskDTO


class TaskResponse(BaseResponse[TaskDTO]):
    pass


class TaskListResponse(BaseResponse[List[TaskDTO]]):
    pass


class SubtaskListResponse(BaseResponse[List[SubtaskDTO]]):
    pass
