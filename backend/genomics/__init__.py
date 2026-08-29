"""
HealthPulse AI — Precision Genomics, Pharmacogenomics (PGx) and Molecular Pathology Module.
Provides VCF variant parsing, CPIC guidelines engine, Polygenic Risk Scoring, and ACMG classification.
"""

from backend.genomics.vcf_parser import (
    VCFRecord,
    VCFHeader,
    parse_vcf_text,
)
from backend.genomics.pharmacogenomics import (
    PharmacogenomicsEngine,
    PGxGuidelineResult,
    MetabolizerPhenotype,
)
from backend.genomics.polygenic_risk import (
    PolygenicRiskEngine,
    PolygenicScoreResult,
)
from backend.genomics.acmg_classifier import (
    ACMGVariantClassifier,
    ACMGClassificationResult,
    PathogenicityClass,
)
from backend.genomics.somatic_oncology import (
    SomaticVariantAnnotator,
    OncologicActionabilityTier,
)

__all__ = [
    "VCFRecord",
    "VCFHeader",
    "parse_vcf_text",
    "PharmacogenomicsEngine",
    "PGxGuidelineResult",
    "MetabolizerPhenotype",
    "PolygenicRiskEngine",
    "PolygenicScoreResult",
    "ACMGVariantClassifier",
    "ACMGClassificationResult",
    "PathogenicityClass",
    "SomaticVariantAnnotator",
    "OncologicActionabilityTier",
]
