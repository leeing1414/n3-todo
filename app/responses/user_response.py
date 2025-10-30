from typing import List

from app.base.base_response import BaseResponse
from app.schemas.models import UserDTO


class UserResponse(BaseResponse[UserDTO]):
    pass


class UserListResponse(BaseResponse[List[UserDTO]]):
    pass
