from dataclasses import dataclass, field
from enum import Enum
from typing import Any, FrozenSet, Optional
from datetime import datetime

class Capability(str, Enum):
    LLM_INFERENCE = "LLM_INFERENCE"
    CODE_EXECUTION = "CODE_EXECUTION"
    MEMORY_READ = "MEMORY_READ"
    TOOL_CALL = "TOOL_CALL"

@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    subject_id: str    thread_id: str
    request_id: str
    correlation_id: str
    permissions: FrozenSet[Capability]

@dataclass(frozen=True)
class ExecutionContext:
    tenant_context: TenantContext
    allowed_capabilities: FrozenSet[Capability]
    allowed_tools: FrozenSet[str]
    remaining_steps: int
    remaining_tool_calls: int
    timeout_seconds: float
    is_cancelled: bool = False

@dataclass(frozen=True)
class Usage:
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

@dataclass(frozen=True)
class ModuleMetadata:
    module_id: str
    name: str
    version: str
    description: str
    required_capabilities: FrozenSet[Capability]

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    evaluated_capabilities: FrozenSet[Capability]

@dataclass
class DecisionTrace:
    router: str
    router_version: str
    selected_module: str
    candidate_modules: list[str]
    matched_capabilities: list[Capability]
    policy_decisions: list[PolicyDecision]
    execution_steps: list[str]
    timestamps: dict[str, datetime] = field(default_factory=dict)

@dataclass(frozen=True)
class AIProvenance:
    generated: bool
    generator_type: str    model_id: Optional[str]
    model_version: Optional[str]
    generation_timestamp: datetime
    content_type: str
    machine_readable_marking: bool
    human_visible_label_required: bool
    human_visible_label_applied: bool

@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    timestamp: datetime
    request_id: str
    tenant_id: str
    actor: str
    event_type: str
    component: str
    status: str
    metadata: dict[str, Any]