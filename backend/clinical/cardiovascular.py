"""
HealthPulse AI — Cardiovascular Risk and Stroke Calculators.
Implements Framingham 10-Year CVD Risk, ACC/AHA ASCVD Pooled Cohort Equations,
CHA2DS2-VASc stroke risk in AFib, and HAS-BLED bleeding risk score.
"""

import math
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CardiovascularRiskResult:
    score_type: str
    risk_percentage: float
    risk_category: str
    target_ldl_recommendation: str
    statin_therapy_recommendation: str
    details: Dict[str, Any]


def calculate_framingham_10yr_risk(
    age: int,
    gender: str,
    total_cholesterol_mg_dl: float,
    hdl_cholesterol_mg_dl: float,
    systolic_bp: float,
    treated_for_bp: bool,
    smoker: bool,
    diabetic: bool,
) -> CardiovascularRiskResult:
    """
    Framingham 10-Year General Cardiovascular Risk score (D'Agostino et al., Circulation 2008).
    """
    is_male = gender.lower() == "male"
    ln_age = math.log(max(age, 20))
    ln_tc = math.log(max(total_cholesterol_mg_dl, 100))
    ln_hdl = math.log(max(hdl_cholesterol_mg_dl, 20))
    ln_sbp = math.log(max(systolic_bp, 80))

    if is_male:
        beta_age = 3.06117
        beta_tc = 1.12370
        beta_hdl = -0.93263
        beta_sbp = 1.99881 if treated_for_bp else 1.93303
        beta_smoke = 0.65451 if smoker else 0.0
        beta_diabetes = 0.57367 if diabetic else 0.0
        
        sum_beta_x = (
            beta_age * ln_age
            + beta_tc * ln_tc
            + beta_hdl * ln_hdl
            + beta_sbp * ln_sbp
            + beta_smoke
            + beta_diabetes
        )
        mean_beta_x = 23.9802
        base_survival = 0.88936
    else:
        beta_age = 2.32888
        beta_tc = 1.20904
        beta_hdl = -0.70833
        beta_sbp = 2.82263 if treated_for_bp else 2.76157
        beta_smoke = 0.52873 if smoker else 0.0
        beta_diabetes = 0.69154 if diabetic else 0.0

        sum_beta_x = (
            beta_age * ln_age
            + beta_tc * ln_tc
            + beta_hdl * ln_hdl
            + beta_sbp * ln_sbp
            + beta_smoke
            + beta_diabetes
        )
        mean_beta_x = 26.1931
        base_survival = 0.95012

    risk_raw = 1.0 - math.pow(base_survival, math.exp(sum_beta_x - mean_beta_x))
    risk_pct = round(max(0.1, min(99.9, risk_raw * 100.0)), 1)

    if risk_pct < 10.0:
        cat = "Low (<10%)"
        statin = "Lifestyle interventions; statin generally not indicated unless LDL-C >= 190 mg/dL."
        target_ldl = "< 100 mg/dL"
    elif risk_pct < 20.0:
        cat = "Intermediate (10-20%)"
        statin = "Moderate-intensity statin therapy recommended if risk enhancers present."
        target_ldl = "< 70 mg/dL"
    else:
        cat = "High (>20%)"
        statin = "High-intensity statin therapy strongly indicated."
        target_ldl = "< 55 mg/dL"

    return CardiovascularRiskResult(
        score_type="Framingham 10-Year CVD Risk",
        risk_percentage=risk_pct,
        risk_category=cat,
        target_ldl_recommendation=target_ldl,
        statin_therapy_recommendation=statin,
        details={"age": age, "gender": gender, "smoker": smoker, "diabetic": diabetic},
    )


def calculate_ascvd_risk(
    age: int,
    gender: str,
    race: str,
    total_cholesterol_mg_dl: float,
    hdl_cholesterol_mg_dl: float,
    systolic_bp: float,
    treated_for_bp: bool,
    smoker: bool,
    diabetic: bool,
) -> CardiovascularRiskResult:
    """
    ACC/AHA 2013/2018 Pooled Cohort Equations for 10-Year Risk of Hard ASCVD (MI or stroke).
    """
    is_male = gender.lower() == "male"
    is_aa = race.lower() in ("african american", "black", "aa")

    ln_age = math.log(max(age, 20))
    ln_tc = math.log(max(total_cholesterol_mg_dl, 100))
    ln_hdl = math.log(max(hdl_cholesterol_mg_dl, 20))
    ln_sbp = math.log(max(systolic_bp, 80))

    if not is_aa and not is_male:  # White / Non-AA Female
        coeff = (
            -29.799 * ln_age
            + 4.884 * (ln_age ** 2)
            + 13.540 * ln_tc
            + -3.114 * ln_age * ln_tc
            + -13.578 * ln_hdl
            + 3.149 * ln_age * ln_hdl
            + (2.019 * ln_sbp if treated_for_bp else 1.957 * ln_sbp)
            + (7.574 * (1 if smoker else 0))
            + (-1.665 * ln_age * (1 if smoker else 0))
            + (0.661 * (1 if diabetic else 0))
        )
        base_s10 = 0.9665
        mean_coeff = -29.18
    elif is_aa and not is_male:  # AA Female
        coeff = (
            17.114 * ln_age
            + 0.940 * ln_tc
            + -18.920 * ln_hdl
            + 4.475 * ln_age * ln_hdl
            + (29.291 * ln_sbp if treated_for_bp else 27.820 * ln_sbp)
            + (-6.432 * ln_age * (ln_sbp if treated_for_bp else ln_sbp))
            + (0.691 * (1 if smoker else 0))
            + (0.874 * (1 if diabetic else 0))
        )
        base_s10 = 0.8954
        mean_coeff = 86.61
    elif not is_aa and is_male:  # White / Non-AA Male
        coeff = (
            12.344 * ln_age
            + 11.853 * ln_tc
            + -2.664 * ln_age * ln_tc
            + -7.990 * ln_hdl
            + 1.769 * ln_age * ln_hdl
            + (1.797 * ln_sbp if treated_for_bp else 1.764 * ln_sbp)
            + (7.837 * (1 if smoker else 0))
            + (-1.795 * ln_age * (1 if smoker else 0))
            + (0.658 * (1 if diabetic else 0))
        )
        base_s10 = 0.9144
        mean_coeff = 61.18
    else:  # AA Male
        coeff = (
            2.469 * ln_age
            + 0.302 * ln_tc
            + -0.307 * ln_hdl
            + (1.916 * ln_sbp if treated_for_bp else 1.809 * ln_sbp)
            + (0.549 * (1 if smoker else 0))
            + (0.645 * (1 if diabetic else 0))
        )
        base_s10 = 0.8954
        mean_coeff = 19.54

    risk_raw = 1.0 - math.pow(base_s10, math.exp(coeff - mean_coeff))
    risk_pct = round(max(0.1, min(99.9, risk_raw * 100.0)), 1)

    if risk_pct < 5.0:
        cat = "Low (<5%)"
        statin = "Emphasize lifestyle modifications."
        target_ldl = "< 100 mg/dL"
    elif risk_pct < 7.5:
        cat = "Borderline (5% to <7.5%)"
        statin = "Consider moderate-intensity statin if risk enhancers present (e.g. CAC score > 0)."
        target_ldl = "< 70 mg/dL"
    elif risk_pct < 20.0:
        cat = "Intermediate (7.5% to <20%)"
        statin = "Moderate-intensity statin therapy recommended."
        target_ldl = "< 70 mg/dL"
    else:
        cat = "High (>=20%)"
        statin = "High-intensity statin therapy strongly recommended."
        target_ldl = "< 55 mg/dL"

    return CardiovascularRiskResult(
        score_type="ACC/AHA ASCVD 10-Year Risk",
        risk_percentage=risk_pct,
        risk_category=cat,
        target_ldl_recommendation=target_ldl,
        statin_therapy_recommendation=statin,
        details={"age": age, "race": race, "gender": gender},
    )


def calculate_cha2ds2_vasc(
    age: int,
    gender: str,
    congestive_heart_failure: bool,
    hypertension: bool,
    stroke_tia_thromboembolism_history: bool,
    vascular_disease_history: bool,
    diabetes: bool,
) -> Dict[str, Any]:
    """
    CHA2DS2-VASc score for stroke risk in non-valvular atrial fibrillation.
    Score components:
      C - Congestive Heart Failure (+1)
      H - Hypertension (+1)
      A2 - Age >= 75 (+2)
      D - Diabetes (+1)
      S2 - Stroke / TIA / Thromboembolism (+2)
      V - Vascular disease (MI, PAD, aortic plaque) (+1)
      A - Age 65-74 (+1)
      Sc - Sex category Female (+1)
    """
    score = 0
    if congestive_heart_failure:
        score += 1
    if hypertension:
        score += 1
    if age >= 75:
        score += 2
    elif 65 <= age <= 74:
        score += 1
    if diabetes:
        score += 1
    if stroke_tia_thromboembolism_history:
        score += 2
    if vascular_disease_history:
        score += 1
    if gender.lower() == "female":
        score += 1

    # Stroke rates (% / year) from Lip et al. (Chest 2010)
    annual_stroke_risk_table = {
        0: 0.2,
        1: 0.6,
        2: 2.2,
        3: 3.2,
        4: 4.8,
        5: 7.2,
        6: 9.7,
        7: 11.2,
        8: 12.5,
        9: 15.2,
    }
    annual_stroke_rate = annual_stroke_risk_table.get(score, 15.2)

    anticoagulation_rec = (
        "Oral Anticoagulation (DOAC e.g. Apixaban, Rivaroxaban) strongly recommended."
        if (gender.lower() == "male" and score >= 2) or (gender.lower() == "female" and score >= 3)
        else (
            "Oral Anticoagulation may be considered after clinical risk-benefit review."
            if (gender.lower() == "male" and score == 1) or (gender.lower() == "female" and score == 2)
            else "No antithrombotic therapy recommended."
        )
    )

    return {
        "score": score,
        "annual_stroke_risk_percent": annual_stroke_rate,
        "anticoagulation_recommendation": anticoagulation_rec,
        "breakdown": {
            "chf": congestive_heart_failure,
            "hypertension": hypertension,
            "age_score": 2 if age >= 75 else (1 if age >= 65 else 0),
            "diabetes": diabetes,
            "stroke_history": stroke_tia_thromboembolism_history,
            "vascular_disease": vascular_disease_history,
            "female_sex": gender.lower() == "female",
        },
    }


def calculate_has_bled(
    hypertension_uncontrolled: bool,     # SBP > 160
    abnormal_renal_function: bool,       # Dialysis, transplant, Cr >= 2.26 mg/dL
    abnormal_liver_function: bool,       # Cirrhosis or Bilirubin > 2x ULN + AST/ALT > 3x ULN
    stroke_history: bool,
    bleeding_history_or_predisposition: bool,
    labile_inr: bool,                    # TTR < 60%
    elderly_age_over_65: bool,
    drugs_antiplatelet_nsaids: bool,
    alcohol_excess: bool,
) -> Dict[str, Any]:
    """
    HAS-BLED score for 1-year major bleeding risk on anticoagulation.
    Score >= 3 indicates high bleeding risk; caution and regular review warranted.
    """
    score = (
        int(hypertension_uncontrolled)
        + int(abnormal_renal_function)
        + int(abnormal_liver_function)
        + int(stroke_history)
        + int(bleeding_history_or_predisposition)
        + int(labile_inr)
        + int(elderly_age_over_65)
        + int(drugs_antiplatelet_nsaids)
        + int(alcohol_excess)
    )

    bleed_rates = {0: 1.13, 1: 1.02, 2: 1.88, 3: 3.74, 4: 8.70, 5: 12.50}
    annual_bleed_rate = bleed_rates.get(min(score, 5), 12.50)

    return {
        "score": score,
        "is_high_risk": score >= 3,
        "annual_major_bleed_risk_percent": annual_bleed_rate,
        "interpretation": (
            "High bleeding risk (HAS-BLED >= 3). Address modifiable risk factors (e.g. blood pressure control, NSAID discontinuation) and schedule frequent follow-up."
            if score >= 3
            else "Low to moderate bleeding risk."
        ),
    }
