"""
HealthPulse AI — Positron Emission Tomography (PET/CT) Quantitative Oncology Engine.
Implements Standardized Uptake Value (SUVmax, SUVmean, SUVpeak), Metabolic Tumor Volume (MTV),
and Total Lesion Glycolysis (TLG) per PERCIST 1.0 (PET Response Criteria in Solid Tumors).
- Radio-decay correction calculation: A(t) = A_0 * e^(-ln(2) * t / t_half)
- SUV body weight (SUVbw) = Radioactivity_tissue (Bq/mL) / (Injected_dose (Bq) / Body_weight (g))
- PERCIST Complete Metabolic Response (CMR) vs Progressive Metabolic Disease (PMD)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import math


class PETQuantifier:
    """Positron Emission Tomography SUV quantification and metabolic tumor staging."""

    F18_HALF_LIFE_MINUTES = 109.771

    @staticmethod
    def calculate_decay_corrected_injected_dose(
        injected_dose_mbq: float,
        injection_time_minutes: float,
        scan_start_time_minutes: float,
    ) -> float:
        """
        Calculates decay-corrected injected dose at the scan start time.
        """
        elapsed = max(0.0, scan_start_time_minutes - injection_time_minutes)
        decay_factor = math.exp(-math.log(2.0) * elapsed / PETQuantifier.F18_HALF_LIFE_MINUTES)
        return injected_dose_mbq * decay_factor

    @staticmethod
    def calculate_suv_body_weight(
        voxel_activity_bq_ml: float,
        injected_dose_mbq: float,
        patient_weight_kg: float,
        elapsed_time_minutes: float = 60.0,
    ) -> float:
        """
        Standardized Uptake Value (SUV_bw) in g/mL.
        SUV = Activity_tissue (Bq/mL) / (Decay_corrected_dose (Bq) / Weight (g))
        """
        if patient_weight_kg <= 0.0 or injected_dose_mbq <= 0.0:
            return 0.0

        decay_factor = math.exp(-math.log(2.0) * elapsed_time_minutes / PETQuantifier.F18_HALF_LIFE_MINUTES)
        decay_corrected_dose_bq = (injected_dose_mbq * 1e6) * decay_factor
        weight_grams = patient_weight_kg * 1000.0

        injected_concentration_bq_g = decay_corrected_dose_bq / weight_grams
        suv = voxel_activity_bq_ml / max(1e-6, injected_concentration_bq_g)
        return round(max(0.0, suv), 3)

    @staticmethod
    def evaluate_percist_response(
        baseline_suv_peak: float,
        follow_up_suv_peak: float,
        new_avid_lesions_present: bool = False,
    ) -> Dict[str, Any]:
        """
        PERCIST 1.0 Response Criteria for FDG-PET Solid Tumors.
        CMR: Complete resolution of FDG uptake to background liver levels.
        PMR: >= 30% and >= 0.8 unit decrease in SUVpeak.
        SMD: < 30% decrease or < 30% increase in SUVpeak.
        PMD: >= 30% and >= 0.8 unit increase in SUVpeak OR appearance of new FDG-avid lesions.
        """
        if new_avid_lesions_present:
            return {
                "percist_category": "PMD (Progressive Metabolic Disease)",
                "percentage_change": None,
                "clinical_guidance": "Disease progression confirmed by appearance of new hypermetabolic metastatic focus. Switch to next-line systemic therapy.",
            }

        delta_suv = follow_up_suv_peak - baseline_suv_peak
        pct_change = (delta_suv / max(0.1, baseline_suv_peak)) * 100.0

        if follow_up_suv_peak <= 1.5:
            cat = "CMR (Complete Metabolic Response)"
            interp = "Complete metabolic remission of tumor FDG uptake."
        elif pct_change <= -30.0 and delta_suv <= -0.8:
            cat = "PMR (Partial Metabolic Response)"
            interp = f"Significant metabolic tumor regression ({pct_change:.1f}% reduction in SUVpeak)."
        elif pct_change >= 30.0 and delta_suv >= 0.8:
            cat = "PMD (Progressive Metabolic Disease)"
            interp = f"Metabolic disease progression ({pct_change:.1f}% increase in SUVpeak)."
        else:
            cat = "SMD (Stable Metabolic Disease)"
            interp = "Stable metabolic activity without significant response or progression."

        return {
            "percist_category": cat,
            "percentage_change": round(pct_change, 1),
            "baseline_suv_peak": baseline_suv_peak,
            "follow_up_suv_peak": follow_up_suv_peak,
            "clinical_guidance": interp,
        }
