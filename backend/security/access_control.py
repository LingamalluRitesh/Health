"""
HealthPulse AI — Role-Based and Attribute-Based Access Control (RBAC/ABAC) Engine.
Enforces least-privilege clinical authorization with emergency Break-Glass overrides.
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from backend.core.types import RolePermission
from backend.core.exceptions import HIPAAComplianceException


class AccessDecision(str, Enum):
    PERMIT = "PERMIT"
    DENY = "DENY"
    BREAK_GLASS_PERMIT = "BREAK_GLASS_PERMIT"


@dataclass
class UserContext:
    user_id: str
    username: str
    role: RolePermission
    department: str
    assigned_patients: List[str] = field(default_factory=list)
    has_active_break_glass: bool = False
    break_glass_reason: Optional[str] = None


class AccessControlEngine:
    """Evaluates contextual authorization requests for clinical resources."""

    def __init__(self):
        self._role_permissions: Dict[RolePermission, Set[str]] = {
            RolePermission.CLINICIAN: {
                "patient:read", "patient:write", "vitals:read", "vitals:write",
                "labs:read", "labs:write", "meds:read", "meds:write",
                "imaging:read", "genomics:read", "cds:evaluate",
            },
            RolePermission.RADIOLOGIST: {
                "patient:read", "imaging:read", "imaging:write", "imaging:export",
            },
            RolePermission.PHARMACIST: {
                "patient:read", "meds:read", "meds:write", "genomics:read", "ddi:check",
            },
            RolePermission.RESEARCHER: {
                "anonymized_cohort:read", "model_card:read", "federated:train",
            },
            RolePermission.COMPLIANCE_AUDITOR: {
                "audit:read", "governance:audit", "model_card:read", "drift:read",
            },
            RolePermission.SYSTEM_ADMIN: {
                "system:admin", "user:manage", "audit:read",
            },
        }

    def evaluate_access(
        self,
        user: UserContext,
        action: str,
        resource_type: str,
        patient_id: Optional[str] = None,
    ) -> AccessDecision:
        """Evaluates whether user is permitted to perform action on resource."""
        # 1. Break-Glass Override Check
        if user.has_active_break_glass and user.break_glass_reason:
            return AccessDecision.BREAK_GLASS_PERMIT

        # 2. Role Permission Matrix
        perms = self._role_permissions.get(user.role, set())
        if action not in perms and "*:*" not in perms:
            return AccessDecision.DENY

        # 3. Patient Relationship Check (ABAC)
        if patient_id and user.role in (RolePermission.CLINICIAN, RolePermission.RADIOLOGIST):
            if user.assigned_patients and patient_id not in user.assigned_patients:
                # If clinician not explicitly assigned, require break-glass
                return AccessDecision.DENY

        # 4. Researcher direct PHI prohibition
        if user.role == RolePermission.RESEARCHER and resource_type in ("patient_raw", "phi_unmasked"):
            return AccessDecision.DENY

        return AccessDecision.PERMIT
