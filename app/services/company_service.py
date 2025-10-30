from app.collections.company_collection import CompanyCollection
from app.documents.company_document import CompanyDocument
from app.requests.company_request import CompanyCreateRequest, CompanyUpdateRequest
from app.schemas.models import CompanyDTO
from app.services import mappers


class CompanyService:
    @staticmethod
    async def create_company(request: CompanyCreateRequest, *, actor_id: str | None = None) -> CompanyDTO:
        document = CompanyDocument(
            name=request.name,
            description=request.description,
            domain=request.domain,
            tags=request.tags,
            created_by=actor_id,
            updated_by=actor_id,
        )
        inserted_id = await CompanyCollection.insert(document)
        created = await CompanyCollection.find_by_id(str(inserted_id))
        if not created:
            raise RuntimeError("Failed to load company after creation")
        return mappers.map_company(created)

    @staticmethod
    async def list_companies() -> list[CompanyDTO]:
        documents = await CompanyCollection.find_many()
        return [mappers.map_company(doc) for doc in documents]

    @staticmethod
    async def get_company(company_id: str) -> CompanyDTO | None:
        document = await CompanyCollection.find_by_id(company_id)
        return mappers.map_company(document) if document else None

    @staticmethod
    async def update_company(company_id: str, request: CompanyUpdateRequest, *, actor_id: str | None = None) -> bool:
        payload = request.model_dump(exclude_none=True)
        if not payload:
            return True
        if actor_id:
            payload["updated_by"] = actor_id
        return await CompanyCollection.update(company_id, payload)

    @staticmethod
    async def delete_company(company_id: str) -> bool:
        return await CompanyCollection.delete(company_id)
