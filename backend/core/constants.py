"""
HealthPulse AI — Core Medical and Architectural Constants.
Contains standard clinical vocabularies, reference ranges, and protocol identifiers.
"""

from typing import Dict, List, Tuple

# Platform metadata
PLATFORM_NAME = "HealthPulse AI Enterprise"
PLATFORM_VERSION = "1.0.0"
COMPLIANCE_STANDARD = "HIPAA Security Rule / EU AI Act High-Risk SaMD"

# Standards & Versions
FHIR_VERSION = "4.0.1"
HL7_VERSION = "2.8"
DICOM_STANDARD_VERSION = "3.0"
ICD10_VERSION = "2024-CM"
ICD11_VERSION = "2024-01"
SNOMED_VERSION = "2024-03-01"
LOINC_VERSION = "2.76"
RXNORM_VERSION = "2024-02"

# Supported Imaging Modalities
SUPPORTED_MODALITIES: List[str] = [
    "CT",     # Computed Tomography
    "MR",     # Magnetic Resonance
    "DX",     # Digital Radiography / X-Ray
    "CR",     # Computed Radiography
    "US",     # Ultrasound
    "XA",     # X-Ray Angiography
    "PET",    # Positron Emission Tomography
    "NM",     # Nuclear Medicine
    "MG",     # Mammography
    "OCT",    # Optical Coherence Tomography
]

# Standard Hounsfield Unit (HU) Window Presets
CT_WINDOW_PRESETS: Dict[str, Tuple[int, int]] = {
    "lung": (-600, 1500),         # Window Level, Window Width
    "mediastinum": (50, 350),
    "bone": (400, 1800),
    "brain": (40, 80),
    "soft_tissue": (40, 400),
    "liver": (60, 160),
    "stroke": (32, 8),
    "subdural": (75, 150),
}

# Normal Adult Physiological Reference Ranges
PHYSIOLOGICAL_NORMAL_RANGES: Dict[str, Dict[str, float]] = {
    "heart_rate": {"min": 60.0, "max": 100.0, "unit": "bpm"},
    "respiratory_rate": {"min": 12.0, "max": 20.0, "unit": "breaths/min"},
    "systolic_bp": {"min": 90.0, "max": 120.0, "unit": "mmHg"},
    "diastolic_bp": {"min": 60.0, "max": 80.0, "unit": "mmHg"},
    "mean_arterial_pressure": {"min": 70.0, "max": 105.0, "unit": "mmHg"},
    "oxygen_saturation": {"min": 95.0, "max": 100.0, "unit": "%"},
    "temperature_celsius": {"min": 36.5, "max": 37.5, "unit": "C"},
    "gcs_score": {"min": 15.0, "max": 15.0, "unit": "points"},
    "serum_creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
    "total_bilirubin": {"min": 0.2, "max": 1.2, "unit": "mg/dL"},
    "platelets": {"min": 150.0, "max": 450.0, "unit": "10^3/uL"},
    "white_blood_cell": {"min": 4.5, "max": 11.0, "unit": "10^3/uL"},
    "blood_urea_nitrogen": {"min": 7.0, "max": 20.0, "unit": "mg/dL"},
    "lactate": {"min": 0.5, "max": 2.0, "unit": "mmol/L"},
    "arterial_ph": {"min": 7.35, "max": 7.45, "unit": "pH"},
    "pao2_fio2_ratio": {"min": 400.0, "max": 500.0, "unit": "mmHg"},
}

# 18 HIPAA Safe Harbor Direct and Indirect Identifiers
HIPAA_18_IDENTIFIERS: List[str] = [
    "NAME",
    "GEOGRAPHIC_SUBDIVISION",
    "DATES",
    "TELEPHONE_NUMBER",
    "FAX_NUMBER",
    "EMAIL_ADDRESS",
    "SOCIAL_SECURITY_NUMBER",
    "MEDICAL_RECORD_NUMBER",
    "HEALTH_PLAN_BENEFICIARY_NUMBER",
    "ACCOUNT_NUMBER",
    "CERTIFICATE_LICENSE_NUMBER",
    "VEHICLE_IDENTIFIER",
    "DEVICE_IDENTIFIER_SERIAL",
    "WEB_URL",
    "IP_ADDRESS",
    "BIOMETRIC_IDENTIFIER",
    "FULL_FACE_PHOTOGRAPH",
    "UNIQUE_IDENTIFYING_NUMBER",
]

# CPIC Actionable Pharmacogenomic Genes
CPIC_ACTIONABLE_GENES: List[str] = [
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "VKORC1",
    "TPMT",
    "NUDT15",
    "DPYD",
    "HLA-B*57:01",
    "HLA-B*15:02",
    "HLA-A*31:01",
    "SLCO1B1",
    "UGT1A1",
    "CYP3A5",
    "G6PD",
]

# Streaming & Queue Constants
DEFAULT_TELEMETRY_INTERVAL_SEC = 1.0
MAX_STREAMING_WINDOW_SIZE = 3600
TELEMETRY_BUFFER_SIZE = 10000
SEPSIS_ALERT_THRESHOLD_SOFA = 2
SEPSIS_ALERT_THRESHOLD_QSOFA = 2
ICU_ALARM_COOLDOWN_SECONDS = 300
