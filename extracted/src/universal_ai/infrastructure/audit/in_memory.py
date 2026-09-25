from typing import List
from universal_ai.interfaces.audit import AuditService
from universal_ai.domain.models import AuditEvent

class InMemoryAuditService(AuditService):
    def __init__(self): self.events: List[AuditEvent] = []
    async def record(self, event: AuditEvent) -> None: self.events.append(event)