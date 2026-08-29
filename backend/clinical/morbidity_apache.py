"""
HealthPulse AI — Critical Care Morbidity and Mortality Indices.
Implements APACHE II (Acute Physiology and Chronic Health Evaluation II)
and Charlson Comorbidity Index (CCI).
"""

import math
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class APACHEIIPrediction:
    total_apache_points: int
    acute_physiology_score: int
    age_points: int
    chronic_health_points: int
    predicted_in_hospital_mortality_percent: float
    gcs_points: int
    interpretation: str


def calculate_apache_ii(
    temp_celsius: float,
    mean_arterial_pressure: float,
    heart_rate: float,
    respiratory_rate: float,
    pao2: Optional[float],
    fio2: float,
    aado2: Optional[float],
    arterial_ph: Optional[float],
    serum_sodium: float,
    serum_potassium: float,
    serum_creatinine: float,
    hematocrit_pct: float,
    wbc_count_10e3: float,
    gcs_score: float,
    age: int,
    chronic_organ_failure: bool = False,
    emergency_surgery_or_non_operative: bool = True,
) -> APACHEIIPrediction:
    """
    APACHE II Severity of Disease Score (Knaus et al., Crit Care Med 1985).
    Ranges from 0 to 71.
    """
    aps = 0

    # 1. Temperature (rectal C)
    if temp_celsius >= 41.0 or temp_celsius <= 29.9:
        aps += 4
    elif temp_celsius >= 39.0 or (30.0 <= temp_celsius <= 31.9):
        aps += 3
    elif 32.0 <= temp_celsius <= 33.9:
        aps += 2
    elif (38.5 <= temp_celsius <= 38.9) or (34.0 <= temp_celsius <= 35.9):
        aps += 1

    # 2. Mean Arterial Pressure (mmHg)
    if mean_arterial_pressure >= 160 or mean_arterial_pressure <= 49:
        aps += 4
    elif 130 <= mean_arterial_pressure <= 159 or 50 <= mean_arterial_pressure <= 69:
        aps += 2
    elif 110 <= mean_arterial_pressure <= 129:
        aps += 1

    # 3. Heart Rate (bpm)
    if heart_rate >= 180 or heart_rate <= 39:
        aps += 4
    elif 140 <= heart_rate <= 179 or 40 <= heart_rate <= 54:
        aps += 3
    elif 110 <= heart_rate <= 139 or 55 <= heart_rate <= 69:
        aps += 2

    # 4. Respiratory Rate (breaths/min)
    if respiratory_rate >= 50 or respiratory_rate <= 5:
        aps += 4
    elif 35 <= respiratory_rate <= 49:
        aps += 3
    elif 6 <= respiratory_rate <= 9:
        aps += 2
    elif 25 <= respiratory_rate <= 34 or 10 <= respiratory_rate <= 11:
        aps += 1

    # 5. Oxygenation: If FiO2 >= 0.5 use A-aDO2; if FiO2 < 0.5 use PaO2
    if fio2 >= 0.5:
        a_a_gradient = aado2 if aado2 is not None else 0.0
        if a_a_gradient >= 500:
            aps += 4
        elif 350 <= a_a_gradient <= 499:
            aps += 3
        elif 200 <= a_a_gradient <= 349:
            aps += 2
    else:
        po2 = pao2 if pao2 is not None else 90.0
        if po2 < 55:
            aps += 4
        elif 55 <= po2 <= 60:
            aps += 3
        elif 61 <= po2 <= 70:
            aps += 1

    # 6. Arterial pH
    if arterial_ph is not None:
        if arterial_ph >= 7.70 or arterial_ph < 7.15:
            aps += 4
        elif (7.60 <= arterial_ph <= 7.69) or (7.15 <= arterial_ph <= 7.24):
            aps += 3
        elif 7.25 <= arterial_ph <= 7.32:
            aps += 2
        elif 7.50 <= arterial_ph <= 7.59:
            aps += 1

    # 7. Serum Sodium (mEq/L)
    if serum_sodium >= 180 or serum_sodium <= 110:
        aps += 4
    elif 160 <= serum_sodium <= 179 or 111 <= serum_sodium <= 119:
        aps += 3
    elif 155 <= serum_sodium <= 159 or 120 <= serum_sodium <= 129:
        aps += 2
    elif 150 <= serum_sodium <= 154:
        aps += 1

    # 8. Serum Potassium (mEq/L)
    if serum_potassium >= 7.0 or serum_potassium < 2.5:
        aps += 4
    elif 6.0 <= serum_potassium <= 6.9 or 2.5 <= serum_potassium <= 2.9:
        aps += 2
    elif 5.5 <= serum_potassium <= 5.9 or 3.0 <= serum_potassium <= 3.4:
        aps += 1

    # 9. Serum Creatinine (mg/dL) - Double score if acute renal failure
    creat_pts = 0
    if serum_creatinine >= 3.5:
        creat_pts = 4
    elif 2.0 <= serum_creatinine <= 3.4:
        creat_pts = 3
    elif 1.5 <= serum_creatinine <= 1.9 or serum_creatinine < 0.6:
        creat_pts = 2
    aps += creat_pts

    # 10. Hematocrit (%)
    if hematocrit_pct >= 60.0 or hematocrit_pct < 20.0:
        aps += 4
    elif 50.0 <= hematocrit_pct <= 59.9 or 20.0 <= hematocrit_pct <= 29.9:
        aps += 2
    elif 46.0 <= hematocrit_pct <= 49.9:
        aps += 1

    # 11. White Blood Count (total / mm3 in 1000s)
    if wbc_count_10e3 >= 40.0 or wbc_count_10e3 < 1.0:
        aps += 4
    elif 20.0 <= wbc_count_10e3 <= 39.9 or 1.0 <= wbc_count_10e3 <= 2.9:
        aps += 2
    elif 15.0 <= wbc_count_10e3 <= 19.9:
        aps += 1

    # 12. Glasgow Coma Score (GCS Points = 15 - actual GCS)
    gcs_pts = int(15.0 - max(3.0, min(15.0, gcs_score)))
    aps += gcs_pts

    # Age Points
    age_pts = 0
    if age >= 75:
        age_pts = 6
    elif 65 <= age <= 74:
        age_pts = 5
    elif 55 <= age <= 64:
        age_pts = 3
    elif 45 <= age <= 54:
        age_pts = 2

    # Chronic Health Points
    chronic_pts = 0
    if chronic_organ_failure:
        chronic_pts = 5 if emergency_surgery_or_non_operative else 2

    total_score = aps + age_pts + chronic_pts

    # Logistic regression estimated mortality
    logit = -3.517 + (0.146 * total_score)
    mortality_pct = round((1.0 / (1.0 + math.exp(-logit))) * 100.0, 1)

    return APACHEIIPrediction(
        total_apache_points=total_score,
        acute_physiology_score=aps,
        age_points=age_pts,
        chronic_health_points=chronic_pts,
        predicted_in_hospital_mortality_percent=mortality_pct,
        gcs_points=gcs_pts,
        interpretation=f"APACHE II Score: {total_score} points (Estimated ICU Mortality: {mortality_pct}%)",
    )


def calculate_charlson_comorbidity_index(
    age: int,
    myocardial_infarction: bool = False,
    congestive_heart_failure: bool = False,
    peripheral_vascular_disease: bool = False,
    cerebrovascular_disease: bool = False,
    dementia: bool = False,
    chronic_pulmonary_disease: bool = False,
    connective_tissue_disease: bool = False,
    peptic_ulcer_disease: bool = False,
    mild_liver_disease: bool = False,
    diabetes_uncomplicated: bool = False,
    diabetes_with_end_organ_damage: bool = False,
    hemiplegia: bool = False,
    moderate_to_severe_renal_disease: bool = False,
    solid_tumor_localized: bool = False,
    leukemia: bool = False,
    lymphoma: bool = False,
    moderate_to_severe_liver_disease: bool = False,
    metastatic_solid_tumor: bool = False,
    aids_hiv: bool = False,
) -> Dict[str, Any]:
    """
    Charlson Comorbidity Index (CCI) calculates 10-year survival probability.
    """
    score = 0

    # 1 point each
    if myocardial_infarction:
        score += 1
    if congestive_heart_failure:
        score += 1
    if peripheral_vascular_disease:
        score += 1
    if cerebrovascular_disease:
        score += 1
    if dementia:
        score += 1
    if chronic_pulmonary_disease:
        score += 1
    if connective_tissue_disease:
        score += 1
    if peptic_ulcer_disease:
        score += 1
    if mild_liver_disease:
        score += 1
    if diabetes_uncomplicated:
        score += 1

    # 2 points each
    if hemiplegia:
        score += 2
    if moderate_to_severe_renal_disease:
        score += 2
    if diabetes_with_end_organ_damage:
        score += 2
    if solid_tumor_localized:
        score += 2
    if leukemia:
        score += 2
    if lymphoma:
        score += 2

    # 3 points each
    if moderate_to_severe_liver_disease:
        score += 3

    # 6 points each
    if metastatic_solid_tumor:
        score += 6
    if aids_hiv:
        score += 6

    # Age points: +1 for each decade over 40
    age_pts = 0
    if age >= 50:
        age_pts = min(4, (age - 40) // 10)
    total_score = score + age_pts

    # 10-year survival probability = 0.983^(exp(total_score * 0.9))
    ten_year_survival_pct = round(math.pow(0.983, math.exp(total_score * 0.9)) * 100.0, 1)

    return {
        "charlson_index": total_score,
        "comorbidity_score": score,
        "age_points": age_pts,
        "estimated_10yr_survival_percent": max(0.1, min(99.0, ten_year_survival_pct)),
        "interpretation": f"CCI Score {total_score}: Estimated 10-year survival is {ten_year_survival_pct}%.",
    }
