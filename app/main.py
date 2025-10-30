from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.collections.activity_collection import ActivityCollection
from app.collections.company_collection import CompanyCollection
from app.collections.department_collection import DepartmentCollection
from app.collections.project_collection import ProjectCollection
from app.collections.subtask_collection import SubtaskCollection
from app.collections.task_collection import TaskCollection
from app.collections.user_collection import UserCollection
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
