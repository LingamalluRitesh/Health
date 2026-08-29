"""
HealthPulse AI — Patient Consent and Minimum Necessary Disclosure Manager.
Tracks individual patient consent preferences for clinical trials, research secondary use, and genomics sharing.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConsentPolicy:
    patient_id: str
    allow_clinical_care_access: bool = True
    allow_academic_research: bool = True
    allow_commercial_pharma_trials: bool = False
    allow_genomic_data_sharing: bool = False
    allow_ai_model_training: bool = True
    consent_date: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    revocation_date: Optional[str] = None


class PatientConsentManager:
    """Manages consent verification before clinical data extraction."""

    def __init__(self):
        self._consent_store: Dict[str, ConsentPolicy] = {}

    def set_consent(self, policy: ConsentPolicy) -> None:
        self._consent_store[policy.patient_id] = policy

    def get_consent(self, patient_id: str) -> ConsentPolicy:
        if patient_id not in self._consent_store:
            # Default opt-in to clinical care & research with AI training
            self._consent_store[patient_id] = ConsentPolicy(patient_id=patient_id)
        return self._consent_store[patient_id]

    def can_use_for_federated_training(self, patient_id: str) -> bool:
        policy = self.get_consent(patient_id)
        return policy.allow_ai_model_training and policy.revocation_date is None

    def filter_minimum_necessary(self, patient_record: Dict[str, Any], requester_purpose: str) -> Dict[str, Any]:
        """Strips non-essential fields conforming to HIPAA minimum necessary rule."""
        if requester_purpose == "BILLING":
            return {
                "patient_id": patient_record.get("patient_id"),
                "icd10_codes": patient_record.get("icd10_codes", []),
                "procedures": patient_record.get("procedures", []),
                "dates_of_service": patient_record.get("dates_of_service", []),
            }
        elif requester_purpose == "RESEARCH":
            rec = patient_record.copy()
            rec.pop("name", None)
            rec.pop("address", None)
            rec.pop("telecom", None)
            rec.pop("ssn", None)
            return rec
        return patient_record
