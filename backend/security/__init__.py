"""
HealthPulse AI — HIPAA Compliance, Cryptographic Security & Privacy Module.
Provides 18 Safe Harbor PHI de-identification, Merkle audit chains, RBAC/ABAC with break-glass, and Differential Privacy.
"""

from backend.security.hipaa_scrubber import (
    HIPAAScrubber,
    DeidentificationResult,
    deidentify_clinical_text,
)
from backend.security.merkle_audit import (
    MerkleAuditTrail,
    AuditBlock,
)
from backend.security.access_control import (
    AccessControlEngine,
    UserContext,
    AccessDecision,
)
from backend.security.differential_privacy import (
    DifferentialPrivacyEngine,
    add_gaussian_noise,
    add_laplace_noise,
)
from backend.security.consent_manager import (
    PatientConsentManager,
    ConsentPolicy,
)

__all__ = [
    "HIPAAScrubber",
    "DeidentificationResult",
    "deidentify_clinical_text",
    "MerkleAuditTrail",
    "AuditBlock",
    "AccessControlEngine",
    "UserContext",
    "AccessDecision",
    "DifferentialPrivacyEngine",
    "add_gaussian_noise",
    "add_laplace_noise",
    "PatientConsentManager",
    "ConsentPolicy",
]
