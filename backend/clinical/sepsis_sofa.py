"""
HealthPulse AI — Sepsis-3, SOFA (Sequential Organ Failure Assessment) and qSOFA Calculators.
Implements the 2016 Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3).
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from backend.core.types import PatientVitalSigns


@dataclass
class qSOFAScoreResult:
    score: int
    respiratory_rate_flag: bool
    altered_mentation_flag: bool
    systolic_bp_flag: bool
    is_high_risk: bool
    clinical_interpretation: str


@dataclass
class SOFAScoreResult:
    total_score: int
    respiratory_score: int
    coagulation_score: int
    hepatic_score: int
    cardiovascular_score: int
    cns_score: int
    renal_score: int
    estimated_mortality_percent: float
    is_sepsis_positive: bool
    breakdown: Dict[str, Any]


def calculate_qsofa(
    respiratory_rate: float,
    gcs_score: float,
    systolic_bp: float,
) -> qSOFAScoreResult:
    """
    Calculates quick SOFA (qSOFA) score.
    Criteria:
      - Respiratory rate >= 22 breaths/min (+1)
      - Altered mentation (GCS < 15) (+1)
      - Systolic BP <= 100 mmHg (+1)
    High risk >= 2 points.
    """
    rr_flag = respiratory_rate >= 22.0
    cns_flag = gcs_score < 15.0
    sbp_flag = systolic_bp <= 100.0

    score = int(rr_flag) + int(cns_flag) + int(sbp_flag)
    high_risk = score >= 2

    if score >= 2:
        interp = "High risk for in-hospital mortality or prolonged ICU stay. Assess immediately for organ dysfunction."
    elif score == 1:
        interp = "Moderate risk. Monitor vitals closely and repeat assessment if status deteriorates."
    else:
        interp = "Low risk for acute sepsis-related decompensation based on bedside qSOFA criteria."

    return qSOFAScoreResult(
        score=score,
        respiratory_rate_flag=rr_flag,
        altered_mentation_flag=cns_flag,
        systolic_bp_flag=sbp_flag,
        is_high_risk=high_risk,
        clinical_interpretation=interp,
    )


def calculate_sofa(
    pao2_fio2_ratio: Optional[float] = None,
    on_mechanical_ventilation: bool = False,
    platelets: Optional[float] = None,             # 10^3/uL
    bilirubin_mg_dl: Optional[float] = None,        # mg/dL
    mean_arterial_pressure: Optional[float] = None, # mmHg
    vasopressors: Optional[str] = None,             # None, "dopamine_low", "dopamine_med", "norepi_low", "norepi_high"
    gcs_score: Optional[float] = 15.0,
    creatinine_mg_dl: Optional[float] = None,       # mg/dL
    urine_output_ml_day: Optional[float] = None,    # mL/day
) -> SOFAScoreResult:
    """
    Calculates complete 6-organ-system SOFA Score.
    """
    # 1. Respiration: PaO2/FiO2 ratio (mmHg)
    resp_score = 0
    if pao2_fio2_ratio is not None:
        if pao2_fio2_ratio < 100 and on_mechanical_ventilation:
            resp_score = 4
        elif pao2_fio2_ratio < 200 and on_mechanical_ventilation:
            resp_score = 3
        elif pao2_fio2_ratio < 300:
            resp_score = 2
        elif pao2_fio2_ratio < 400:
            resp_score = 1

    # 2. Coagulation: Platelets (x 10^3 / uL)
    coag_score = 0
    if platelets is not None:
        if platelets < 20:
            coag_score = 4
        elif platelets < 50:
            coag_score = 3
        elif platelets < 100:
            coag_score = 2
        elif platelets < 150:
            coag_score = 1

    # 3. Liver: Bilirubin (mg/dL)
    liver_score = 0
    if bilirubin_mg_dl is not None:
        if bilirubin_mg_dl >= 12.0:
            liver_score = 4
        elif bilirubin_mg_dl >= 6.0:
            liver_score = 3
        elif bilirubin_mg_dl >= 2.0:
            liver_score = 2
        elif bilirubin_mg_dl >= 1.2:
            liver_score = 1

    # 4. Cardiovascular: MAP and Vasopressors
    cv_score = 0
    if vasopressors == "norepi_high" or vasopressors == "epi_high" or vasopressors == "dopamine_high":
        cv_score = 4
    elif vasopressors == "norepi_low" or vasopressors == "epi_low" or vasopressors == "dopamine_med":
        cv_score = 3
    elif vasopressors == "dopamine_low" or vasopressors == "dobutamine":
        cv_score = 2
    elif mean_arterial_pressure is not None and mean_arterial_pressure < 70.0:
        cv_score = 1

    # 5. Central Nervous System: Glasgow Coma Scale (GCS)
    cns_score = 0
    gcs = gcs_score if gcs_score is not None else 15.0
    if gcs < 6:
        cns_score = 4
    elif gcs <= 9:
        cns_score = 3
    elif gcs <= 12:
        cns_score = 2
    elif gcs <= 14:
        cns_score = 1

    # 6. Renal: Creatinine (mg/dL) or Urine Output (mL/day)
    renal_score = 0
    if (creatinine_mg_dl is not None and creatinine_mg_dl >= 5.0) or (urine_output_ml_day is not None and urine_output_ml_day < 200):
        renal_score = 4
    elif (creatinine_mg_dl is not None and creatinine_mg_dl >= 3.5) or (urine_output_ml_day is not None and urine_output_ml_day < 500):
        renal_score = 3
    elif creatinine_mg_dl is not None and creatinine_mg_dl >= 2.0:
        renal_score = 2
    elif creatinine_mg_dl is not None and creatinine_mg_dl >= 1.2:
        renal_score = 1

    total = resp_score + coag_score + liver_score + cv_score + cns_score + renal_score

    # Mortality correlation according to Vincent et al. (1998)
    if total <= 1:
        mortality = 0.0
    elif total <= 3:
        mortality = 3.5
    elif total <= 5:
        mortality = 7.0
    elif total <= 7:
        mortality = 14.0
    elif total <= 9:
        mortality = 22.0
    elif total <= 11:
        mortality = 36.0
    elif total <= 14:
        mortality = 50.0
    else:
        mortality = 80.0

    return SOFAScoreResult(
        total_score=total,
        respiratory_score=resp_score,
        coagulation_score=coag_score,
        hepatic_score=liver_score,
        cardiovascular_score=cv_score,
        cns_score=cns_score,
        renal_score=renal_score,
        estimated_mortality_percent=mortality,
        is_sepsis_positive=total >= 2,
        breakdown={
            "respiratory": resp_score,
            "coagulation": coag_score,
            "hepatic": liver_score,
            "cardiovascular": cv_score,
            "cns": cns_score,
            "renal": renal_score,
        },
    )


def evaluate_sepsis3_criteria(
    baseline_sofa: int,
    current_sofa: int,
    infection_suspected: bool,
    serum_lactate_mmol_l: Optional[float] = None,
    mean_arterial_pressure: Optional[float] = None,
    requiring_vasopressors: bool = False,
) -> Dict[str, Any]:
    """
    Evaluates Sepsis-3 definitions:
    1. Sepsis: Suspected infection + delta SOFA >= 2
    2. Septic Shock: Sepsis + requiring vasopressors to maintain MAP >= 65 + lactate > 2 mmol/L despite fluid resuscitation
    """
    delta_sofa = current_sofa - baseline_sofa
    is_sepsis = infection_suspected and (delta_sofa >= 2 or current_sofa >= 2)
    
    is_septic_shock = False
    if is_sepsis and requiring_vasopressors:
        if serum_lactate_mmol_l is not None and serum_lactate_mmol_l > 2.0:
            is_septic_shock = True

    return {
        "is_sepsis": is_sepsis,
        "is_septic_shock": is_septic_shock,
        "delta_sofa": delta_sofa,
        "current_sofa": current_sofa,
        "serum_lactate": serum_lactate_mmol_l,
        "recommendation": (
            "EMERGENCY: Septic shock criteria met. Continue vasopressors, monitor central venous access, and titrate fluids."
            if is_septic_shock
            else (
                "CRITICAL: Sepsis criteria met. Initiate 1-Hour resuscitation bundle immediately."
                if is_sepsis
                else "Normal / Non-septic profile."
            )
        ),
    }
