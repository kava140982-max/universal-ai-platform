from contextvars import ContextVar
from fastapi import Request, HTTPException
from universal_ai.domain.models import TenantContext, Capability

request_id_var: ContextVar[str] = ContextVar('request_id')
correlation_id_var: ContextVar[str] = ContextVar('correlation_id')

def get_tenant_context(request: Request) -> TenantContext:    req_id = request.headers.get("X-Request-ID")
    if not req_id: raise HTTPException(status_code=400, detail="Missing X-Request-ID header")
    request_id_var.set(req_id)
    correlation_id_var.set(request.headers.get("X-Correlation-ID", req_id))
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id: raise HTTPException(status_code=400, detail="Missing X-Tenant-ID header")

    # SECURITY: Client CANNOT grant themselves permissions via headers. 
    # Permissions must come from a trusted IAM/JWT validation in production.
    permissions = set() 
    subject_id = request.headers.get("X-Subject-ID", "anonymous")
    # Mocked trusted lookup for testing purposes only
    if subject_id == "admin_user": permissions.add(Capability.CODE_EXECUTION)

    return TenantContext(tenant_id, subject_id, request.headers.get("X-Thread-ID", "default"), req_id, request.headers.get("X-Correlation-ID", req_id), frozenset(permissions))