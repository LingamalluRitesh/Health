"""
HealthPulse AI — Somatic Oncology Mutation & Precision Therapeutics Annotator.
Annotates driver oncogenes (EGFR, KRAS, BRAF, ALK, ROS1, RET, PIK3CA, BRCA1/2) with AMP/ASCO/CAP actionability tiers.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class OncologicActionabilityTier(str, Enum):
    TIER_I = "Tier I: Variants of Strong Clinical Significance (FDA-approved or NCCN guideline therapy)"
    TIER_II = "Tier II: Variants of Potential Clinical Significance (Off-label or clinical trials)"
    TIER_III = "Tier III: Variants of Unknown Clinical Significance (VUS)"
    TIER_IV = "Tier IV: Benign or Likely Benign Variants"


@dataclass
class SomaticAnnotationResult:
    gene: str
    protein_alteration: str
    cancer_type: str
    actionability_tier: OncologicActionabilityTier
    indicated_therapies: List[str]
    resistance_mechanisms: List[str]
    nccn_guideline_reference: str


class SomaticVariantAnnotator:
    """Clinical Cancer Genomics and Targeted Therapy Knowledge Base."""

    def __init__(self):
        self._knowledge_base: Dict[str, Dict[str, Any]] = {
            "BRAF:V600E": {
                "cancer_types": ["Melanoma", "Colorectal Cancer", "Non-Small Cell Lung Cancer", "Thyroid"],
                "tier": OncologicActionabilityTier.TIER_I,
                "therapies": ["Dabrafenib + Trametinib", "Encorafenib + Cetuximab (CRC)", "Vemurafenib"],
                "resistance": ["NRAS activating mutations", "MEK1/2 mutations", "PTEN loss"],
                "ref": "NCCN Melanoma & NSCLC Guidelines v2024",
            },
            "EGFR:L858R": {
                "cancer_types": ["Non-Small Cell Lung Cancer"],
                "tier": OncologicActionabilityTier.TIER_I,
                "therapies": ["Osimertinib (1st-line)", "Erlotinib", "Gefitinib", "Afatinib"],
                "resistance": ["EGFR T790M", "EGFR C797S", "MET amplification", "HER2 amplification"],
                "ref": "NCCN NSCLC Guidelines v2024",
            },
            "EGFR:T790M": {
                "cancer_types": ["Non-Small Cell Lung Cancer"],
                "tier": OncologicActionabilityTier.TIER_I,
                "therapies": ["Osimertinib (3rd-gen EGFR TKI)"],
                "resistance": ["EGFR C797S", "Small cell histologic transformation"],
                "ref": "FDA Approved Label Osimertinib",
            },
            "KRAS:G12C": {
                "cancer_types": ["Non-Small Cell Lung Cancer", "Colorectal Cancer"],
                "tier": OncologicActionabilityTier.TIER_I,
                "therapies": ["Sotorasib", "Adagrasib (+ Cetuximab in CRC)"],
                "resistance": ["Secondary KRAS mutations (Y96D, G12D)", "MET amplification"],
                "ref": "NCCN NSCLC & Colon Guidelines 2024",
            },
            "BRCA1:c.5266dupC": {
                "cancer_types": ["Breast Cancer", "Ovarian Cancer", "Pancreatic Cancer", "Prostate Cancer"],
                "tier": OncologicActionabilityTier.TIER_I,
                "therapies": ["Olaparib", "Talazoparib", "Rucaparib", "Niraparib", "Platinum Chemotherapy"],
                "resistance": ["BRCA1 reversion mutations restoring reading frame"],
                "ref": "NCCN Breast & Ovarian Cancer Guidelines 2024",
            },
        }

    def annotate(self, gene: str, alteration: str, cancer_type: str = "Pan-Cancer") -> SomaticAnnotationResult:
        key = f"{gene.upper().strip()}:{alteration.strip()}"
        if key in self._knowledge_base:
            data = self._knowledge_base[key]
            return SomaticAnnotationResult(
                gene=gene.upper(),
                protein_alteration=alteration,
                cancer_type=cancer_type,
                actionability_tier=data["tier"],
                indicated_therapies=data["therapies"],
                resistance_mechanisms=data["resistance"],
                nccn_guideline_reference=data["ref"],
            )

        # Fallback for novel variants
        return SomaticAnnotationResult(
            gene=gene.upper(),
            protein_alteration=alteration,
            cancer_type=cancer_type,
            actionability_tier=OncologicActionabilityTier.TIER_III,
            indicated_therapies=[],
            resistance_mechanisms=[],
            nccn_guideline_reference="Evaluate for basket or umbrella precision oncology clinical trials.",
        )
