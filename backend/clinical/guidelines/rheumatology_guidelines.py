"""
HealthPulse AI — Evidence-Based Rheumatology Clinical Practice Guidelines.
Implements ACR (American College of Rheumatology) and EULAR clinical guidelines:
- Rheumatoid Arthritis (ACR/EULAR 2010 Criteria, DAS28 / CDAI Staging, csDMARD Methotrexate vs bDMARDs/tsDMARDs)
- Systemic Lupus Erythematosus (EULAR/ACR 2019 Criteria, Hydroxychloroquine Dosing & Lupus Nephritis Induction)
- Giant Cell Arteritis & Polymyalgia Rheumatica (Tocilizumab + High-Dose Glucocorticoid Taper)
- Gout Flare & Urate-Lowering Therapy (ACR 2020 Guidelines: Allopurinol Treat-to-Target Serum Urate < 6.0 mg/dL)
- ANCA-Associated Vasculitis (GPA / MPA: Rituximab vs Cyclophosphamide Induction & Avacopan)
- Ankylosing Spondylitis & Axial Spondyloarthritis (ASAS Criteria & TNF / IL-17 Inhibitors)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class RheumatologyGuidelineEvaluation:
    guideline_source: str
    rheumatic_condition: str
    disease_activity_index: str
    cs_dmard_recommendations: List[str]
    biologic_and_targeted_dmard_options: List[str]
    safety_monitoring_protocol: List[str]


class RheumatologyGuidelineEngine:
    """Evaluates autoantibody profiles, joint counts, and acute phase reactants."""

    @staticmethod
    def evaluate_rheumatoid_arthritis_therapy(
        cdai_score: float,  # Clinical Disease Activity Index
        has_moderate_high_activity: bool,
        has_poor_prognostic_factors: bool = True,  # High anti-CCP/RF titers, bone erosions
        current_methotrexate_weekly_mg: float = 0.0,
        has_prior_biologic_failure: bool = False,
    ) -> RheumatologyGuidelineEvaluation:
        """
        ACR 2021 Guideline for the Treatment of Rheumatoid Arthritis.
        CDAI <= 2.8: Remission
        CDAI 2.9 - 10.0: Low Activity
        CDAI 10.1 - 22.0: Moderate Activity
        CDAI > 22.0: High Activity
        """
        cs_dmards = []
        b_dmards = []

        if current_methotrexate_weekly_mg < 15.0:
            cs_dmards.append("Initiate or titrate Oral/Subcutaneous Methotrexate: Start at 15mg weekly and rapidly escalate to target dose 20-25mg weekly with daily Folic Acid (1-2mg/day) (Class 1, Level A).")
        else:
            cs_dmards.append("Continue maximally tolerated Methotrexate (20-25mg weekly).")

        if has_moderate_high_activity:
            if current_methotrexate_weekly_mg >= 15.0:
                b_dmards.append("Add a Biologic DMARD (TNF inhibitor: Adalimumab 40mg q2w or Etanercept 50mg weekly) OR a targeted synthetic DMARD (JAK inhibitor: Tofacitinib, Upadacitinib) (Class 1, Level A).")
                if has_prior_biologic_failure:
                    b_dmards.append("Switch to alternative mechanism of action Biologic (IL-6 inhibitor Tocilizumab, T-cell costimulation modulator Abatacept, or B-cell depleting agent Rituximab).")

        safety = [
            "Screen for Latent Tuberculosis (QuantiFERON-TB Gold or T-Spot) and Hepatitis B/C serologies PRIOR to initiating any biologic or targeted synthetic DMARD.",
            "Obtain baseline CBC, AST/ALT, and serum creatinine every 4-8 weeks during Methotrexate titration.",
            "Vaccination: Administer Recombinant Zoster Vaccine (Shingrix), Pneumococcal, and Influenza vaccines before DMARD immunosuppression where feasible.",
        ]

        return RheumatologyGuidelineEvaluation(
            guideline_source="ACR 2021 Rheumatoid Arthritis Guidelines",
            rheumatic_condition="Rheumatoid Arthritis (RA)",
            disease_activity_index=f"CDAI Score: {cdai_score} ({'High Activity' if cdai_score > 22 else 'Moderate Activity' if cdai_score > 10 else 'Low/Remission'})",
            cs_dmard_recommendations=cs_dmards,
            biologic_and_targeted_dmard_options=b_dmards if b_dmards else ["Maintain csDMARD monotherapy in low disease activity/remission."],
            safety_monitoring_protocol=safety,
        )
