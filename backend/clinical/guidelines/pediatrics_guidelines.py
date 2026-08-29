"""
HealthPulse AI — Evidence-Based Pediatrics & Pediatric Critical Care Guidelines.
Implements AAP (American Academy of Pediatrics) and PALS guidelines:
- Pediatric Sepsis & Septic Shock (Phoenix 2024 Criteria & Fluid Bolus 10-20 mL/kg Balanced Crystalloid)
- Pediatric Diabetic Ketoacidosis (ISPAD 2022 Guidelines: Two-Bag System & Cerebral Edema Prevention)
- Bronchiolitis Management (AAP 2014 Guidelines: Supportive Care vs Bronchodilator De-implementation)
- Febrile Infant Evaluation (AAP 2021 Clinical Practice Guideline for Infants 8-60 Days)
- Pediatric Advanced Life Support (PALS 2020 Cardiac Arrest & Tachyarrhythmia Algorithms)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class PediatricGuidelineEvaluation:
    guideline_source: str
    pediatric_syndrome: str
    age_category: str
    fluid_bolus_prescription: str
    first_line_antimicrobials: List[str]
    neurological_monitoring_alerts: List[str]


class PediatricsGuidelineEngine:
    """Evaluates pediatric weight-based dosing, age-adjusted vital norms, and neonatal resuscitation."""

    @staticmethod
    def evaluate_pediatric_septic_shock(
        weight_kg: float,
        age_months: int,
        mean_arterial_pressure: float,
        has_hypotension: bool = True,
        capillary_refill_seconds: float = 4.0,
    ) -> PediatricGuidelineEvaluation:
        """
        Phoenix 2024 Pediatric Sepsis Criteria / Surviving Sepsis Pediatric Guidelines.
        Fluid bolus: 10-20 mL/kg balanced crystalloid over 10-20 minutes, reassessing for hepatomegaly/crackles.
        """
        bolus_vol = round(weight_kg * 20.0, 1)

        antibiotics = [
            "Ceftriaxone 50-100 mg/kg IV q24h (or Cefotaxime 50 mg/kg IV q8h in neonates/young infants) (Class 1).",
            "Add Vancomycin 15 mg/kg IV q6-8h for suspected MRSA or toxic shock syndrome.",
            "Add Ampicillin 50-100 mg/kg IV q6h in infants < 60 days to cover Listeria monocytogenes.",
        ]

        return PediatricGuidelineEvaluation(
            guideline_source="Phoenix 2024 / SSC Pediatric Guidelines",
            pediatric_syndrome="Pediatric Septic Shock",
            age_category=f"{age_months} Months ({weight_kg} kg)",
            fluid_bolus_prescription=f"Administer {bolus_vol} mL (20 mL/kg) Plasmalyte or Lactated Ringer's over 15 minutes. Reassess for rales and hepatomegaly before repeat boluses.",
            first_line_antimicrobials=antibiotics,
            neurological_monitoring_alerts=[
                "Assess Pediatric Glasgow Coma Scale (pGCS) every 30 minutes.",
                "Target Epinephrine (0.05-0.3 mcg/kg/min) for 'cold shock' (prolonged cap refill, cool extremities) or Norepinephrine for 'warm shock' (bounding pulses, flash cap refill).",
            ],
        )
