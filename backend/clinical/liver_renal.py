"""
HealthPulse AI — Hepatic, Cirrhosis, and Renal Function Calculators.
Implements MELD, MELD-Na, Child-Pugh Class, CKD-EPI 2021 (race-free) eGFR, and Cockcroft-Gault CrCl.
"""

import math
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class MELDScoreResult:
    meld_original: float
    meld_na: float
    three_month_mortality_percent: float
    unos_tier: str
    interpretation: str


def calculate_meld_score(
    serum_creatinine_mg_dl: float,
    serum_bilirubin_mg_dl: float,
    inr: float,
    serum_sodium_meq_l: Optional[float] = None,
    on_dialysis_twice_past_week: bool = False,
) -> MELDScoreResult:
    """
    MELD (Model for End-Stage Liver Disease) and MELD-Na (Kamath et al., Hepatology 2007).
    """
    # Lower bound 1.0 for all parameters
    cr = 4.0 if on_dialysis_twice_past_week else max(1.0, min(serum_creatinine_mg_dl, 4.0))
    bili = max(1.0, serum_bilirubin_mg_dl)
    inr_val = max(1.0, inr)

    # Standard MELD formula
    meld_score = 9.57 * math.log(cr) + 3.78 * math.log(bili) + 11.2 * math.log(inr_val) + 6.43
    meld_rounded = round(max(6.0, min(40.0, meld_score)), 1)

    # MELD-Na formula
    meld_na_rounded = meld_rounded
    if serum_sodium_meq_l is not None and meld_rounded > 11.0:
        na = max(125.0, min(137.0, serum_sodium_meq_l))
        meld_na = meld_rounded + 1.32 * (137.0 - na) - (0.033 * meld_rounded * (137.0 - na))
        meld_na_rounded = round(max(6.0, min(40.0, meld_na)), 1)

    # 3-Month mortality estimate
    if meld_na_rounded >= 40:
        mortality = 71.3
        tier = "Tier 1A / Urgent (Highest Priority)"
    elif meld_na_rounded >= 30:
        mortality = 52.6
        tier = "Tier 1B (High Priority)"
    elif meld_na_rounded >= 20:
        mortality = 19.6
        tier = "Tier 2 (Moderate Priority)"
    elif meld_na_rounded >= 10:
        mortality = 6.0
        tier = "Tier 3 (Elective Monitoring)"
    else:
        mortality = 1.9
        tier = "Tier 4 (Low Priority)"

    return MELDScoreResult(
        meld_original=meld_rounded,
        meld_na=meld_na_rounded,
        three_month_mortality_percent=mortality,
        unos_tier=tier,
        interpretation=f"MELD-Na Score: {meld_na_rounded} (Estimated 3-Month Waitlist Mortality: {mortality}%)",
    )


def calculate_child_pugh(
    total_bilirubin_mg_dl: float,
    serum_albumin_g_dl: float,
    inr: float,
    ascites: str,            # "none", "slight", "moderate"
    encephalopathy_grade: int,  # 0: None, 1-2: Grade 1-2, 3-4: Grade 3-4
) -> Dict[str, Any]:
    """
    Child-Pugh Classification for Cirrhosis Severity (Score 5-15, Class A/B/C).
    """
    score = 0

    # Bilirubin (mg/dL)
    if total_bilirubin_mg_dl < 2.0:
        score += 1
    elif 2.0 <= total_bilirubin_mg_dl <= 3.0:
        score += 2
    else:
        score += 3

    # Serum Albumin (g/dL)
    if serum_albumin_g_dl > 3.5:
        score += 1
    elif 2.8 <= serum_albumin_g_dl <= 3.5:
        score += 2
    else:
        score += 3

    # INR
    if inr < 1.7:
        score += 1
    elif 1.7 <= inr <= 2.2:
        score += 2
    else:
        score += 3

    # Ascites
    asc_map = {"none": 1, "slight": 2, "moderate": 3, "severe": 3}
    score += asc_map.get(ascites.lower(), 1)

    # Encephalopathy
    if encephalopathy_grade == 0:
        score += 1
    elif 1 <= encephalopathy_grade <= 2:
        score += 2
    else:
        score += 3

    if score <= 6:
        child_class = "Class A (Well-compensated)"
        one_year_survival = 100.0
        two_year_survival = 85.0
    elif score <= 9:
        child_class = "Class B (Significant functional compromise)"
        one_year_survival = 80.0
        two_year_survival = 60.0
    else:
        child_class = "Class C (Decompensated cirrhosis)"
        one_year_survival = 45.0
        two_year_survival = 35.0

    return {
        "score": score,
        "child_pugh_class": child_class,
        "one_year_survival_percent": one_year_survival,
        "two_year_survival_percent": two_year_survival,
    }


def calculate_ckd_epi_egfr(
    serum_creatinine_mg_dl: float,
    age: int,
    gender: str,
) -> Dict[str, Any]:
    """
    2021 CKD-EPI (Chronic Kidney Disease Epidemiology Collaboration) Race-Free Equation
    (Inker et al., NEJM 2021).
    """
    is_female = gender.lower() == "female"
    scr = max(0.1, serum_creatinine_mg_dl)

    if is_female:
        kappa = 0.7
        alpha = -0.241
        gender_multiplier = 1.012
    else:
        kappa = 0.9
        alpha = -0.302
        gender_multiplier = 1.0

    min_ratio = min(scr / kappa, 1.0)
    max_ratio = max(scr / kappa, 1.0)

    egfr = (
        142.0
        * math.pow(min_ratio, alpha)
        * math.pow(max_ratio, -1.200)
        * math.pow(0.9938, age)
        * gender_multiplier
    )
    egfr_rounded = round(egfr, 1)

    if egfr_rounded >= 90:
        stage = "G1 - Normal or high kidney function"
    elif egfr_rounded >= 60:
        stage = "G2 - Mildly decreased"
    elif egfr_rounded >= 45:
        stage = "G3a - Mildly to moderately decreased"
    elif egfr_rounded >= 30:
        stage = "G3b - Moderately to severely decreased"
    elif egfr_rounded >= 15:
        stage = "G4 - Severely decreased"
    else:
        stage = "G5 - Kidney failure (ESRD)"

    return {
        "egfr_ml_min_1_73m2": egfr_rounded,
        "ckd_stage": stage,
        "equation": "CKD-EPI 2021 (Race-Free Refit)",
    }


def calculate_cockcroft_gault(
    serum_creatinine_mg_dl: float,
    age: int,
    weight_kg: float,
    gender: str,
) -> float:
    """
    Cockcroft-Gault formula for Creatinine Clearance (CrCl mL/min) used in pharmacological dosing.
    """
    scr = max(0.1, serum_creatinine_mg_dl)
    is_female = gender.lower() == "female"

    crcl = ((140.0 - age) * weight_kg) / (72.0 * scr)
    if is_female:
        crcl *= 0.85

    return round(crcl, 1)
