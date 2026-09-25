from typing import List
from universal_ai.interfaces.router import Router, RouterDecision
from universal_ai.domain.models import TenantContext, Capabilityfrom universal_ai.application.module_registry import ModuleRegistry
from universal_ai.domain.exceptions import RoutingError

class RuleBasedRouter(Router):
    def __init__(self, registry: ModuleRegistry):
        self.registry, self.version = registry, "1.0.0"
    async def route(self, ctx: TenantContext, payload: dict) -> RouterDecision:
        target = payload.get("target_module", "echo_module")
        candidates = [m.metadata.module_id for m in self.registry.list()]
        if target not in candidates:
            raise RoutingError(f"Target module {target} not available")
        module = self.registry.get(target)
        return RouterDecision(
            request_id=ctx.request_id, selected_module=target, confidence=1.0,
            alternatives=[c for c in candidates if c != target],
            matched_capabilities=list(module.required_capabilities()),
            routing_reason="Deterministic rule-based routing"
        )