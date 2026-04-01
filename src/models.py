from pydantic import BaseModel
from typing import List, Optional

class SecurityFinding(BaseModel):
    severity: str
    issue: str
    resource_name: str
    namespace: Optional[str] = None

class AuditEvent(BaseModel):
    timestamp: str
    user: str
    action: str
    resource: str
    status: str
