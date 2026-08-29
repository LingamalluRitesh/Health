"""
HealthPulse AI — ACMG/AMP 2015 Sequence Variant Pathogenicity Classifier.
Implements the Richards et al. rules combining very strong (PVS1), strong (PS1-4),
moderate (PM1-6), supporting (PP1-5), stand-alone benign (BA1), strong benign (BS1-4), and supporting benign (BP1-7).
"""

from typing import List, Dict, Any, Set
from dataclasses import dataclass
from enum import Enum


class PathogenicityClass(str, Enum):
    PATHOGENIC = "Pathogenic"
    LIKELY_PATHOGENIC = "Likely Pathogenic"
    UNCERTAIN_SIGNIFICANCE = "Variant of Uncertain Significance (VUS)"
    LIKELY_BENIGN = "Likely Benign"
    BENIGN = "Benign"


@dataclass
class ACMGClassificationResult:
    variant_id: str
    gene: str
    classification: PathogenicityClass
    pathogenic_criteria_met: List[str]
    benign_criteria_met: List[str]
    reasoning: str


class ACMGVariantClassifier:
    """Classifies genomic variants according to ACMG/AMP 2015 guidelines."""

    def classify_variant(
        self,
        variant_id: str,
        gene: str,
        criteria_codes: List[str],
    ) -> ACMGClassificationResult:
        """
        Applies standard combination rules to determine ACMG class:
        - Pathogenic:
          (i) 1 PVS1 AND (>=1 PS OR >=2 PM OR 1 PM + 1 PP OR >=2 PP)
          (ii) >=2 PS
          (iii) 1 PS AND (>=3 PM OR 2 PM + >=2 PP OR 1 PM + >=4 PP)
        - Likely Pathogenic:
          (i) 1 PVS1 AND 1 PM
          (ii) 1 PS AND 1-2 PM
          (iii) 1 PS AND >=2 PP
          (iv) >=3 PM
          (v) 2 PM AND >=2 PP
          (vi) 1 PM AND >=4 PP
        - Benign:
          (i) 1 BA1
          (ii) >=2 BS
        - Likely Benign:
          (i) 1 BS AND 1 BP
          (ii) >=2 BP
        - VUS: All other combinations or contradictory evidence
        """
        c_set = set(code.upper().strip() for code in criteria_codes)

        pvs = [c for c in c_set if c.startswith("PVS")]
        ps = [c for c in c_set if c.startswith("PS")]
        pm = [c for c in c_set if c.startswith("PM")]
        pp = [c for c in c_set if c.startswith("PP")]

        ba = [c for c in c_set if c.startswith("BA")]
        bs = [c for c in c_set if c.startswith("BS")]
        bp = [c for c in c_set if c.startswith("BP")]

        path_count = len(pvs) + len(ps) + len(pm) + len(pp)
        benign_count = len(ba) + len(bs) + len(bp)

        # Stand-alone benign rule
        if len(ba) >= 1:
            cls = PathogenicityClass.BENIGN
            reason = "Classified as Benign via stand-alone allele frequency criterion BA1 (>5% in gnomAD)."
        elif len(bs) >= 2:
            cls = PathogenicityClass.BENIGN
            reason = "Classified as Benign with >=2 strong benign criteria (BS)."
        elif (len(bs) >= 1 and len(bp) >= 1) or len(bp) >= 2:
            cls = PathogenicityClass.LIKELY_BENIGN
            reason = "Classified as Likely Benign with supporting benign criteria."
        elif path_count > 0 and benign_count > 0:
            # Conflicting evidence
            cls = PathogenicityClass.UNCERTAIN_SIGNIFICANCE
            reason = "Classified as VUS due to conflicting pathogenic and benign evidence criteria."
        # Pathogenic rules
        elif len(pvs) >= 1 and (len(ps) >= 1 or len(pm) >= 2 or (len(pm) >= 1 and len(pp) >= 1) or len(pp) >= 2):
            cls = PathogenicityClass.PATHOGENIC
            reason = "Classified as Pathogenic: PVS1 combined with strong/moderate evidence."
        elif len(ps) >= 2:
            cls = PathogenicityClass.PATHOGENIC
            reason = "Classified as Pathogenic: >= 2 Strong (PS) pathogenic criteria."
        elif len(ps) >= 1 and (len(pm) >= 3 or (len(pm) >= 2 and len(pp) >= 2) or (len(pm) >= 1 and len(pp) >= 4)):
            cls = PathogenicityClass.PATHOGENIC
            reason = "Classified as Pathogenic: PS combined with multiple moderate/supporting criteria."
        # Likely Pathogenic rules
        elif len(pvs) >= 1 and len(pm) >= 1:
            cls = PathogenicityClass.LIKELY_PATHOGENIC
            reason = "Classified as Likely Pathogenic: 1 PVS1 and 1 PM."
        elif len(ps) >= 1 and (1 <= len(pm) <= 2 or len(pp) >= 2):
            cls = PathogenicityClass.LIKELY_PATHOGENIC
            reason = "Classified as Likely Pathogenic: 1 PS combined with moderate/supporting criteria."
        elif len(pm) >= 3 or (len(pm) >= 2 and len(pp) >= 2) or (len(pm) >= 1 and len(pp) >= 4):
            cls = PathogenicityClass.LIKELY_PATHOGENIC
            reason = "Classified as Likely Pathogenic: Accumulation of moderate and supporting criteria."
        else:
            cls = PathogenicityClass.UNCERTAIN_SIGNIFICANCE
            reason = "Classified as VUS: Insufficient criteria met to establish pathogenicity or benign status."

        return ACMGClassificationResult(
            variant_id=variant_id,
            gene=gene,
            classification=cls,
            pathogenic_criteria_met=sorted(list(pvs + ps + pm + pp)),
            benign_criteria_met=sorted(list(ba + bs + bp)),
            reasoning=reason,
        )
