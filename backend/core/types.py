"""
HealthPulse AI — Core Type Definitions and Data Models.
Standard enterprise dataclasses and typed structures used across backend systems.
"""

from typing import Dict, List, Optional, Any, Union, Literal
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PatientGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class ClinicalSeverity(str, Enum):
    NORMAL = "normal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class AlertType(str, Enum):
    SEPSIS_WARNING = "sepsis_warning"
    CARDIAC_ARREST_RISK = "cardiac_arrest_risk"
    RESPIRATORY_DEPRESSION = "respiratory_depression"
    DRUG_INTERACTION = "drug_interaction"
    ACUTE_KIDNEY_INJURY = "acute_kidney_injury"
    HEMORRHAGE_RISK = "hemorrhage_risk"
    ANAPHYLAXIS_ALERT = "anaphylaxis_alert"


class ModalityType(str, Enum):
    CT = "CT"
    MR = "MR"
    DX = "DX"
    CR = "CR"
    US = "US"
    PET = "PET"
    NM = "NM"


class RolePermission(str, Enum):
    CLINICIAN = "clinician"
    RADIOLOGIST = "radiologist"
    PHARMACIST = "pharmacist"
    RESEARCHER = "researcher"
    COMPLIANCE_AUDITOR = "compliance_auditor"
    SYSTEM_ADMIN = "system_admin"
    EMERGENCY_OVERRIDE = "emergency_override"


@dataclass
class PatientVitalSigns:
    patient_id: str
    timestamp: datetime
    heart_rate: float
    respiratory_rate: float
    systolic_bp: float
    diastolic_bp: float
    oxygen_saturation: float
    temperature_celsius: float
    mean_arterial_pressure: Optional[float] = None
    gcs_score: Optional[float] = 15.0
    fio2: Optional[float] = 0.21
    pao2: Optional[float] = None
    platelets: Optional[float] = None
    bilirubin: Optional[float] = None
    creatinine: Optional[float] = None
    urine_output_24h: Optional[float] = None
    on_vasopressors: bool = False
    on_mechanical_ventilation: bool = False

    def __post_init__(self):
        if self.mean_arterial_pressure is None:
            self.mean_arterial_pressure = (2.0 * self.diastolic_bp + self.systolic_bp) / 3.0


@dataclass
class ClinicalLabResult:
    test_code: str
    test_name: str
    value: float
    unit: str
    reference_low: float
    reference_high: float
    is_abnormal: bool
    collected_at: datetime
    loinc_code: Optional[str] = None


@dataclass
class MedicationOrder:
    order_id: str
    patient_id: str
    drug_name: str
    rxnorm_code: Optional[str]
    dosage: str
    route: str
    frequency: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "active"


@dataclass
class ClinicalAlert:
    alert_id: str
    patient_id: str
    alert_type: AlertType
    severity: ClinicalSeverity
    message: str
    score: float
    threshold: float
    timestamp: datetime
    evidence: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


@dataclass
class AuditLogEntry:
    entry_id: str
    timestamp: datetime
    actor_id: str
    actor_role: str
    action: str
    resource_type: str
    resource_id: str
    patient_id: Optional[str]
    ip_address: str
    payload_hash: str
    previous_entry_hash: str
    signature: str
    is_break_glass: bool = False
    justification: Optional[str] = None
