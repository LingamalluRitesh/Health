"""
HealthPulse AI — Core Package.
Provides foundation settings, telemetry, caching, database layer, and event buses.
"""

from backend.core.config import Settings, get_settings
from backend.core.constants import (
    FHIR_VERSION,
    SUPPORTED_MODALITIES,
    ICD10_VERSION,
    SNOMED_VERSION,
    DEFAULT_TELEMETRY_INTERVAL_SEC,
)
from backend.core.exceptions import (
    HealthPulseException,
    ClinicalValidationException,
    HIPAAComplianceException,
    DICOMProcessingException,
    FHIRParsingException,
)

__all__ = [
    "Settings",
    "get_settings",
    "FHIR_VERSION",
    "SUPPORTED_MODALITIES",
    "ICD10_VERSION",
    "SNOMED_VERSION",
    "DEFAULT_TELEMETRY_INTERVAL_SEC",
    "HealthPulseException",
    "ClinicalValidationException",
    "HIPAAComplianceException",
    "DICOMProcessingException",
    "FHIRParsingException",
]
