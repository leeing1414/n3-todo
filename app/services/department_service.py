from bson import ObjectId

from app.collections.department_collection import DepartmentCollection
from app.documents.department_document import DepartmentDocument
from app.requests.department_request import (
    DepartmentCreateRequest,
    DepartmentUpdateRequest,
)
from app.schemas.models import DepartmentDTO
from app.services import mappers


class DepartmentService:
    @staticmethod
    async def create_department(
        request: DepartmentCreateRequest, *, actor_id: str | None = None
    ) -> DepartmentDTO:
        document = DepartmentDocument(
            company_id=ObjectId(request.company_id),
            name=request.name,
            description=request.description,
            lead_id=ObjectId(request.lead_id) if request.lead_id else None,
            tags=request.tags,
            created_by=actor_id,
            updated_by=actor_id,
        )
        inserted_id = await DepartmentCollection.insert(document)
        created = await DepartmentCollection.find_by_id(str(inserted_id))
        if not created:
            raise RuntimeError("Failed to load department after creation")
        return mappers.map_department(created)

    @staticmethod
    async def list_departments(*, company_id: str | None = None) -> list[DepartmentDTO]:
        if company_id:
            documents = await DepartmentCollection.find_by_company(company_id)
        else:
            documents = await DepartmentCollection.find_all()
        return [mappers.map_department(doc) for doc in documents]

    @staticmethod
    async def get_department(department_id: str) -> DepartmentDTO | None:
        document = await DepartmentCollection.find_by_id(department_id)
        return mappers.map_department(document) if document else None

    @staticmethod
    async def update_department(
        department_id: str, request: DepartmentUpdateRequest, *, actor_id: str | None = None
    ) -> bool:
        payload = request.model_dump(exclude_none=True)
        if actor_id:
            payload["updated_by"] = actor_id
        return await DepartmentCollection.update(department_id, payload)

    @staticmethod
    async def delete_department(department_id: str) -> bool:
        return await DepartmentCollection.delete(department_id)
