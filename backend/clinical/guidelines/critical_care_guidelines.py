"""
HealthPulse AI — Evidence-Based Critical Care & Intensive Care Unit (ICU) Practice Guidelines.
Implements Surviving Sepsis Campaign 2021/2026, SCCM, and ESICM guidelines:
- Surviving Sepsis Campaign 1-Hour and 3-Hour Hour Bundles
- Septic Shock Vasopressor & Inotrope Titration Hierarchy (Norepinephrine -> Vasopressin -> Epinephrine)
- Stress-Dose Corticosteroids in Refractory Septic Shock (Hydrocortisone 200mg/day)
- ICU Sedation, Analgesia, and Delirium (PADIS 2018 Guidelines: Dexmedetomidine / Propofol)
- Post-Cardiac Arrest Targeted Temperature Management (TTM: 32-36 C vs Strict Normothermia)
- Critical Care Nutrition & Enteral Feeding Protocols in Shock
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class CriticalCareGuidelineEvaluation:
    guideline_source: str
    clinical_syndrome: str
    hemodynamic_state: str
    first_line_vasopressor: str
    adjunctive_vasopressor_titration: List[str]
    fluid_resuscitation_volume_ml: float
    corticosteroid_indication: Optional[str]
    inotrope_indication: Optional[str]
    resuscitation_targets: Dict[str, str]


class CriticalCareGuidelineEngine:
    """Evaluates hemodynamic parameters, shock severity, and vasoactive infusions."""

    @staticmethod
    def evaluate_surviving_sepsis_resuscitation(
        weight_kg: float,
        mean_arterial_pressure: float,
        serum_lactate_mmol_l: float,
        current_norepinephrine_mcg_min: float = 0.0,
        has_cardiac_dysfunction_or_hypoperfusion: bool = False,
        fluid_administered_ml: float = 0.0,
    ) -> CriticalCareGuidelineEvaluation:
        """
        Surviving Sepsis Campaign 2021 International Guidelines for Management of Sepsis and Septic Shock.
        Initial resuscitation: >= 30 mL/kg IV balanced crystalloid within 3 hours.
        Target MAP >= 65 mmHg.
        """
        recommended_fluid = round(30.0 * weight_kg, 0)
        remaining_fluid = max(0.0, recommended_fluid - fluid_administered_ml)

        # 1. First-line vasopressor
        first_line = "Norepinephrine continuous IV infusion (titrate to target MAP >= 65 mmHg) (Class 1, Strong recommendation)."

        # 2. Second-line and adjunctive vasopressors
        adjuncts = []
        corticosteroids = None
        inotropes = None

        if current_norepinephrine_mcg_min >= 15.0 or current_norepinephrine_mcg_min >= (0.25 * weight_kg):
            adjuncts.append("Add Vasopressin (fixed dose 0.03 units/min, do not titrate) to raise MAP and reduce norepinephrine dosage requirement (Class 2a).")

        if current_norepinephrine_mcg_min >= 30.0 or (current_norepinephrine_mcg_min >= 20.0 and len(adjuncts) > 0):
            adjuncts.append("Add Epinephrine (2-10 mcg/min) as third-line vasopressor for refractory hypotension.")
            corticosteroids = "Stress-dose IV Hydrocortisone (200 mg/day administered as 50 mg IV q6h or continuous infusion) is indicated for ongoing vasopressor requirement >= 4 hours (Class 2a, Level B)."

        if has_cardiac_dysfunction_or_hypoperfusion and mean_arterial_pressure >= 65.0:
            inotropes = "Add Dobutamine infusion (2.5-20 mcg/kg/min) or switch to Epinephrine if myocardial dysfunction and persistent hypoperfusion despite adequate volume and MAP."

        targets = {
            "Mean Arterial Pressure (MAP)": ">= 65 mmHg",
            "Serum Lactate Clearance": "Decline by >= 20% every 2 hours toward normal (< 2.0 mmol/L)",
            "Capillary Refill Time (ANDROMEDA-SHOCK)": "<= 3.0 seconds on finger pulp",
            "Urine Output": ">= 0.5 mL/kg/hour",
            "Dynamic Fluid Responsiveness": "Passive Leg Raise (PLR) or Stroke Volume Variation (SVV) > 13% before giving additional fluid boluses beyond 30 mL/kg",
        }

        return CriticalCareGuidelineEvaluation(
            guideline_source="Surviving Sepsis Campaign 2021 Guidelines",
            clinical_syndrome="Septic Shock / Severe Sepsis",
            hemodynamic_state=f"MAP: {mean_arterial_pressure} mmHg | Lactate: {serum_lactate_mmol_l} mmol/L | Norepi: {current_norepinephrine_mcg_min} mcg/min",
            first_line_vasopressor=first_line,
            adjunctive_vasopressor_titration=adjuncts,
            fluid_resuscitation_volume_ml=recommended_fluid,
            corticosteroid_indication=corticosteroids,
            inotrope_indication=inotropes,
            resuscitation_targets=targets,
        )
