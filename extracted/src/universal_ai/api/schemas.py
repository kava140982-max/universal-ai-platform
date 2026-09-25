from pydantic import BaseModel, Field
from typing import Any, Optional
from universal_ai.domain.models import Usage, AIProvenance, DecisionTrace

class RequestDTO(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    target_module: Optional[str] = "echo_module"
    allowed_tools: list[str] = Field(default_factory=list)

class ResponseDTO(BaseModel):
    request_id: str
    tenant_id: str
    thread_id: str
    payload: dict[str, Any]
    usage: Usage
    provenance: AIProvenance
    decision_trace: DecisionTrace
    metadata: dict[str, Any]