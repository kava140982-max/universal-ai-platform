from typing import Set
from universal_ai.interfaces.policies import PolicyEngine
from universal_ai.domain.models import TenantContext, Capability, PolicyDecision

class DefaultDenyPolicyEngine(PolicyEngine):
    async def evaluate(self, ctx: TenantContext, required_capabilities: Set[Capability]) -> PolicyDecision:
        missing = required_capabilities - ctx.permissions
        if missing:
            return PolicyDecision(False, f"Missing permissions for: {', '.join(c.value for c in missing)}", frozenset(required_capabilities))
        return PolicyDecision(True, "All capabilities granted", frozenset(required_capabilities))