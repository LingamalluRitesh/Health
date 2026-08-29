"""
HealthPulse AI — Pulmonary, Thromboembolism, Neurological, and Pediatric Early Warning Calculators.
Implements CURB-65, Wells DVT / PE criteria, NIHSS stroke scale, Glasgow Coma Scale, and PEWS.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


def calculate_curb65(
    confusion: bool,
    bun_mg_dl: float,             # BUN > 19 mg/dL (or urea > 7 mmol/L)
    respiratory_rate: float,      # RR >= 30
    systolic_bp: float,           # SBP < 90
    diastolic_bp: float,          # DBP <= 60
    age: int,                     # Age >= 65
) -> Dict[str, Any]:
    """
    CURB-65 Score for Community-Acquired Pneumonia Severity.
    """
    c_flag = confusion
    u_flag = bun_mg_dl > 19.0
    r_flag = respiratory_rate >= 30.0
    b_flag = systolic_bp < 90.0 or diastolic_bp <= 60.0
    a_flag = age >= 65

    score = int(c_flag) + int(u_flag) + int(r_flag) + int(b_flag) + int(a_flag)

    mortality_table = {0: 0.6, 1: 2.7, 2: 6.8, 3: 14.0, 4: 27.8, 5: 27.8}
    mortality = mortality_table.get(score, 27.8)

    if score <= 1:
        site = "Outpatient management suitable"
        risk = "Low risk"
    elif score == 2:
        site = "Short inpatient stay or supervised outpatient"
        risk = "Moderate risk"
    else:
        site = "Inpatient hospitalization required; assess for ICU admission if score 4-5"
        risk = "Severe / High risk"

    return {
        "score": score,
        "risk_level": risk,
        "estimated_30day_mortality_percent": mortality,
        "recommended_site_of_care": site,
        "criteria": {
            "confusion": c_flag,
            "uremia": u_flag,
            "respiratory_rate": r_flag,
            "blood_pressure": b_flag,
            "age_65": a_flag,
        },
    }


def calculate_wells_dvt(
    active_cancer: bool = False,
    paralysis_or_immobilization_lower_limb: bool = False,
    bedridden_over_3_days_or_major_surgery: bool = False,
    localized_tenderness_deep_venous_system: bool = False,
    entire_leg_swollen: bool = False,
    calf_swelling_3cm_larger: bool = False,
    pitting_edema_confined_symptomatic_leg: bool = False,
    collateral_superficial_veins_non_varicose: bool = False,
    previously_documented_dvt: bool = False,
    alternative_diagnosis_at_least_as_likely: bool = False,
) -> Dict[str, Any]:
    """
    Wells' Criteria for Deep Vein Thrombosis (DVT).
    """
    score = (
        int(active_cancer)
        + int(paralysis_or_immobilization_lower_limb)
        + int(bedridden_over_3_days_or_major_surgery)
        + int(localized_tenderness_deep_venous_system)
        + int(entire_leg_swollen)
        + int(calf_swelling_3cm_larger)
        + int(pitting_edema_confined_symptomatic_leg)
        + int(collateral_superficial_veins_non_varicose)
        + int(previously_documented_dvt)
        - (2 if alternative_diagnosis_at_least_as_likely else 0)
    )

    if score >= 3:
        prob = "High Probability (~75%)"
        rec = "Order urgent compression ultrasound of lower extremity."
    elif 1 <= score <= 2:
        prob = "Moderate Probability (~17%)"
        rec = "Order high-sensitivity D-dimer or ultrasound."
    else:
        prob = "Low Probability (~3%)"
        rec = "High-sensitivity D-dimer test can rule out DVT if negative."

    return {
        "score": score,
        "probability_tier": prob,
        "recommendation": rec,
    }


def calculate_wells_pe(
    clinical_signs_symptoms_dvt: bool = False,         # +3.0
    pe_most_likely_or_equal_to_alternative: bool = False,  # +3.0
    heart_rate_over_100: bool = False,                 # +1.5
    immobilization_surgery_past_4_weeks: bool = False,  # +1.5
    previous_dvt_or_pe: bool = False,                  # +1.5
    hemoptysis: bool = False,                          # +1.0
    malignancy_with_active_treatment: bool = False,    # +1.0
) -> Dict[str, Any]:
    """
    Wells' Criteria for Pulmonary Embolism (PE).
    """
    score = (
        (3.0 if clinical_signs_symptoms_dvt else 0.0)
        + (3.0 if pe_most_likely_or_equal_to_alternative else 0.0)
        + (1.5 if heart_rate_over_100 else 0.0)
        + (1.5 if immobilization_surgery_past_4_weeks else 0.0)
        + (1.5 if previous_dvt_or_pe else 0.0)
        + (1.0 if hemoptysis else 0.0)
        + (1.0 if malignancy_with_active_treatment else 0.0)
    )

    is_pe_likely = score > 4.0

    return {
        "score": round(score, 1),
        "is_pe_likely": is_pe_likely,
        "recommendation": (
            "PE Likely (>4.0): Perform CT Pulmonary Angiography (CTPA) STAT."
            if is_pe_likely
            else "PE Unlikely (<=4.0): Consider high-sensitivity D-dimer test."
        ),
    }


def calculate_nihss_score(
    level_of_consciousness: int = 0,         # 0-3
    loc_questions: int = 0,                  # 0-2
    loc_commands: int = 0,                   # 0-2
    best_gaze: int = 0,                      # 0-2
    visual_fields: int = 0,                  # 0-3
    facial_palsy: int = 0,                   # 0-3
    motor_arm_left: int = 0,                 # 0-4
    motor_arm_right: int = 0,                # 0-4
    motor_leg_left: int = 0,                 # 0-4
    motor_leg_right: int = 0,                # 0-4
    limb_ataxia: int = 0,                    # 0-2
    sensory: int = 0,                        # 0-2
    best_language: int = 0,                  # 0-3
    dysarthria: int = 0,                     # 0-2
    extinction_inattention: int = 0,         # 0-2
) -> Dict[str, Any]:
    """
    National Institutes of Health Stroke Scale (NIHSS) score (0-42).
    """
    total = (
        level_of_consciousness
        + loc_questions
        + loc_commands
        + best_gaze
        + visual_fields
        + facial_palsy
        + motor_arm_left
        + motor_arm_right
        + motor_leg_left
        + motor_leg_right
        + limb_ataxia
        + sensory
        + best_language
        + dysarthria
        + extinction_inattention
    )

    if total == 0:
        sev = "No stroke symptoms"
    elif 1 <= total <= 4:
        sev = "Minor stroke"
    elif 5 <= total <= 15:
        sev = "Moderate stroke"
    elif 16 <= total <= 20:
        sev = "Moderate to severe stroke"
    else:
        sev = "Severe stroke"

    thrombolysis_candidate = 4 <= total <= 25

    return {
        "total_nihss": total,
        "stroke_severity": sev,
        "iv_thrombolysis_candidate": thrombolysis_candidate,
        "recommendation": (
            "Urgent Endovascular Thrombectomy (EVT) / Thrombolytic Evaluation: Large vessel occlusion screening."
            if total >= 6
            else "Standard acute stroke pathway."
        ),
    }


def calculate_glasgow_coma_scale(
    eye_opening: int,       # 1-4
    verbal_response: int,   # 1-5
    motor_response: int,    # 1-6
) -> Dict[str, Any]:
    """
    Glasgow Coma Scale (GCS) (3-15).
    """
    eye = max(1, min(4, eye_opening))
    verbal = max(1, min(5, verbal_response))
    motor = max(1, min(6, motor_response))
    total = eye + verbal + motor

    if total <= 8:
        tbi_sev = "Severe Head Injury / Coma (Intubation strongly indicated)"
    elif 9 <= total <= 12:
        tbi_sev = "Moderate Head Injury"
    else:
        tbi_sev = "Mild Head Injury"

    return {
        "gcs_total": total,
        "eye_opening": eye,
        "verbal_response": verbal,
        "motor_response": motor,
        "tbi_severity": tbi_sev,
    }


def calculate_pews_score(
    behavior_score: int,      # 0: Playing/appropriate, 1: Sleeping, 2: Irritable, 3: Lethargic
    cardiovascular_score: int,# 0: Pink/cap refill 1-2s, 1: Pale/cap refill 3s, 2: Grey/cap refill 4s/tachy, 3: Mottled/cap refill 5s
    respiratory_score: int,   # 0: Normal, 1: >10 above norm/subcostal retractions, 2: >20 above norm/recessions, 3: >30 above norm/grunting
) -> Dict[str, Any]:
    """
    Pediatric Early Warning Score (PEWS) (0-9).
    """
    score = behavior_score + cardiovascular_score + respiratory_score
    if score >= 5:
        urgency = "High Urgency: Urgent pediatric critical care / medical response team review."
    elif 3 <= score <= 4:
        urgency = "Moderate Urgency: Notify senior resident / charge nurse, increase monitoring frequency."
    else:
        urgency = "Low Urgency: Routine observation."

    return {
        "pews_score": score,
        "action_required": urgency,
    }
