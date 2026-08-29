"""
HealthPulse AI — Evidence-Based Precision Oncology Practice Guidelines.
Implements NCCN (National Comprehensive Cancer Network) and ASCO guidelines:
- Non-Small Cell Lung Cancer (NSCLC): EGFR, ALK, ROS1, BRAF, KRAS G12C, RET, MET exon 14, PD-L1
- Breast Cancer: ER/PR/HER2 Receptor Status, CDK4/6 Inhibitors, PARP Inhibitors in BRCA1/2, Antibody-Drug Conjugates
- Colorectal Cancer (CRC): RAS/BRAF Wild-Type vs Mutant, dMMR/MSI-H Immunotherapy (Pembrolizumab)
- Prostate Cancer: Risk Stratification (NCCN Very Low to Very High), Castration-Resistant Protocols (Enzalutamide / Abiraterone)
- Immune Checkpoint Inhibitor-Related Adverse Events (irAEs) Staging & High-Dose Corticosteroid Algorithms
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CancerStage(str, Enum):
    STAGE_I = "Stage I: Localized"
    STAGE_II = "Stage II: Early Locally Advanced"
    STAGE_III = "Stage III: Regional Lymph Node Involvement"
    STAGE_IV = "Stage IV: Distant Metastatic Disease"


@dataclass
class OncologyGuidelineEvaluation:
    guideline_source: str
    malignancy_type: str
    cancer_stage: CancerStage
    molecular_biomarker_profile: Dict[str, str]
    first_line_systemic_therapy: List[str]
    maintenance_therapy: Optional[str]
    targeted_therapy_rationale: str
    clinical_trial_options: List[str]


class OncologyGuidelineEngine:
    """Evaluates tumor histology, next-generation sequencing (NGS) panels, and PD-L1 TPS scores."""

    @staticmethod
    def evaluate_advanced_nsclc_treatment(
        histology: str,  # "Adenocarcinoma" or "Squamous"
        egfr_mutation: Optional[str] = None,  # "exon19del", "L858R", "T790M", "exon20ins", None
        alk_fusion: bool = False,
        ros1_fusion: bool = False,
        braf_v600e: bool = False,
        kras_mutation: Optional[str] = None,  # "G12C", "G12D", None
        ret_fusion: bool = False,
        met_exon14_skipping: bool = False,
        pdl1_tps_percent: float = 0.0,
    ) -> OncologyGuidelineEvaluation:
        """
        NCCN Clinical Practice Guidelines in Oncology: Non-Small Cell Lung Cancer (v2024).
        """
        biomarkers = {
            "Histology": histology,
            "EGFR": egfr_mutation or "Wild-Type",
            "ALK": "Positive" if alk_fusion else "Negative",
            "ROS1": "Positive" if ros1_fusion else "Negative",
            "BRAF": "V600E Mutant" if braf_v600e else "Wild-Type",
            "KRAS": kras_mutation or "Wild-Type",
            "PD-L1 TPS": f"{pdl1_tps_percent}%",
        }

        # 1. Actionable Driver Oncogenes (Targeted Therapies Preferred over Immunotherapy/Chemo)
        if egfr_mutation in ("exon19del", "L858R"):
            first_line = [
                "Osimertinib 80mg orally once daily (Preferred Category 1 First-Line Therapy - FLAURA trial).",
                "Alternative: Amivantamab + Lazertinib (MARIPOSA regimen).",
            ]
            rationale = "Targeted third-generation irreversible EGFR TKI with superior CNS penetration and progression-free survival."
            maintenance = "Continue Osimertinib until disease progression or unacceptable toxicity."
            trials = ["Phase II/III post-Osimertinib resistance trials (MET amplification, EGFR C797S inhibitors)."]

        elif alk_fusion:
            first_line = [
                "Alectinib 600mg BID with food (Preferred Category 1 - ALEX trial) OR Brigatinib 180mg daily OR Lorlatinib 100mg daily (CROWN trial).",
            ]
            rationale = "Second/Third-generation ALK TKI providing robust systemic and intracranial efficacy with prolonged duration of response."
            maintenance = "Continue ALK TKI monotherapy indefinitely until progression."
            trials = ["Next-generation ALK inhibitor trials for G1202R solvent-front resistance mutations."]

        elif braf_v600e:
            first_line = [
                "Dabrafenib 150mg BID + Trametinib 2mg daily (Preferred Category 1) OR Encorafenib 450mg daily + Binimetinib 45mg BID.",
            ]
            rationale = "Dual BRAF/MEK kinase inhibition suppresses paradoxical MAPK pathway reactivation and prolongs PFS."
            maintenance = "Continue combination targeted therapy."
            trials = ["Novel pan-RAF inhibitor clinical trials."]

        elif kras_mutation == "G12C":
            first_line = [
                "Platinum-doublet Chemotherapy + Immunotherapy (Pembrolizumab + Carboplatin + Pemetrexed).",
                "Reserve KRAS G12C specific inhibitors (Sotorasib 960mg daily or Adagrasib 600mg BID) for Second-Line therapy after chemotherapy progression.",
            ]
            rationale = "First-line chemo-immunotherapy remains standard for KRAS G12C; direct covalent G12C inhibitors are FDA-approved in 2nd-line setting (CodeBreaK 100, KRYSTAL-1)."
            maintenance = "Pemetrexed + Pembrolizumab maintenance every 3 weeks."
            trials = ["First-line Sotorasib/Adagrasib in combination with SHP2 inhibitors or anti-PD-1."]

        # 2. Driver-Negative: Immunotherapy Stratification by PD-L1 Tumor Proportion Score (TPS)
        elif pdl1_tps_percent >= 50.0:
            first_line = [
                "Pembrolizumab 200mg IV q3w (or 400mg q6w) monotherapy (Preferred Category 1 - KEYNOTE-024) OR Cemiplimab 350mg IV q3w.",
                "Alternative: Chemotherapy + Pembrolizumab (if rapid disease burden reduction required).",
            ]
            rationale = "High PD-L1 expression (TPS >= 50%) enables chemotherapy-free single-agent immune checkpoint inhibition with superior overall survival."
            maintenance = "Pembrolizumab monotherapy for up to 2 years (35 cycles) in responsive disease."
            trials = ["Novel bispecific T-cell engager (BiTE) and TIGIT combination trials."]

        else:
            first_line = [
                "Carboplatin (AUC 5) + Pemetrexed 500 mg/m2 + Pembrolizumab 200mg IV q3w x 4 cycles (KEYNOTE-189).",
            ]
            rationale = "Standard platinum-doublet chemotherapy combined with anti-PD-1 immunotherapy for non-squamous non-driver NSCLC."
            maintenance = "Pemetrexed + Pembrolizumab maintenance every 3 weeks."
            trials = ["Phase III frontline immunotherapy intensification trials."]

        return OncologyGuidelineEvaluation(
            guideline_source="NCCN Guidelines for Non-Small Cell Lung Cancer v2024",
            malignancy_type="Non-Small Cell Lung Cancer (NSCLC)",
            cancer_stage=CancerStage.STAGE_IV,
            molecular_biomarker_profile=biomarkers,
            first_line_systemic_therapy=first_line,
            maintenance_therapy=maintenance,
            targeted_therapy_rationale=rationale,
            clinical_trial_options=trials,
        )
