from typing import Set, Dict, Any
from universal_ai.interfaces.modules import BaseModule
from universal_ai.domain.models import ModuleMetadata, ExecutionContext, Capability

class EchoModule(BaseModule):
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata("echo_module", "Echo Module", "1.0.0", "Echoes input.", frozenset())
    def required_capabilities(self) -> Set[Capability]: return set(self.metadata.required_capabilities)
    async def execute(self, ctx: ExecutionContext, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"echo": payload.get("message", "No message"), "tenant_id": ctx.tenant_context.tenant_id, "request_id": ctx.tenant_context.request_id}
    async def health_check(self) -> bool: return True