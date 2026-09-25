import pytest
from universal_ai.domain.models import TenantContext, Capability
from universal_ai.application.orchestrator import Orchestrator
from universal_ai.application.module_registry import ModuleRegistry
from universal_ai.application.router_service import RuleBasedRouter
from universal_ai.application.policy_service import DefaultDenyPolicyEngine
from universal_ai.infrastructure.audit.in_memory import InMemoryAuditService
from universal_ai.modules.echo import EchoModule
from universal_ai.domain.exceptions import PolicyError

@pytest.fixture
def orchestrator():
    reg = ModuleRegistry()
    reg.register(EchoModule())
    return Orchestrator(RuleBasedRouter(reg), reg, DefaultDenyPolicyEngine(), InMemoryAuditService())

@pytest.mark.asyncio
async def test_tenant_context_propagation(orchestrator):
    ctx = TenantContext("tenant_a", "user_1", "t1", "r1", "c1", frozenset())
    res = await orchestrator.handle(ctx, {"message": "hello", "target_module": "echo_module"})
    assert res["tenant_id"] == "tenant_a"
    assert res["payload"]["echo"] == "hello"

@pytest.mark.asyncio
async def test_policy_denies_missing_capabilities(orchestrator):
    class FakeCode:
        @property
        def metadata(self):
            from universal_ai.domain.models import ModuleMetadata
            return ModuleMetadata("code_mod", "Code", "1.0", "", frozenset({Capability.CODE_EXECUTION}))
        def required_capabilities(self): return {Capability.CODE_EXECUTION}
        async def execute(self, ctx, payload): return {}
        async def health_check(self): return True
    orchestrator.registry.register(FakeCode())
    ctx = TenantContext("tenant_b", "user_2", "t2", "r2", "c2", frozenset())
    with pytest.raises(PolicyError) as exc:        await orchestrator.handle(ctx, {"message": "run", "target_module": "code_mod"})
    assert "Missing permissions" in str(exc.value)