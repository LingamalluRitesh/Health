"""
HealthPulse AI — Evidence-Based Infectious Disease Clinical Practice Guidelines.
Implements IDSA (Infectious Diseases Society of America) clinical guidelines:
- Hospital-Acquired Pneumonia (HAP) and Ventilator-Associated Pneumonia (VAP) Antibiograms
- Febrile Neutropenia (MASCC Risk Index, Broad-Spectrum Antipseudomonal Beta-Lactams)
- Clostridioides difficile Infection (CDI) Primary Episode vs Recurrent (Fidaxomicin / Vancomycin / Fecal Microbiota)
- Infective Endocarditis Duke Modified Criteria & Native vs Prosthetic Valve Empiric Regimens
- Catheter-Related Bloodstream Infections (CRBSI) Line Removal Rules & Lock Solutions
- Complicated Intra-Abdominal Infections (cIAI) Source Control & Targeted Gram-Negative / Anaerobic Coverage
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class IDGuidelineEvaluation:
    guideline_source: str
    infection_syndrome: str
    pathogen_risk_factors: List[str]
    empiric_antimicrobial_regimen: List[str]
    directed_stepdown_options: List[str]
    treatment_duration_days: int
    mandatory_source_control: List[str]


class InfectiousDiseaseGuidelineEngine:
    """Evaluates host immune status, local hospital antibiograms, and pathogen susceptibility patterns."""

    @staticmethod
    def evaluate_febrile_neutropenia(
        absolute_neutrophil_count_cells_ul: float,
        temperature_celsius: float,
        mascc_risk_score: int,
        has_central_line: bool = True,
        hemodynamic_instability: bool = False,
    ) -> IDGuidelineEvaluation:
        """
        IDSA 2011/2023 Guidelines for the Management of Fever and Neutropenia in Cancer Patients.
        High Risk: ANC < 100 cells/uL anticipated > 7 days, or MASCC < 21, or hemodynamic instability.
        Empiric Monotherapy: Cefepime, Meropenem, or Piperacillin-Tazobactam.
        """
        is_high_risk = (
            absolute_neutrophil_count_cells_ul < 100.0
            or mascc_risk_score < 21
            or hemodynamic_instability
        )

        risks = []
        if is_high_risk:
            risks.append("High-Risk Febrile Neutropenia (MASCC < 21 or profound ANC < 100). Inpatient admission required.")
        else:
            risks.append("Low-Risk Febrile Neutropenia (MASCC >= 21). Outpatient oral Ciprofloxacin + Amox/Clav eligible if strictly monitored.")

        empiric = []
        if is_high_risk:
            empiric.append("Antipseudomonal Beta-Lactam Monotherapy: Cefepime 2g IV q8h (extended 4h infusion) OR Piperacillin/Tazobactam 4.5g IV q6h OR Meropenem 1g IV q8h.")
            if hemodynamic_instability or has_central_line:
                empiric.append("Add Vancomycin 15-20 mg/kg IV q8-12h for suspected catheter-related MRSA infection, skin soft tissue infection, or septic shock.")
        else:
            empiric.append("Oral Ciprofloxacin 750mg BID + Amoxicillin-Clavulanate 875/125mg BID.")

        return IDGuidelineEvaluation(
            guideline_source="IDSA Guidelines for Febrile Neutropenia",
            infection_syndrome="Febrile Neutropenia",
            pathogen_risk_factors=risks,
            empiric_antimicrobial_regimen=empiric,
            directed_stepdown_options=["Tailor antibiotics upon blood culture pathogen isolation and MIC susceptibilities."],
            treatment_duration_days=7,
            mandatory_source_control=["Examine all central venous catheter insertion sites daily for erythema/pus."],
        )

    @staticmethod
    def evaluate_cdiff_infection(
        wbc_k_ul: float,
        serum_creatinine_mg_dl: float,
        is_recurrent: bool = False,
        recurrence_count: int = 0,
    ) -> Dict[str, Any]:
        """
        IDSA/SHEA 2021 Focused Update on Management of Clostridioides difficile Infection in Adults.
        Non-Severe: WBC <= 15,000 and SCr < 1.5 mg/dL.
        Severe: WBC >= 15,000 or SCr >= 1.5 mg/dL.
        Fulminant: Hypotension, shock, ileus, or toxic megacolon.
        """
        is_severe = wbc_k_ul >= 15.0 or serum_creatinine_mg_dl >= 1.5

        if not is_recurrent:
            regimen = "Fidaxomicin 200mg orally twice daily for 10 days (Preferred IDSA Category 1 recommendation) OR Oral Vancomycin 125mg QID for 10 days."
        elif recurrence_count == 1:
            regimen = "Fidaxomicin 200mg BID x 5 days then every other day for 20 days (extended-pulsed) OR Vancomycin pulsed/tapered regimen over 6 weeks."
        else:
            regimen = "Fecal Microbiota Transplantation (FMT e.g. Vowst oral spores or Rebyota rectal suspension) + Oral Vancomycin pretreatment. Indicated for multiple recurrent CDI (Class 1, Level A)."

        return {
            "guideline": "IDSA/SHEA 2021 C. difficile Guideline",
            "severity": "Severe CDI" if is_severe else "Non-Severe CDI",
            "is_recurrent": is_recurrent,
            "recurrence_count": recurrence_count,
            "preferred_pharmacotherapy": regimen,
            "isolation_precautions": "Contact Precautions with soap and water hand hygiene (alcohol rub does NOT eradicate C. diff bacterial spores). Discontinue offending inciting systemic antibiotics as soon as possible.",
        }
