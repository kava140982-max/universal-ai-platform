import uuid, hashlib, json
from datetime import datetime, timezone
from typing import Dict, Any, Set
from universal_ai.domain.models import TenantContext, ExecutionContext, Usage, DecisionTrace, AIProvenance, AuditEvent, Capability
from universal_ai.domain.exceptions import PolicyError
from universal_ai.interfaces.router import Router
from universal_ai.interfaces.policies import PolicyEngine
from universal_ai.interfaces.audit import AuditService
from universal_ai.application.module_registry import ModuleRegistry

class Orchestrator:
    def __init__(self, router: Router, registry: ModuleRegistry, policy_engine: PolicyEngine, audit_service: AuditService):
        self.router, self.registry, self.policy_engine, self.audit_service = router, registry, policy_engine, audit_service

    async def handle(self, ctx: TenantContext, payload: Dict[str, Any]) -> Dict[str, Any]:
        trace = DecisionTrace(self.router.__class__.__name__, getattr(self.router, 'version', 'unknown'), "", [], [], [], [], {"start": datetime.now(timezone.utc)})
        try:
            decision = await self.router.route(ctx, payload)
            trace.selected_module, trace.candidate_modules, trace.matched_capabilities = decision.selected_module, decision.alternatives + [decision.selected_module], decision.matched_capabilities
            trace.execution_steps.append("routed")            
            module = self.registry.get(decision.selected_module)
            required_caps: Set[Capability] = set(module.required_capabilities())
            policy_decision = await self.policy_engine.evaluate(ctx, required_caps)
            trace.policy_decisions.append(policy_decision)
            trace.execution_steps.append("policy_evaluated")
            if not policy_decision.allowed: raise PolicyError(policy_decision.reason)

            # SECURITY: Intersection ensures ONLY granted capabilities are passed to execution context
            granted_caps = required_caps.intersection(ctx.permissions)
            exec_ctx = ExecutionContext(ctx, frozenset(granted_caps), frozenset(), 10, 5, 30.0, False)
            
            trace.execution_steps.append("executing_module")
            result = await module.execute(exec_ctx, payload)
            trace.execution_steps.append("module_executed")

            is_generative = module.metadata.module_id not in ["echo_module"]
            provenance = AIProvenance(is_generative, module.metadata.name, module.metadata.module_id if is_generative else None, module.metadata.version if is_generative else None, datetime.now(timezone.utc), "text/plain", True, not is_generative, False)

            # SECURITY: Deterministic SHA-256 hashing, no raw data
            in_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
            out_hash = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
            
            audit_event = AuditEvent(str(uuid.uuid4()), datetime.now(timezone.utc), ctx.request_id, ctx.tenant_id, ctx.subject_id, "MODULE_EXECUTION", module.metadata.module_id, "SUCCESS", {"input_hash": in_hash, "output_hash": out_hash})
            await self.audit_service.record(audit_event)
            trace.execution_steps.append("audited")
            trace.timestamps["end"] = datetime.now(timezone.utc)

            return {"request_id": ctx.request_id, "tenant_id": ctx.tenant_id, "thread_id": ctx.thread_id, "payload": result, "usage": Usage(), "provenance": provenance, "decision_trace": trace, "metadata": {}}
        except Exception as e:
            trace.timestamps["end"] = datetime.now(timezone.utc)
            trace.execution_steps.append(f"failed: {type(e).__name__}")
            await self.audit_service.record(AuditEvent(str(uuid.uuid4()), datetime.now(timezone.utc), ctx.request_id, ctx.tenant_id, ctx.subject_id, "MODULE_EXECUTION", trace.selected_module or "unknown", "FAILURE", {"error_type": type(e).__name__, "error_code": getattr(e, 'code', 'UNKNOWN')}))
            raise