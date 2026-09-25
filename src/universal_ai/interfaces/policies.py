from typing import Protocol, runtime_checkable, Set
from universal_ai.domain.models import TenantContext, Capability, PolicyDecision

@runtime_checkable
class PolicyEngine(Protocol):
    async def evaluate(self, ctx: TenantContext, required_capabilities: Set[Capability]) -> PolicyDecision: ...