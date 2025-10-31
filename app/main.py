from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.base.base_response import BaseResponse
from app.collections.activity_collection import ActivityCollection
from app.collections.company_collection import CompanyCollection
from app.collections.department_collection import DepartmentCollection
from app.collections.project_collection import ProjectCollection
from app.collections.subtask_collection import SubtaskCollection
from app.collections.task_collection import TaskCollection
from app.collections.user_collection import UserCollection
from app.core.settings import settings
from app.routers.activity_router import router as activity_router
from app.routers.auth_router import router as auth_router
from app.routers.company_router import router as company_router
from app.routers.department_router import router as department_router
from app.routers.health_router import router as health_router
from app.routers.project_router import router as project_router
from app.routers.subtask_router import router as subtask_router
from app.routers.task_router import router as task_router
from app.routers.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await CompanyCollection.create_indexes()
    await DepartmentCollection.create_indexes()
    await UserCollection.create_indexes()
    await ProjectCollection.create_indexes()
    await TaskCollection.create_indexes()
    await SubtaskCollection.create_indexes()
    await ActivityCollection.create_indexes()
    yield


app = FastAPI(title="N3 Todo Platform", version="1.0.0", lifespan=lifespan)

ALLOWED_CORS_ORIGINS = settings.CORS_ALLOW_ORIGINS or ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(department_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(subtask_router)
app.include_router(activity_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "N3 Todo platform API"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return a structured, user-friendly validation response."""
    field_labels = {
        "identifier": "아이디",
        "login_id": "아이디",
        "email": "이메일",
        "username": "아이디",
        "password": "비밀번호",
        "name": "이름",
        "department": "부서",
    }
    errors: list[dict[str, str]] = []
    for error in exc.errors():
        raw_path = [
            str(item)
            for item in error.get("loc", [])
            if item not in {"body", "query", "path"}
        ]
        field = raw_path[-1] if raw_path else "요청"
        label = field_labels.get(field, field)
        error_type = error.get("type", "")
        ctx = error.get("ctx") or {}
        message = error.get("msg", "잘못된 요청입니다.")

        if error_type == "string_too_short":
            limit = ctx.get("min_length") or ctx.get("limit_value")
            message = f"{limit}자 이상 입력해야 합니다."
        elif error_type == "string_too_long":
            limit = ctx.get("max_length") or ctx.get("limit_value")
            message = f"{limit}자 이하로 입력해야 합니다."
        elif error_type in {"missing", "value_error.missing"}:
            message = "필수 항목입니다."

        errors.append(
            {
                "field": field,
                "label": label,
                "message": message,
            }
        )

    primary_detail = (
        f"{errors[0]['label']} 항목 오류: {errors[0]['message']}" if errors else "잘못된 요청입니다."
    )
    response_body = BaseResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=primary_detail,
        data={"errors": errors} if errors else None,
    )
    return JSONResponse(content=response_body.model_dump(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
