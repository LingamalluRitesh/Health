"""
HealthPulse AI — ICD-10-CM / ICD-11 Diagnosis Coding & Hierarchical Condition Categories (HCC).
Complete structured diagnosis master file for clinical documentation improvement and risk adjustment.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ICD10Entry:
    code: str
    description: str
    chapter_num: int
    chapter_title: str
    is_billable: bool
    hcc_code_v28: Optional[str]
    is_chronic: bool
    risk_adjustment_factor_weight: float


ICD10_MASTER_CATALOG: Dict[str, ICD10Entry] = {
    # Infectious Diseases
    "A41.9": ICD10Entry("A41.9", "Sepsis, unspecified organism", 1, "Certain infectious and parasitic diseases", True, "HCC 2", False, 0.450),
    "R65.20": ICD10Entry("R65.20", "Severe sepsis without septic shock", 18, "Symptoms, signs and abnormal findings", True, "HCC 2", False, 0.580),
    "R65.21": ICD10Entry("R65.21", "Severe sepsis with septic shock", 18, "Symptoms, signs and abnormal findings", True, "HCC 2", False, 0.720),
    "A04.72": ICD10Entry("A04.72", "Enterocolitis due to Clostridioides difficile, not specified as recurrent", 1, "Certain infectious and parasitic diseases", True, None, False, 0.0),
    "A04.71": ICD10Entry("A04.71", "Enterocolitis due to Clostridioides difficile, recurrent", 1, "Certain infectious and parasitic diseases", True, None, False, 0.0),
    "B34.9": ICD10Entry("B34.9", "Viral infection, unspecified", 1, "Certain infectious and parasitic diseases", True, None, False, 0.0),

    # Circulatory System
    "I10": ICD10Entry("I10", "Essential (primary) hypertension", 9, "Diseases of the circulatory system", True, None, True, 0.0),
    "I11.0": ICD10Entry("I11.0", "Hypertensive heart disease with heart failure", 9, "Diseases of the circulatory system", True, "HCC 85", True, 0.368),
    "I12.9": ICD10Entry("I12.9", "Hypertensive chronic kidney disease with stage 1 through stage 4 chronic kidney disease", 9, "Diseases of the circulatory system", True, None, True, 0.0),
    "I13.0": ICD10Entry("I13.0", "Hypertensive heart and chronic kidney disease with heart failure and stage 1 through stage 4 chronic kidney disease", 9, "Diseases of the circulatory system", True, "HCC 85", True, 0.420),
    "I50.9": ICD10Entry("I50.9", "Heart failure, unspecified", 9, "Diseases of the circulatory system", True, "HCC 85", True, 0.368),
    "I50.20": ICD10Entry("I50.20", "Unspecified systolic (congestive) heart failure", 9, "Diseases of the circulatory system", True, "HCC 85", True, 0.368),
    "I50.22": ICD10Entry("I50.22", "Chronic systolic (congestive) heart failure (HFrEF)", 9, "Diseases of the circulatory system", True, "HCC 85", True, 0.368),
    "I50.32": ICD10Entry("I50.32", "Chronic diastolic (congestive) heart failure (HFpEF)", 9, "Diseases of the circulatory system", True, "HCC 85", True, 0.368),
    "I48.91": ICD10Entry("I48.91", "Unspecified atrial fibrillation", 9, "Diseases of the circulatory system", True, "HCC 96", True, 0.268),
    "I48.0": ICD10Entry("I48.0", "Paroxysmal atrial fibrillation", 9, "Diseases of the circulatory system", True, "HCC 96", True, 0.268),
    "I48.19": ICD10Entry("I48.19", "Other persistent atrial fibrillation", 9, "Diseases of the circulatory system", True, "HCC 96", True, 0.268),
    "I21.09": ICD10Entry("I21.09", "ST elevation (STEMI) myocardial infarction involving other coronary artery of anterior wall", 9, "Diseases of the circulatory system", True, "HCC 86", False, 0.290),
    "I21.4": ICD10Entry("I21.4", "Non-ST elevation (NSTEMI) myocardial infarction", 9, "Diseases of the circulatory system", True, "HCC 86", False, 0.290),
    "I25.10": ICD10Entry("I25.10", "Atherosclerotic heart disease of native coronary artery without angina pectoris", 9, "Diseases of the circulatory system", True, None, True, 0.0),

    # Endocrine & Metabolic
    "E11.9": ICD10Entry("E11.9", "Type 2 diabetes mellitus without complications", 4, "Endocrine, nutritional and metabolic diseases", True, "HCC 19", True, 0.105),
    "E11.22": ICD10Entry("E11.22", "Type 2 diabetes mellitus with diabetic chronic kidney disease", 4, "Endocrine, nutritional and metabolic diseases", True, "HCC 18", True, 0.302),
    "E11.51": ICD10Entry("E11.51", "Type 2 diabetes mellitus with diabetic peripheral angiopathy without gangrene", 4, "Endocrine, nutritional and metabolic diseases", True, "HCC 18", True, 0.302),
    "E10.10": ICD10Entry("E10.10", "Type 1 diabetes mellitus with ketoacidosis without coma", 4, "Endocrine, nutritional and metabolic diseases", True, "HCC 17", True, 0.450),
    "E03.9": ICD10Entry("E03.9", "Hypothyroidism, unspecified", 4, "Endocrine, nutritional and metabolic diseases", True, None, True, 0.0),
    "E78.5": ICD10Entry("E78.5", "Hyperlipidemia, unspecified", 4, "Endocrine, nutritional and metabolic diseases", True, None, True, 0.0),

    # Respiratory System
    "J44.9": ICD10Entry("J44.9", "Chronic obstructive pulmonary disease, unspecified", 10, "Diseases of the respiratory system", True, "HCC 111", True, 0.335),
    "J44.1": ICD10Entry("J44.1", "Chronic obstructive pulmonary disease with (acute) exacerbation", 10, "Diseases of the respiratory system", True, "HCC 111", False, 0.335),
    "J45.909": ICD10Entry("J45.909", "Unspecified asthma, uncomplicated", 10, "Diseases of the respiratory system", True, None, True, 0.0),
    "J18.9": ICD10Entry("J18.9", "Pneumonia, unspecified organism", 10, "Diseases of the respiratory system", True, "HCC 114", False, 0.210),
    "J80": ICD10Entry("J80", "Acute respiratory distress syndrome", 10, "Diseases of the respiratory system", True, "HCC 114", False, 0.450),

    # Genitourinary System
    "N18.30": ICD10Entry("N18.30", "Chronic kidney disease, stage 3 unspecified", 14, "Diseases of the genitourinary system", True, "HCC 138", True, 0.069),
    "N18.31": ICD10Entry("N18.31", "Chronic kidney disease, stage 3a", 14, "Diseases of the genitourinary system", True, "HCC 138", True, 0.069),
    "N18.32": ICD10Entry("N18.32", "Chronic kidney disease, stage 3b", 14, "Diseases of the genitourinary system", True, "HCC 138", True, 0.069),
    "N18.4": ICD10Entry("N18.4", "Chronic kidney disease, stage 4 (severe)", 14, "Diseases of the genitourinary system", True, "HCC 137", True, 0.289),
    "N18.5": ICD10Entry("N18.5", "Chronic kidney disease, stage 5", 14, "Diseases of the genitourinary system", True, "HCC 136", True, 0.450),
    "N18.6": ICD10Entry("N18.6", "End stage renal disease (on chronic dialysis)", 14, "Diseases of the genitourinary system", True, "HCC 134", True, 0.580),
    "N17.9": ICD10Entry("N17.9", "Acute kidney failure, unspecified", 14, "Diseases of the genitourinary system", True, "HCC 135", False, 0.315),
}


def lookup_icd10(code: str) -> Optional[ICD10Entry]:
    """Retrieves ICD-10-CM entry by code."""
    return ICD10_MASTER_CATALOG.get(code)
