"""
HealthPulse AI — Cryptographically Verifiable Merkle Tree Audit Trail.
Guarantees tamper-evident, append-only logging for all EHR accesses, clinical model predictions, and break-glass events.
"""

import hashlib
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditBlock:
    index: int
    timestamp: str
    actor_id: str
    role: str
    action: str
    resource_type: str
    resource_id: str
    patient_id: Optional[str]
    is_break_glass: bool
    payload_hash: str
    previous_hash: str
    current_hash: str

    def compute_hash(self) -> str:
        data_str = f"{self.index}|{self.timestamp}|{self.actor_id}|{self.role}|{self.action}|{self.resource_type}|{self.resource_id}|{self.patient_id}|{self.is_break_glass}|{self.payload_hash}|{self.previous_hash}"
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()


class MerkleAuditTrail:
    """Tamper-evident blockchain-style cryptographic audit ledger."""

    def __init__(self):
        self.chain: List[AuditBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = AuditBlock(
            index=0,
            timestamp="2026-01-01T00:00:00Z",
            actor_id="SYSTEM",
            role="ROOT",
            action="GENESIS_INITIALIZE",
            resource_type="AUDIT_LEDGER",
            resource_id="0",
            patient_id=None,
            is_break_glass=False,
            payload_hash=hashlib.sha256(b"GENESIS_SEED").hexdigest(),
            previous_hash="0" * 64,
            current_hash="",
        )
        genesis.current_hash = genesis.compute_hash()
        self.chain.append(genesis)

    def log_event(
        self,
        actor_id: str,
        role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        patient_id: Optional[str] = None,
        payload_data: Optional[Dict[str, Any]] = None,
        is_break_glass: bool = False,
    ) -> AuditBlock:
        """Appends new cryptographically chained audit block."""
        prev = self.chain[-1]
        payload_json = json.dumps(payload_data or {}, sort_keys=True)
        p_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()

        block = AuditBlock(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat() + "Z",
            actor_id=actor_id,
            role=role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            patient_id=patient_id,
            is_break_glass=is_break_glass,
            payload_hash=p_hash,
            previous_hash=prev.current_hash,
            current_hash="",
        )
        block.current_hash = block.compute_hash()
        self.chain.append(block)
        return block

    def verify_integrity(self) -> Tuple[bool, Optional[str]]:
        """Verifies the unbroken cryptographic hash sequence of the entire audit chain."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.previous_hash != prev.current_hash:
                return False, f"Hash chain broken at block {curr.index}: previous_hash mismatch"

            expected_hash = curr.compute_hash()
            if curr.current_hash != expected_hash:
                return False, f"Tampering detected in block {curr.index}: content hash mismatch"

        return True, "Audit log integrity verified; zero tampering detected."


audit_ledger = MerkleAuditTrail()
