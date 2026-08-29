"""
HealthPulse AI — Automated ICD-10-CM / ICD-11 Clinical Coding Engine.
Maps clinical text diagnoses and impression sections to standardized billing and epidemiological codes.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ICD10CodeMatch:
    code: str
    description: str
    chapter: str
    confidence_score: float
    is_primary_candidate: bool
    matched_term: str


class AutomatedICD10Coder:
    """Assigns ICD-10-CM codes to clinical diagnosis descriptions."""

    def __init__(self):
        self._icd_catalog: Dict[str, Dict[str, Any]] = {
            "type 2 diabetes": {"code": "E11.9", "desc": "Type 2 diabetes mellitus without complications", "ch": "Endocrine, nutritional and metabolic diseases"},
            "type 2 diabetes with ckd": {"code": "E11.22", "desc": "Type 2 diabetes mellitus with diabetic chronic kidney disease", "ch": "Endocrine, nutritional and metabolic diseases"},
            "hypertension": {"code": "I10", "desc": "Essential (primary) hypertension", "ch": "Diseases of the circulatory system"},
            "essential hypertension": {"code": "I10", "desc": "Essential (primary) hypertension", "ch": "Diseases of the circulatory system"},
            "atrial fibrillation": {"code": "I48.91", "desc": "Unspecified atrial fibrillation", "ch": "Diseases of the circulatory system"},
            "heart failure": {"code": "I50.9", "desc": "Heart failure, unspecified", "ch": "Diseases of the circulatory system"},
            "systolic heart failure": {"code": "I50.20", "desc": "Unspecified systolic (congestive) heart failure", "ch": "Diseases of the circulatory system"},
            "diastolic heart failure": {"code": "I50.30", "desc": "Unspecified diastolic (congestive) heart failure", "ch": "Diseases of the circulatory system"},
            "community-acquired pneumonia": {"code": "J18.9", "desc": "Pneumonia, unspecified organism", "ch": "Diseases of the respiratory system"},
            "bacterial pneumonia": {"code": "J15.9", "desc": "Unspecified bacterial pneumonia", "ch": "Diseases of the respiratory system"},
            "acute kidney injury": {"code": "N17.9", "desc": "Acute kidney failure, unspecified", "ch": "Diseases of the genitourinary system"},
            "chronic kidney disease stage 3": {"code": "N18.3", "desc": "Chronic kidney disease, stage 3 (moderate)", "ch": "Diseases of the genitourinary system"},
            "sepsis": {"code": "A41.9", "desc": "Sepsis, unspecified organism", "ch": "Certain infectious and parasitic diseases"},
            "septic shock": {"code": "R65.21", "desc": "Severe sepsis with septic shock", "ch": "Symptoms, signs and abnormal clinical findings"},
            "copd": {"code": "J44.9", "desc": "Chronic obstructive pulmonary disease, unspecified", "ch": "Diseases of the respiratory system"},
            "non-small cell lung cancer": {"code": "C34.90", "desc": "Malignant neoplasm of unspecified part of unspecified bronchus or lung", "ch": "Neoplasms"},
        }

    def code_diagnosis_text(self, text: str) -> List[ICD10CodeMatch]:
        """Scans clinical impression text and returns ranked ICD-10 code matches."""
        matches: List[ICD10CodeMatch] = []
        text_lower = text.lower()

        for term, data in self._icd_catalog.items():
            if term in text_lower:
                conf = 0.95 if term == text_lower.strip() else 0.88
                matches.append(
                    ICD10CodeMatch(
                        code=data["code"],
                        description=data["desc"],
                        chapter=data["ch"],
                        confidence_score=conf,
                        is_primary_candidate=False,
                        matched_term=term,
                    )
                )

        # Sort by confidence
        matches.sort(key=lambda m: m.confidence_score, reverse=True)
        if matches:
            matches[0].is_primary_candidate = True

        return matches
