"""
HealthPulse AI — Clinical Named Entity Recognition & Concept Extractor.
Extracts medical entities (diseases, symptoms, medications, procedures, anatomical sites)
and maps them to UMLS Concept Unique Identifiers (CUI) and SNOMED-CT codes.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from backend.nlp.negex import is_negated


class EntityType(str, Enum):
    DISEASE_OR_SYNDROME = "DISEASE_OR_SYNDROME"
    SIGN_OR_SYMPTOM = "SIGN_OR_SYMPTOM"
    MEDICATION = "MEDICATION"
    PROCEDURE = "PROCEDURE"
    ANATOMY = "ANATOMY"
    LAB_MEASUREMENT = "LAB_MEASUREMENT"


@dataclass
class ClinicalEntity:
    text: str
    entity_type: EntityType
    start_char: int
    end_char: int
    snomed_code: Optional[str]
    cui: Optional[str]
    is_negated: bool
    confidence: float


class ClinicalConceptExtractor:
    """Extracts clinical concepts and resolves biomedical terminologies."""

    def __init__(self):
        self._concept_dictionary: Dict[str, Dict[str, Any]] = {
            "type 2 diabetes": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "44054006", "cui": "C0011860"},
            "diabetes mellitus": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "73211009", "cui": "C0011849"},
            "hypertension": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "38341003", "cui": "C0020538"},
            "high blood pressure": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "38341003", "cui": "C0020538"},
            "atrial fibrillation": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "49436004", "cui": "C0004238"},
            "heart failure": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "84114007", "cui": "C0018801"},
            "pneumonia": {"type": EntityType.DISEASE_OR_SYNDROME, "snomed": "233604007", "cui": "C0032285"},
            "chest pain": {"type": EntityType.SIGN_OR_SYMPTOM, "snomed": "29857009", "cui": "C0008031"},
            "shortness of breath": {"type": EntityType.SIGN_OR_SYMPTOM, "snomed": "267036007", "cui": "C0013404"},
            "dyspnea": {"type": EntityType.SIGN_OR_SYMPTOM, "snomed": "267036007", "cui": "C0013404"},
            "fever": {"type": EntityType.SIGN_OR_SYMPTOM, "snomed": "386661006", "cui": "C0015967"},
            "metformin": {"type": EntityType.MEDICATION, "snomed": "372567009", "cui": "C0025598"},
            "lisinopril": {"type": EntityType.MEDICATION, "snomed": "387431005", "cui": "C0065374"},
            "aspirin": {"type": EntityType.MEDICATION, "snomed": "387458008", "cui": "C0004057"},
            "atorvastatin": {"type": EntityType.MEDICATION, "snomed": "387584000", "cui": "C0286651"},
            "warfarin": {"type": EntityType.MEDICATION, "snomed": "372756006", "cui": "C0043031"},
            "apixaban": {"type": EntityType.MEDICATION, "snomed": "703848006", "cui": "C2347313"},
            "echocardiogram": {"type": EntityType.PROCEDURE, "snomed": "40701008", "cui": "C0013516"},
            "coronary angiogram": {"type": EntityType.PROCEDURE, "snomed": "252275004", "cui": "C0010055"},
            "computed tomography": {"type": EntityType.PROCEDURE, "snomed": "77477000", "cui": "C0040405"},
            "left ventricle": {"type": EntityType.ANATOMY, "snomed": "87878005", "cui": "C0225897"},
            "right lung": {"type": EntityType.ANATOMY, "snomed": "266005", "cui": "C0225756"},
        }

    def extract_entities(self, text: str) -> List[ClinicalEntity]:
        """Extracts all clinical entities in text with character spans, SNOMED codes, and negation status."""
        found_entities: List[ClinicalEntity] = []
        text_lower = text.lower()

        # Sentence split for contextual negation evaluation
        sentences = re.split(r"(?<=[.!?])\s+", text)

        for phrase, meta in self._concept_dictionary.items():
            pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
            for match in pattern.finditer(text):
                start, end = match.span()
                entity_txt = text[start:end]

                # Find containing sentence for negation
                containing_sentence = text
                for s in sentences:
                    if entity_txt in s:
                        containing_sentence = s
                        break

                neg = is_negated(containing_sentence, entity_txt)

                found_entities.append(
                    ClinicalEntity(
                        text=entity_txt,
                        entity_type=meta["type"],
                        start_char=start,
                        end_char=end,
                        snomed_code=meta["snomed"],
                        cui=meta["cui"],
                        is_negated=neg,
                        confidence=0.95,
                    )
                )

        # Sort by occurrence in text
        found_entities.sort(key=lambda e: e.start_char)
        return found_entities
