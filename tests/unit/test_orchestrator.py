import pytest
from universal_ai.domain.models import TenantContext
from universal_ai.application.orchestrator import Orchestrator
from universal_ai.application.module_registry import ModuleRegistry
from universal_ai.application.router_service import RuleBasedRouter
from universal_ai.application.policy_service import DefaultDenyPolicyEngine
from universal_ai.infrastructure.audit.in_memory import InMemoryAuditService
from universal_ai.modules.echo import EchoModule

@pytest.fixture
def orch():
    reg = ModuleRegistry()
    reg.register(EchoModule())
    return Orchestrator(RuleBasedRouter(reg), reg, DefaultDenyPolicyEngine(), InMemoryAuditService())

@pytest.mark.asyncio
async def test_echo_end_to_end(orch):
    ctx = TenantContext("t1", "s1", "th1", "req1", "cor1", frozenset())
    res = await orch.handle(ctx, {"message": "test_payload", "target_module": "echo_module"})
    assert res["request_id"] == "req1"
    assert res["tenant_id"] == "t1"
    assert res["payload"]["echo"] == "test_payload"
    assert res["provenance"].generated is False # Echo is non-generative
    assert "audited" in res["decision_trace"].execution_steps