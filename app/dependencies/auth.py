from fastapi import Depends, Header, HTTPException, status

from app.schemas.models import UserDTO
from app.services.user_service import UserService
from app.utils.security import decode_access_token


async def get_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return authorization.split(" ", 1)[1]


async def get_current_user(token: str = Depends(get_bearer_token)) -> UserDTO:
    try:
        payload = decode_access_token(token)
    except Exception as exc:  # pragma: no cover - external validation
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
