from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from app.base.base_response import BaseResponse
from app.db.mongo_db import db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", tags=["Health"])
async def health_check() -> BaseResponse[dict[str, str]]:
    return BaseResponse(status_code=HTTP_200_OK, detail="Service OK", data={"status": "healthy"})


@router.get("/db", tags=["Health"])
async def health_check_db() -> BaseResponse[dict[str, str]]:
    try:
        await db.command("ping")
        return BaseResponse(status_code=HTTP_200_OK, detail="Database reachable", data={"status": "healthy"})
    except Exception as exc:  # pragma: no cover - diagnostic path
        return BaseResponse(status_code=500, detail="Database unreachable", data={"error": str(exc)})
