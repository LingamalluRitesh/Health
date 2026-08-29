"""
HealthPulse AI — Core Exceptions and Error Hierarchy.
Defines domain-specific clinical and infrastructure exceptions.
"""

from typing import Optional, Dict, Any


class HealthPulseException(Exception):
    """Base exception for all HealthPulse AI platform errors."""
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
        }


class ClinicalValidationException(HealthPulseException):
    """Raised when physiological parameters or lab measurements violate bounds or schemas."""
    def __init__(self, message: str, invalid_field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="CLINICAL_VALIDATION_FAILED", details=details)
        self.invalid_field = invalid_field


class HIPAAComplianceException(HealthPulseException):
    """Raised when an operation violates HIPAA privacy, PHI sanitization, or RBAC controls."""
    def __init__(self, message: str, violation_type: str = "PHI_EXPOSURE_RISK", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="HIPAA_VIOLATION", details=details)
        self.violation_type = violation_type


class FHIRParsingException(HealthPulseException):
    """Raised when FHIR JSON/XML resource parsing or serialization fails."""
    def __init__(self, message: str, resource_type: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="FHIR_PARSE_ERROR", details=details)
        self.resource_type = resource_type


class HL7MessageException(HealthPulseException):
    """Raised when HL7 v2.x segment parsing or generation fails."""
    def __init__(self, message: str, segment_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="HL7_PARSE_ERROR", details=details)
        self.segment_id = segment_id


class DICOMProcessingException(HealthPulseException):
    """Raised when DICOM dataset reading, pixel decoding, or HU transformation fails."""
    def __init__(self, message: str, sop_instance_uid: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="DICOM_PROCESSING_ERROR", details=details)
        self.sop_instance_uid = sop_instance_uid


class GenomicAnalysisException(HealthPulseException):
    """Raised when VCF parsing, variant calling, or PGx guideline matching fails."""
    def __init__(self, message: str, gene: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="GENOMIC_ANALYSIS_ERROR", details=details)
        self.gene = gene


class GovernanceAuditException(HealthPulseException):
    """Raised when AI model cards fail conformity or fairness demographic parity checks."""
    def __init__(self, message: str, metric: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="GOVERNANCE_AUDIT_FAILED", details=details)
        self.metric = metric


class FederatedSecurityException(HealthPulseException):
    """Raised when federated learning aggregation fails or differential privacy budget is exhausted."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="FEDERATED_SECURITY_VIOLATION", details=details)
