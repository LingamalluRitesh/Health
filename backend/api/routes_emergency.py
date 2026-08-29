"""
Break-Glass Emergency Access API Routes.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from backend.security.emergency_access import BreakGlassSecurityManager

router = APIRouter()
security_manager = BreakGlassSecurityManager()


class EmergencyAccessRequest(BaseModel):
    user_id: str = Field(..., example="PRACTITIONER-701")
    user_role: str = Field(..., example="ATTENDING_PHYSICIAN")
    patient_id: str = Field(..., example="PAT-99104")
    clinical_justification: str = Field(..., example="Patient in acute cardiac arrest requiring immediate un-consented chart review.")
    duration_minutes: Optional[int] = Field(60, example=60)


class VerifyAccessRequest(BaseModel):
    session_id: str = Field(..., example="BG-A1B2C3D4")
    token: str = Field(..., example="sometoken")


@router.post("/request", summary="Request Break-Glass Emergency Override")
async def request_break_glass(req: EmergencyAccessRequest) -> Dict[str, Any]:
    try:
        session = security_manager.request_emergency_access(
            user_id=req.user_id,
            user_role=req.user_role,
            patient_id=req.patient_id,
            clinical_justification=req.clinical_justification,
            duration_minutes=req.duration_minutes or 60,
        )
        return {
            "session_id": session.session_id,
            "patient_id": session.patient_id,
            "user_id": session.user_id,
            "expires_at": session.expires_at.isoformat(),
            "cryptographic_token": session.cryptographic_token,
            "audit_hash": session.audit_hash,
            "status": "AUTHORIZED_EMERGENCY_OVERRIDE",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify", summary="Verify Active Emergency Session")
async def verify_break_glass(req: VerifyAccessRequest) -> Dict[str, Any]:
    is_valid = security_manager.verify_emergency_access(req.session_id, req.token)
    return {"session_id": req.session_id, "valid": is_valid}


@router.post("/revoke/{session_id}", summary="Revoke Emergency Session")
async def revoke_break_glass(session_id: str) -> Dict[str, Any]:
    revoked = security_manager.revoke_emergency_access(session_id)
    if not revoked:
        raise HTTPException(status_code=404, detail="Emergency session not found.")
    return {"session_id": session_id, "revoked": True}
