"""
HealthPulse AI — Pharmacogenomics (PGx) and CPIC Guideline Rules Engine.
Translates patient star-allele diplotypes into metabolizer phenotypes and CPIC Level A dosing recommendations.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class MetabolizerPhenotype(str, Enum):
    ULTRA_RAPID = "Ultra-rapid Metabolizer (UM)"
    RAPID = "Rapid Metabolizer (RM)"
    NORMAL = "Normal Metabolizer (NM)"
    INTERMEDIATE = "Intermediate Metabolizer (IM)"
    POOR = "Poor Metabolizer (PM)"
    INDETERMINATE = "Indeterminate"


@dataclass
class PGxGuidelineResult:
    gene: str
    diplotype: str
    phenotype: MetabolizerPhenotype
    drug: str
    cpic_level: str
    clinical_implication: str
    dosing_recommendation: str
    therapeutic_alternatives: List[str]


class PharmacogenomicsEngine:
    """CPIC (Clinical Pharmacogenetics Implementation Consortium) Rule Interpreter."""

    def __init__(self):
        self._cyp2d6_activity_scores: Dict[str, float] = {
            "*1": 1.0,
            "*2": 1.0,
            "*3": 0.0,
            "*4": 0.0,
            "*5": 0.0,
            "*6": 0.0,
            "*9": 0.5,
            "*10": 0.25,
            "*17": 0.5,
            "*41": 0.5,
            "*1xN": 2.0,
            "*2xN": 2.0,
        }

    def infer_cyp2d6_phenotype(self, allele1: str, allele2: str) -> MetabolizerPhenotype:
        """Calculates CYP2D6 total activity score (AS) and translates to consensus phenotype."""
        a1 = self._cyp2d6_activity_scores.get(allele1, 1.0)
        a2 = self._cyp2d6_activity_scores.get(allele2, 1.0)
        total_as = a1 + a2

        if total_as > 2.25:
            return MetabolizerPhenotype.ULTRA_RAPID
        elif 1.25 <= total_as <= 2.25:
            return MetabolizerPhenotype.NORMAL
        elif 0.25 <= total_as < 1.25:
            return MetabolizerPhenotype.INTERMEDIATE
        elif total_as == 0.0:
            return MetabolizerPhenotype.POOR
        return MetabolizerPhenotype.INDETERMINATE

    def evaluate_codeine_cyp2d6(self, diplotype: str) -> PGxGuidelineResult:
        """CPIC Guideline for Codeine & Tramadol based on CYP2D6."""
        parts = diplotype.split("/")
        a1 = parts[0] if len(parts) > 0 else "*1"
        a2 = parts[1] if len(parts) > 1 else "*1"
        phenotype = self.infer_cyp2d6_phenotype(a1, a2)

        if phenotype == MetabolizerPhenotype.ULTRA_RAPID:
            implication = "Increased conversion to morphine leading to toxic systemic concentrations and life-threatening respiratory depression."
            rec = "AVOID codeine and tramadol. High risk of severe opioid toxicity."
            alts = ["Morphine (direct)", "Hydromorphone", "Non-opioid analgesics (Acetaminophen, NSAIDs)"]
        elif phenotype == MetabolizerPhenotype.POOR:
            implication = "Greatly reduced morphine formation resulting in lack of analgesia."
            rec = "AVOID codeine and tramadol due to lack of efficacy."
            alts = ["Morphine", "Oxycodone (monitor response)", "Hydromorphone"]
        elif phenotype == MetabolizerPhenotype.INTERMEDIATE:
            implication = "Reduced morphine formation; may experience decreased analgesic response."
            rec = "Use standard starting dose; if inadequate analgesia, switch to non-CYP2D6 metabolized opioid."
            alts = ["Morphine", "Hydromorphone"]
        else:
            implication = "Expected normal rate of bioactivation to active morphine."
            rec = "Initiate standard labeled dose of codeine."
            alts = []

        return PGxGuidelineResult(
            gene="CYP2D6",
            diplotype=diplotype,
            phenotype=phenotype,
            drug="Codeine",
            cpic_level="Level A",
            clinical_implication=implication,
            dosing_recommendation=rec,
            therapeutic_alternatives=alts,
        )

    def evaluate_clopidogrel_cyp2c19(self, diplotype: str) -> PGxGuidelineResult:
        """CPIC Guideline for Clopidogrel based on CYP2C19."""
        # *17 = increased function, *2/*3 = loss of function
        if "*2/*2" in diplotype or "*3/*3" in diplotype or "*2/*3" in diplotype:
            phenotype = MetabolizerPhenotype.POOR
            implication = "Severely reduced active metabolite generation; significantly higher risk of stent thrombosis and recurrent ischemic stroke."
            rec = "AVOID clopidogrel. Prescribe alternative P2Y12 inhibitor at standard dose."
            alts = ["Prasugrel (if no TIA/stroke history)", "Ticagrelor"]
        elif "*2" in diplotype or "*3" in diplotype:
            phenotype = MetabolizerPhenotype.INTERMEDIATE
            implication = "Reduced active metabolite generation; elevated risk of adverse cardiovascular events."
            rec = "AVOID clopidogrel for acute coronary syndromes (ACS); use alternative P2Y12 inhibitor."
            alts = ["Ticagrelor", "Prasugrel"]
        elif "*17/*17" in diplotype or "*1/*17" in diplotype:
            phenotype = MetabolizerPhenotype.ULTRA_RAPID
            implication = "Enhanced active metabolite generation; standard antiplatelet efficacy."
            rec = "Prescribe standard label dose of clopidogrel."
            alts = []
        else:
            phenotype = MetabolizerPhenotype.NORMAL
            implication = "Normal antiplatelet response."
            rec = "Prescribe standard label dose of clopidogrel (75 mg/day)."
            alts = []

        return PGxGuidelineResult(
            gene="CYP2C19",
            diplotype=diplotype,
            phenotype=phenotype,
            drug="Clopidogrel",
            cpic_level="Level A",
            clinical_implication=implication,
            dosing_recommendation=rec,
            therapeutic_alternatives=alts,
        )

    def evaluate_fluoropyrimidine_dpyd(self, variants_detected: List[str]) -> PGxGuidelineResult:
        """CPIC Guideline for 5-Fluorouracil / Capecitabine based on DPYD (Dihydropyrimidine Dehydrogenase)."""
        has_c1905_1g_a = "*2A" in variants_detected or "c.1905+1G>A" in variants_detected
        has_c1679t_g = "*13" in variants_detected or "c.1679T>G" in variants_detected
        has_c2846a_t = "c.2846A>T" in variants_detected

        if has_c1905_1g_a or has_c1679t_g:
            phenotype = MetabolizerPhenotype.POOR
            implication = "Complete or near-complete DPD deficiency leading to lethal 5-FU accumulation, mucositis, neutropenia, and neurotoxicity."
            rec = "AVOID 5-Fluorouracil and Capecitabine. If strongly indicated, reduce starting dose by >= 75% under close PK monitoring."
            alts = ["Alternative non-fluoropyrimidine chemotherapy regimen"]
        elif has_c2846a_t:
            phenotype = MetabolizerPhenotype.INTERMEDIATE
            implication = "Partial DPD deficiency with increased risk of severe toxicity."
            rec = "Reduce starting dose of 5-FU / Capecitabine by 50%. Titrate based on toxicity."
            alts = []
        else:
            phenotype = MetabolizerPhenotype.NORMAL
            implication = "Normal DPD enzymatic activity."
            rec = "Use standard guideline dosing for 5-FU / Capecitabine."
            alts = []

        return PGxGuidelineResult(
            gene="DPYD",
            diplotype=",".join(variants_detected) if variants_detected else "WT/WT",
            phenotype=phenotype,
            drug="Fluorouracil (5-FU)",
            cpic_level="Level A",
            clinical_implication=implication,
            dosing_recommendation=rec,
            therapeutic_alternatives=alts,
        )
