"""
HealthPulse AI — SNOMED CT Comprehensive Medical Ontology & Clinical Terminology.
Contains mapped SNOMED concepts spanning clinical findings, disorders, procedures, body structures, and organisms.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SNOMEDConcept:
    concept_id: str
    fully_specified_name: str
    preferred_term: str
    semantic_tag: str
    parent_concept_ids: List[str]


SNOMED_CONCEPT_DICTIONARY: Dict[str, SNOMEDConcept] = {
    # Cardiovascular Disorders
    "49436004": SNOMEDConcept("49436004", "Atrial fibrillation (disorder)", "Atrial fibrillation", "disorder", ["49601007"]),
    "84114007": SNOMEDConcept("84114007", "Heart failure (disorder)", "Heart failure", "disorder", ["56265001"]),
    "22298006": SNOMEDConcept("22298006", "Myocardial infarction (disorder)", "Myocardial infarction", "disorder", ["56265001"]),
    "38341003": SNOMEDConcept("38341003", "Hypertensive disorder, systemic arterial (disorder)", "Essential hypertension", "disorder", ["56265001"]),
    "42343007": SNOMEDConcept("42343007", "Congestive heart failure (disorder)", "Congestive heart failure", "disorder", ["84114007"]),
    "53741008": SNOMEDConcept("53741008", "Coronary arteriosclerosis (disorder)", "Coronary artery disease", "disorder", ["56265001"]),
    "401303003": SNOMEDConcept("401303003", "Acute non-ST segment elevation myocardial infarction (disorder)", "NSTEMI", "disorder", ["22298006"]),
    "401314000": SNOMEDConcept("401314000", "Acute ST segment elevation myocardial infarction (disorder)", "STEMI", "disorder", ["22298006"]),
    "698247007": SNOMEDConcept("698247007", "Heart failure with reduced ejection fraction (disorder)", "HFrEF", "disorder", ["84114007"]),
    "698248002": SNOMEDConcept("698248002", "Heart failure with preserved ejection fraction (disorder)", "HFpEF", "disorder", ["84114007"]),

    # Pulmonary Disorders
    "13645005": SNOMEDConcept("13645005", "Chronic obstructive lung disease (disorder)", "COPD", "disorder", ["19829001"]),
    "195967001": SNOMEDConcept("195967001", "Asthma (disorder)", "Asthma", "disorder", ["19829001"]),
    "233604007": SNOMEDConcept("233604007", "Pneumonia (disorder)", "Pneumonia", "disorder", ["19829001"]),
    "67782005": SNOMEDConcept("67782005", "Acute respiratory distress syndrome (disorder)", "ARDS", "disorder", ["19829001"]),
    "59282003": SNOMEDConcept("59282003", "Pulmonary embolism (disorder)", "Pulmonary embolism", "disorder", ["19829001"]),
    "70995007": SNOMEDConcept("70995007", "Pulmonary hypertension (disorder)", "Pulmonary hypertension", "disorder", ["19829001"]),

    # Endocrine & Metabolic Disorders
    "44054006": SNOMEDConcept("44054006", "Type 2 diabetes mellitus (disorder)", "Type 2 diabetes mellitus", "disorder", ["73211009"]),
    "46635009": SNOMEDConcept("46635009", "Type 1 diabetes mellitus (disorder)", "Type 1 diabetes mellitus", "disorder", ["73211009"]),
    "420422005": SNOMEDConcept("420422005", "Diabetic ketoacidosis (disorder)", "Diabetic ketoacidosis", "disorder", ["73211009"]),
    "40930008": SNOMEDConcept("40930008", "Hypothyroidism (disorder)", "Hypothyroidism", "disorder", ["36369007"]),
    "34486009": SNOMEDConcept("34486009", "Hyperthyroidism (disorder)", "Hyperthyroidism", "disorder", ["36369007"]),
    "237599002": SNOMEDConcept("237599002", "Primary hyperparathyroidism (disorder)", "Primary hyperparathyroidism", "disorder", ["36369007"]),

    # Renal & Urological Disorders
    "709044004": SNOMEDConcept("709044004", "Chronic kidney disease (disorder)", "Chronic kidney disease", "disorder", ["90708001"]),
    "14669001": SNOMEDConcept("14669001", "Acute kidney injury (disorder)", "Acute kidney injury", "disorder", ["90708001"]),
    "46177005": SNOMEDConcept("46177005", "End stage renal disease (disorder)", "End-stage renal disease", "disorder", ["709044004"]),
    "95893006": SNOMEDConcept("95893006", "Diabetic nephropathy (disorder)", "Diabetic nephropathy", "disorder", ["709044004"]),

    # Infectious Diseases & Sepsis
    "91302008": SNOMEDConcept("91302008", "Sepsis (disorder)", "Sepsis", "disorder", ["40733004"]),
    "76571007": SNOMEDConcept("76571007", "Septic shock (disorder)", "Septic shock", "disorder", ["91302008"]),
    "186431008": SNOMEDConcept("186431008", "Clostridioides difficile colitis (disorder)", "C. difficile colitis", "disorder", ["40733004"]),
    "15437000": SNOMEDConcept("15437000", "Infective endocarditis (disorder)", "Infective endocarditis", "disorder", ["40733004"]),
    "128045006": SNOMEDConcept("128045006", "Cellulitis (disorder)", "Cellulitis", "disorder", ["40733004"]),

    # Neurological Disorders
    "230690007": SNOMEDConcept("230690007", "Cerebrovascular accident (disorder)", "Stroke", "disorder", ["69896004"]),
    "422504002": SNOMEDConcept("422504002", "Ischemic stroke (disorder)", "Acute ischemic stroke", "disorder", ["230690007"]),
    "274100004": SNOMEDConcept("274100004", "Intracerebral hemorrhage (disorder)", "Intracerebral hemorrhage", "disorder", ["230690007"]),
    "230456007": SNOMEDConcept("230456007", "Status epilepticus (disorder)", "Status epilepticus", "disorder", ["84757009"]),
    "24700007": SNOMEDConcept("24700007", "Multiple sclerosis (disorder)", "Multiple sclerosis", "disorder", ["69896004"]),
    "26929004": SNOMEDConcept("26929004", "Alzheimer's disease (disorder)", "Alzheimer's disease", "disorder", ["69896004"]),
    "49049000": SNOMEDConcept("49049000", "Parkinson's disease (disorder)", "Parkinson's disease", "disorder", ["69896004"]),

    # Clinical Findings & Symptoms
    "29857009": SNOMEDConcept("29857009", "Chest pain (finding)", "Chest pain", "finding", ["404684003"]),
    "267036007": SNOMEDConcept("267036007", "Dyspnea (finding)", "Shortness of breath", "finding", ["404684003"]),
    "386661006": SNOMEDConcept("386661006", "Fever (finding)", "Fever", "finding", ["404684003"]),
    "422400008": SNOMEDConcept("422400008", "Altered mental status (finding)", "Altered mental status", "finding", ["404684003"]),
    "422587007": SNOMEDConcept("422587007", "Nausea (finding)", "Nausea", "finding", ["404684003"]),
    "271795006": SNOMEDConcept("271795006", "Edema (finding)", "Peripheral edema", "finding", ["404684003"]),
    "84229001": SNOMEDConcept("84229001", "Fatigue (finding)", "Fatigue", "finding", ["404684003"]),
}


def lookup_snomed_concept(concept_id: str) -> Optional[SNOMEDConcept]:
    """Retrieves SNOMED CT concept metadata by identifier."""
    return SNOMED_CONCEPT_DICTIONARY.get(concept_id)


def search_snomed_by_term(term: str) -> List[SNOMEDConcept]:
    """Performs substring match on preferred term or fully specified name."""
    term_lower = term.lower()
    return [
        c for c in SNOMED_CONCEPT_DICTIONARY.values()
        if term_lower in c.preferred_term.lower() or term_lower in c.fully_specified_name.lower()
    ]
