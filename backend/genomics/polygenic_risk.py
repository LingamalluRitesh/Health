"""
HealthPulse AI — Polygenic Risk Score (PRS) Calculation Engine.
Aggregates genome-wide association study (GWAS) effect sizes across susceptibility loci
to estimate percentiles and lifetime relative risks for complex diseases.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class PolygenicScoreResult:
    disease_trait: str
    raw_prs_score: float
    population_percentile: float
    relative_risk: float
    risk_category: str
    num_variants_evaluated: int
    recommendation: str


class PolygenicRiskEngine:
    """Calculates additive polygenic scores from patient genotype calls."""

    def __init__(self):
        # Sample GWAS effect weights: (rsID: {effect_allele, beta_weight})
        self._cad_weights: Dict[str, Dict[str, Any]] = {
            "rs10757274": {"allele": "G", "beta": 0.28, "gene": "9p21.3 / CDKN2B-AS1"},
            "rs1333049":  {"allele": "C", "beta": 0.24, "gene": "9p21.3"},
            "rs6903956":  {"allele": "A", "beta": 0.18, "gene": "ADTRP"},
            "rs11556924": {"allele": "C", "beta": 0.15, "gene": "ZC3HC1"},
            "rs9982601":  {"allele": "T", "beta": 0.17, "gene": "SLC5A3"},
            "rs20455":    {"allele": "G", "beta": 0.12, "gene": "KIF6"},
            "rs17465637": {"allele": "C", "beta": 0.14, "gene": "MIA3"},
            "rs1746048":  {"allele": "C", "beta": 0.13, "gene": "CXCL12"},
            "rs6725887":  {"allele": "T", "beta": 0.14, "gene": "WDR12"},
            "rs12190287": {"allele": "C", "beta": 0.19, "gene": "TCF21"},
        }
        self._t2d_weights: Dict[str, Dict[str, Any]] = {
            "rs7903146":  {"allele": "T", "beta": 0.35, "gene": "TCF7L2"},
            "rs1801282":  {"allele": "G", "beta": 0.14, "gene": "PPARG"},
            "rs5219":     {"allele": "T", "beta": 0.15, "gene": "KCNJ11"},
            "rs10811661": {"allele": "T", "beta": 0.18, "gene": "CDKN2A/2B"},
            "rs4402960":  {"allele": "T", "beta": 0.14, "gene": "IGF2BP2"},
            "rs13266634": {"allele": "T", "beta": 0.15, "gene": "SLC30A8"},
        }

    def _calc_raw_prs(self, patient_genotypes: Dict[str, str], weight_db: Dict[str, Dict[str, Any]]) -> Tuple[float, int]:
        """Calculates weighted sum: PRS = sum(beta_i * dosage_i)."""
        prs = 0.0
        count = 0

        for rsid, meta in weight_db.items():
            if rsid in patient_genotypes:
                gt = patient_genotypes[rsid].upper()
                eff_allele = meta["allele"].upper()
                dosage = gt.count(eff_allele)
                prs += meta["beta"] * dosage
                count += 1

        return prs, count

    def calculate_cad_prs(self, patient_genotypes: Dict[str, str]) -> PolygenicScoreResult:
        """Calculates CAD (Coronary Artery Disease) polygenic risk score."""
        raw_score, count = self._calc_raw_prs(patient_genotypes, self._cad_weights)
        
        # Approximate standard normal Z-score assuming mean=1.2, std=0.6
        z_score = (raw_score - 1.2) / 0.6
        percentile = round(0.5 * (1.0 + math.erf(z_score / math.sqrt(2.0))) * 100.0, 1)
        rr = round(math.exp(0.35 * z_score), 2)

        if percentile >= 80.0:
            cat = "High Genetic Risk (Top 20%)"
            rec = "Intensive lifestyle coaching, early screening (Coronary Artery Calcium scan), and lower LDL-C threshold."
        elif percentile <= 20.0:
            cat = "Low Genetic Risk (Bottom 20%)"
            rec = "Standard primary prevention guidelines."
        else:
            cat = "Average Genetic Risk"
            rec = "Routine cardiovascular health maintenance."

        return PolygenicScoreResult(
            disease_trait="Coronary Artery Disease (CAD)",
            raw_prs_score=round(raw_score, 3),
            population_percentile=percentile,
            relative_risk=rr,
            risk_category=cat,
            num_variants_evaluated=count,
            recommendation=rec,
        )

    def calculate_t2d_prs(self, patient_genotypes: Dict[str, str]) -> PolygenicScoreResult:
        """Calculates Type 2 Diabetes Mellitus polygenic risk score."""
        raw_score, count = self._calc_raw_prs(patient_genotypes, self._t2d_weights)
        z_score = (raw_score - 0.9) / 0.45
        percentile = round(0.5 * (1.0 + math.erf(z_score / math.sqrt(2.0))) * 100.0, 1)
        rr = round(math.exp(0.30 * z_score), 2)

        if percentile >= 80.0:
            cat = "High Genetic Risk"
            rec = "Annual fasting glucose and HbA1c screening; structured diabetes prevention lifestyle program."
        else:
            cat = "Average / Low Genetic Risk"
            rec = "Routine preventative metabolic screening."

        return PolygenicScoreResult(
            disease_trait="Type 2 Diabetes Mellitus (T2D)",
            raw_prs_score=round(raw_score, 3),
            population_percentile=percentile,
            relative_risk=rr,
            risk_category=cat,
            num_variants_evaluated=count,
            recommendation=rec,
        )
