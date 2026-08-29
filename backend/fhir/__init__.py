"""
HealthPulse AI — FHIR R4 and HL7 Interoperability Module.
Provides FHIR R4 resource models, HL7 v2.x parser/serializers, OMOP CDM ETL, and CDS Hooks engines.
"""

from backend.fhir.models import (
    FHIRResource,
    FHIRPatient,
    FHIRObservation,
    FHIRCondition,
    FHIREncounter,
    FHIRDiagnosticReport,
    FHIRMedicationRequest,
    FHIRCarePlan,
    FHIRBundle,
    FHIRCodeableConcept,
    FHIRCoding,
    FHIRIdentifier,
    FHIRReference,
    FHIRQuantity,
)
from backend.fhir.hl7_parser import HL7Message, HL7Segment, parse_hl7_v2
from backend.fhir.hl7_serializer import build_adt_a01, build_oru_r01, build_mdm_t02
from backend.fhir.omop_cdm import OMOPTransformer, OMOPPerson, OMOPMeasurement
from backend.fhir.cds_hooks import CDSHooksEngine, CDSCard, CDSServiceDiscovery

__all__ = [
    "FHIRResource",
    "FHIRPatient",
    "FHIRObservation",
    "FHIRCondition",
    "FHIREncounter",
    "FHIRDiagnosticReport",
    "FHIRMedicationRequest",
    "FHIRCarePlan",
    "FHIRBundle",
    "FHIRCodeableConcept",
    "FHIRCoding",
    "FHIRIdentifier",
    "FHIRReference",
    "FHIRQuantity",
    "HL7Message",
    "HL7Segment",
    "parse_hl7_v2",
    "build_adt_a01",
    "build_oru_r01",
    "build_mdm_t02",
    "OMOPTransformer",
    "OMOPPerson",
    "OMOPMeasurement",
    "CDSHooksEngine",
    "CDSCard",
    "CDSServiceDiscovery",
]
