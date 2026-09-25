from typing import Protocol, runtime_checkable
from universal_ai.domain.models import AuditEvent

@runtime_checkable
class AuditService(Protocol):
    async def record(self, event: AuditEvent) -> None: ...