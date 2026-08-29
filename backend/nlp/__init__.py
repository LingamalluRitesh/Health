"""
HealthPulse AI — Clinical NLP, Negation Detection & Terminology Mapping Module.
Provides NegEx negation scopes, ICD-10/11 coding, SNOMED-CT entity extraction, and SOAP parsing.
"""

from backend.nlp.negex import (
    NegExClassifier,
    NegationResult,
    is_negated,
)
from backend.nlp.concept_extractor import (
    ClinicalConceptExtractor,
    ClinicalEntity,
    EntityType,
)
from backend.nlp.icd_coding import (
    AutomatedICD10Coder,
    ICD10CodeMatch,
)
from backend.nlp.soap_parser import (
    SOAPNoteParser,
    SOAPNoteStructure,
)
from backend.nlp.discharge_summary import (
    DischargeSummaryGenerator,
    DischargeSummaryData,
)

__all__ = [
    "NegExClassifier",
    "NegationResult",
    "is_negated",
    "ClinicalConceptExtractor",
    "ClinicalEntity",
    "EntityType",
    "AutomatedICD10Coder",
    "ICD10CodeMatch",
    "SOAPNoteParser",
    "SOAPNoteStructure",
    "DischargeSummaryGenerator",
    "DischargeSummaryData",
]
