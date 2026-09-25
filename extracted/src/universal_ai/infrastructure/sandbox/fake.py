from universal_ai.interfaces.sandbox import BaseSandbox, SandboxResult
from universal_ai.domain.models import ExecutionContextfrom universal_ai.domain.exceptions import SandboxError

class FakeSandbox(BaseSandbox):
    async def execute(self, ctx: ExecutionContext, code: str, language: str) -> SandboxResult:
        raise SandboxError("Code execution is disabled in the current environment (FakeSandbox).")