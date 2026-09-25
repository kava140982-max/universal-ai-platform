from typing import Protocol, runtime_checkable
from dataclasses import dataclass
from universal_ai.domain.models import TenantContext, Capability

@dataclass(frozen=True)
class RouterDecision:
    request_id: str
    selected_module: str
    confidence: float
    alternatives: list[str]
    matched_capabilities: list[Capability]
    routing_reason: str

@runtime_checkable
class Router(Protocol):
    async def route(self, ctx: TenantContext, payload: dict) -> RouterDecision: ...