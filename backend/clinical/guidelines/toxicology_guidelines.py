"""
HealthPulse AI — Evidence-Based Medical Toxicology Clinical Practice Guidelines.
Implements ACMT (American College of Medical Toxicology) and AACT guidelines:
- Acetaminophen (APAP) Overdose & Rumack-Matthew Nomogram N-Acetylcysteine (NAC) 21-Hour IV Protocol
- Salicylate Overdose (Sodium Bicarbonate Urinary Alkalinization & Hemodialysis Criteria)
- Opioid Overdose (Naloxone Titrated Reversal to Maintain Airway without Precipitating Acute Withdrawal)
- Beta-Blocker & Calcium Channel Blocker Toxicity (High-Dose Insulin Euglycemia / HIE & IV Lipid Emulsion)
- Toxic Alcohol Poisoning (Fomepizole Loading / Maintenance & Hemodialysis Clearance)
- Digoxin Toxicity (Digoxin-Specific Antibody Fragments / DigiFab Dose Calculation)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import math


@dataclass
class ToxicologyGuidelineEvaluation:
    guideline_source: str
    toxic_ingestion: str
    antidote_indicated: bool
    antidote_prescription: str
    hemodialysis_indicated: bool
    monitoring_and_toxidrome_features: List[str]


class ToxicologyGuidelineEngine:
    """Evaluates drug levels, toxicokinetics, and specific antidote dosing."""

    @staticmethod
    def evaluate_acetaminophen_overdose(
        hours_post_ingestion: float,
        apap_level_mcg_ml: float,
        weight_kg: float,
        has_elevated_ast_alt: bool = False,
    ) -> ToxicologyGuidelineEvaluation:
        """
        Rumack-Matthew Nomogram evaluation for acute single ingestion of Acetaminophen.
        Treatment line starts at 150 mcg/mL at 4 hours post-ingestion with 4-hour half-life curve.
        """
        if hours_post_ingestion < 4.0:
            return ToxicologyGuidelineEvaluation(
                guideline_source="ACMT Acetaminophen Guidelines",
                toxic_ingestion="Acute Acetaminophen (APAP) Ingestion",
                antidote_indicated=False,
                antidote_prescription="Obtain 4-hour post-ingestion APAP concentration. Administer Oral Activated Charcoal (1 g/kg) if within 1-2 hours of ingestion.",
                hemodialysis_indicated=False,
                monitoring_and_toxidrome_features=["Repeat APAP concentration at 4 hours", "Baseline AST, ALT, Total Bilirubin, INR, and Creatinine"],
            )

        # Rumack-Matthew 150-line formula: Threshold(t) = 150 * 2^((4 - t) / 4)
        nomogram_threshold = 150.0 * math.pow(2.0, (4.0 - hours_post_ingestion) / 4.0)
        is_above_line = apap_level_mcg_ml >= nomogram_threshold or has_elevated_ast_alt

        if is_above_line:
            # 21-Hour IV NAC Protocol (3-Bag System or Simplified 2-Bag)
            # Bag 1: 150 mg/kg in 200mL D5W over 1 hour
            # Bag 2: 50 mg/kg in 500mL D5W over 4 hours
            # Bag 3: 100 mg/kg in 1000mL D5W over 16 hours
            nac_order = (
                f"N-ACETYLCYSTEINE (NAC) IV 21-Hour Protocol Indicated:\n"
                f"• Loading Dose: {round(weight_kg * 150.0)} mg IV in 200mL D5W over 60 minutes.\n"
                f"• Second Dose: {round(weight_kg * 50.0)} mg IV in 500mL D5W over 4 hours.\n"
                f"• Third Dose: {round(weight_kg * 100.0)} mg IV in 1000mL D5W over 16 hours.\n"
                f"Continue NAC beyond 21 hours until APAP undetectable, AST/ALT declining, and INR < 2.0."
            )
        else:
            nac_order = "APAP level falls below the Rumack-Matthew 150-line. NAC is not indicated at this time unless high-risk factors or repeated supratherapeutic ingestions."

        return ToxicologyGuidelineEvaluation(
            guideline_source="ACMT / Rumack-Matthew Nomogram",
            toxic_ingestion="Acute Acetaminophen (APAP) Ingestion",
            antidote_indicated=is_above_line,
            antidote_prescription=nac_order,
            hemodialysis_indicated=apap_level_mcg_ml > 900.0 or severe metabolic acidosis,
            monitoring_and_toxidrome_features=[
                f"Nomogram Cutoff at {hours_post_ingestion}h: {round(nomogram_threshold, 1)} mcg/mL (Patient Level: {apap_level_mcg_ml} mcg/mL)",
                "Monitor AST/ALT, INR, and Renal function every 12 hours",
                "Watch for anaphylactoid reaction to IV NAC (treat with diphenhydramine and slow infusion rate)",
            ],
        )
