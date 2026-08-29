"""
Break-Glass Emergency Access & Cryptographic Audit Verification.
Provides audited override access for emergency medical staff with cryptographic non-repudiation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
import hashlib
import hmac
import secrets


@dataclass
class EmergencyAccessSession:
    session_id: str
    user_id: str
    user_role: str
    patient_id: str
    clinical_justification: str
    expires_at: datetime
    is_active: bool = True
    cryptographic_token: str = ""
    audit_hash: str = ""


class BreakGlassSecurityManager:
    """Manages emergency override authorization and cryptographic session non-repudiation."""

    def __init__(self, secret_key: str = "healthpulse-break-glass-master-key"):
        self.secret_key = secret_key.encode("utf-8")
        self.sessions: Dict[str, EmergencyAccessSession] = {}

    def request_emergency_access(
        self,
        user_id: str,
        user_role: str,
        patient_id: str,
        clinical_justification: str,
        duration_minutes: int = 60,
    ) -> EmergencyAccessSession:
        if not clinical_justification or len(clinical_justification.strip()) < 10:
            raise ValueError("A detailed clinical justification (>= 10 chars) is legally required for break-glass override.")

        session_id = f"BG-{secrets.token_hex(8).upper()}"
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
        token = secrets.token_urlsafe(32)

        # Create cryptographic tamper-evident audit hash
        audit_payload = f"{session_id}|{user_id}|{user_role}|{patient_id}|{clinical_justification}|{expires_at.isoformat()}"
        audit_hash = hmac.new(self.secret_key, audit_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        session = EmergencyAccessSession(
            session_id=session_id,
            user_id=user_id,
            user_role=user_role,
            patient_id=patient_id,
            clinical_justification=clinical_justification,
            expires_at=expires_at,
            is_active=True,
            cryptographic_token=token,
            audit_hash=audit_hash,
        )

        self.sessions[session_id] = session
        return session

    def verify_emergency_access(self, session_id: str, token: str) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        if not session.is_active:
            return False
        if datetime.now(timezone.utc) > session.expires_at:
            session.is_active = False
            return False
        return hmac.compare_digest(session.cryptographic_token, token)

    def revoke_emergency_access(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if session:
            session.is_active = False
            return True
        return False
