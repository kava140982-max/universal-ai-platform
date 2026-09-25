from fastapi import APIRouter, Depends, HTTPException
from universal_ai.api.schemas import RequestDTO, ResponseDTO
from universal_ai.api.deps import get_tenant_context
from universal_ai.domain.models import TenantContext
from universal_ai.application.orchestrator import Orchestrator
from universal_ai.domain.exceptions import UniversalAIError
from universal_ai.api.composition import get_orchestrator

router = APIRouter()

@router.get("/health")
async def health(): return {"status": "ok"}

@router.get("/ready")
async def ready(): return {"status": "ready"}
@router.get("/v1/modules")
async def get_modules(orchestrator: Orchestrator = Depends(get_orchestrator)):
    return [{"id": m.metadata.module_id, "name": m.metadata.name} for m in orchestrator.registry.list()]

@router.get("/v1/capabilities")
async def get_capabilities():
    from universal_ai.domain.models import Capability
    return [{"value": c.value} for c in Capability]

@router.post("/v1/request", response_model=ResponseDTO)
async def handle_request(dto: RequestDTO, ctx: TenantContext = Depends(get_tenant_context), orchestrator: Orchestrator = Depends(get_orchestrator)):
    try:
        # Pydantic v2 API
        result = await orchestrator.handle(ctx, dto.model_dump())
        return ResponseDTO(**result)
    except UniversalAIError as e:
        raise HTTPException(status_code=400, detail={"code": e.code, "message": e.message})
    except Exception:
        raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR", "message": "An internal error occurred"})