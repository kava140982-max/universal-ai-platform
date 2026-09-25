from typing import Protocol, runtime_checkable
from dataclasses import dataclass
from universal_ai.domain.models import ExecutionContext

@dataclass(frozen=True)
class SandboxResult:
    stdout: str
    stderr: str
    exit_code: int

@runtime_checkable
class BaseSandbox(Protocol):
    async def execute(self, ctx: ExecutionContext, code: str, language: str) -> SandboxResult: ...