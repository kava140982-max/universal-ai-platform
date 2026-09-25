from universal_ai.application.orchestrator import Orchestrator
from universal_ai.application.module_registry import ModuleRegistry
from universal_ai.application.router_service import RuleBasedRouter
from universal_ai.application.policy_service import DefaultDenyPolicyEngine
from universal_ai.infrastructure.audit.in_memory import InMemoryAuditService
from universal_ai.modules.echo import EchoModule

_registry = ModuleRegistry()
_registry.register(EchoModule())
_audit_service = InMemoryAuditService()
_policy_engine = DefaultDenyPolicyEngine()
_router_service = RuleBasedRouter(_registry)

orchestrator_instance = Orchestrator(_router_service, _registry, _policy_engine, _audit_service)

def get_orchestrator() -> Orchestrator:
    return orchestrator_instance