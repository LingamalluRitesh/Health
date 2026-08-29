"""
HealthPulse AI — HIPAA Security, De-Identification, and Cryptographic Merkle Audit Endpoints.
"""

from fastapi import APIRouter
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from backend.security.hipaa_scrubber import HIPAAScrubber
from backend.security.merkle_audit import audit_ledger


router = APIRouter()
scrubber = HIPAAScrubber()


class ScrubRequest(BaseModel):
    clinical_text: str = Field(
        ...,
        example="Patient John Doe (SSN: 000-12-3456, MRN: MRN-882319, Phone: 617-555-0199) was admitted on 10/12/2025."
    )
    pseudonymize: bool = Field(True, example=True)


class AuditLogQueryRequest(BaseModel):
    limit: int = Field(50, example=50)


@router.post("/scrub-phi")
def scrub_phi(payload: ScrubRequest):
    res = scrubber.scrub_text(payload.clinical_text, pseudonymize=payload.pseudonymize)
    return {
        "sanitized_text": res.sanitized_text,
        "phi_tokens_removed": res.total_phi_tokens_removed,
        "redacted_entities": [e.__dict__ for e in res.redacted_entities],
    }


@router.get("/audit-ledger")
def get_audit_blocks(limit: int = 50):
    blocks = audit_ledger.chain[-limit:]
    is_valid, msg = audit_ledger.verify_integrity()
    return {
        "is_chain_valid": is_valid,
        "verification_message": msg,
        "total_blocks": len(audit_ledger.chain),
        "recent_blocks": [b.__dict__ for b in blocks],
    }


@router.post("/verify-ledger-integrity")
def verify_integrity():
    is_valid, msg = audit_ledger.verify_integrity()
    return {"is_valid": is_valid, "message": msg}
