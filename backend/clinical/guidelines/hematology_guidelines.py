"""
HealthPulse AI — Evidence-Based Hematology Clinical Practice Guidelines.
Implements ASH (American Society of Hematology) and ISTH guidelines:
- Heparin-Induced Thrombocytopenia (HIT 4Ts Score & Argatroban / Bivalirudin Non-Heparin Anticoagulants)
- Immune Thrombocytopenia (ITP 1st-Line Corticosteroids / IVIG vs 2nd-Line TPO-RAs / Rituximab)
- Thrombotic Thrombocytopenic Purpura (TTP PLASMIC Score & Caplacizumab / Emergent Plasma Exchange)
- Cancer-Associated Thrombosis (CAT: DOACs vs LMWH)
- Massive Transfusion Protocol (MTP: 1:1:1 Balanced Packed Red Blood Cells : Fresh Frozen Plasma : Platelets)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class HematologyGuidelineEvaluation:
    guideline_source: str
    hematologic_syndrome: str
    risk_score_name: str
    risk_score_value: int
    probability_tier: str
    immediate_anticoagulation_changes: List[str]
    confirmatory_laboratory_workup: List[str]


class HematologyGuidelineEngine:
    """Evaluates platelet dynamics, coagulation factor assays, and microangiopathies."""

    @staticmethod
    def evaluate_hit_4ts_score(
        thrombocytopenia_drop_percent: float,  # >50% drop or nadir >=20k -> 2 pts
        timing_onset_days: int,                # 5-10 days after heparin -> 2 pts
        thrombosis_proven: bool,               # New proven thrombosis -> 2 pts
        other_causes_apparent: bool = False,   # No other cause -> 2 pts
    ) -> HematologyGuidelineEvaluation:
        """
        ASH 2018 Guidelines for Management of Venous Thromboembolism: Heparin-Induced Thrombocytopenia (HIT).
        4Ts Score: Thrombocytopenia, Timing, Thrombosis, oTher causes.
        """
        score = 0
        if thrombocytopenia_drop_percent >= 50.0:
            score += 2
        elif thrombocytopenia_drop_percent >= 30.0:
            score += 1

        if 5 <= timing_onset_days <= 10:
            score += 2
        elif timing_onset_days > 10:
            score += 1

        if thrombosis_proven:
            score += 2

        if not other_causes_apparent:
            score += 2
        else:
            score += 0

        if score >= 6:
            tier = "High Probability (6-8 Points)"
            actions = [
                "IMMEDIATELY CESSATE ALL HEPARIN PRODUCTS (including heparin flushes, LMWH, and heparin-coated catheters).",
                "Initiate Non-Heparin Direct Thrombin Inhibitor (Argatroban IV continuous infusion or Bivalirudin) at therapeutic doses (Class 1, Level A).",
                "Do NOT administer Warfarin until platelets have recovered to >= 150,000/uL (prevents warfarin-induced skin necrosis and venous limb gangrene).",
                "Order bilateral lower extremity duplex ultrasound to screen for occult DVT.",
            ]
        elif 4 <= score <= 5:
            tier = "Intermediate Probability (4-5 Points)"
            actions = [
                "Discontinue heparin and transition to non-heparin anticoagulant pending laboratory testing.",
                "Send Anti-PF4/Heparin ELISA and confirmatory Serotonin Release Assay (SRA).",
            ]
        else:
            tier = "Low Probability (0-3 Points)"
            actions = [
                "HIT is highly unlikely (<1% probability). Heparin may be safely continued while investigating alternative causes of thrombocytopenia.",
            ]

        return HematologyGuidelineEvaluation(
            guideline_source="ASH 2018 Guidelines for HIT",
            hematologic_syndrome="Heparin-Induced Thrombocytopenia (HIT)",
            risk_score_name="4Ts Score",
            risk_score_value=score,
            probability_tier=tier,
            immediate_anticoagulation_changes=actions,
            confirmatory_laboratory_workup=[
                "Anti-PF4/Heparin Optical Density (OD) ELISA (OD > 1.00 correlates with high specificity)",
                "Serotonin Release Assay (SRA - Gold Standard Functional Assay)",
            ],
        )
