"""
HealthPulse AI — Clinical Risk Calculators & Evidence-Based Scorer Endpoints.
Provides REST APIs for SOFA, qSOFA, APACHE II, Framingham, ASCVD, CHA2DS2-VASc, MELD, CKD-EPI, DDI, and Trial Matching.
"""

from fastapi import APIRouter, Body
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from backend.clinical.sepsis_sofa import calculate_qsofa, calculate_sofa, evaluate_sepsis3_criteria
from backend.clinical.cardiovascular import calculate_framingham_10yr_risk, calculate_ascvd_risk, calculate_cha2ds2_vasc, calculate_has_bled
from backend.clinical.morbidity_apache import calculate_apache_ii, calculate_charlson_comorbidity_index
from backend.clinical.liver_renal import calculate_meld_score, calculate_child_pugh, calculate_ckd_epi_egfr, calculate_cockcroft_gault
from backend.clinical.pulmonary_stroke import calculate_curb65, calculate_wells_dvt, calculate_wells_pe, calculate_nihss_score, calculate_glasgow_coma_scale
from backend.clinical.drug_interactions import DrugInteractionChecker
from backend.clinical.trial_matching import ClinicalTrialMatcher


router = APIRouter()
ddi_checker = DrugInteractionChecker()
trial_matcher = ClinicalTrialMatcher()


class QSOFARequest(BaseModel):
    respiratory_rate: float = Field(..., example=24.0)
    gcs_score: float = Field(..., example=14.0)
    systolic_bp: float = Field(..., example=95.0)


class SOFARequest(BaseModel):
    pao2_fio2_ratio: Optional[float] = Field(None, example=280.0)
    on_mechanical_ventilation: bool = Field(False, example=False)
    platelets: Optional[float] = Field(None, example=120.0)
    bilirubin_mg_dl: Optional[float] = Field(None, example=1.6)
    mean_arterial_pressure: Optional[float] = Field(None, example=65.0)
    vasopressors: Optional[str] = Field(None, example="dopamine_low")
    gcs_score: Optional[float] = Field(15.0, example=14.0)
    creatinine_mg_dl: Optional[float] = Field(None, example=2.2)
    urine_output_ml_day: Optional[float] = Field(None, example=800.0)


class ASCVDRequest(BaseModel):
    age: int = Field(..., example=58)
    gender: str = Field(..., example="male")
    race: str = Field("white", example="white")
    total_cholesterol: float = Field(..., example=220.0)
    hdl_cholesterol: float = Field(..., example=42.0)
    systolic_bp: float = Field(..., example=142.0)
    treated_for_bp: bool = Field(True, example=True)
    smoker: bool = Field(False, example=False)
    diabetic: bool = Field(True, example=True)


class DDIRequest(BaseModel):
    medications: List[str] = Field(..., example=["warfarin", "amiodarone", "aspirin"])


class TrialMatchRequest(BaseModel):
    age: int = Field(..., example=62)
    gender: str = Field(..., example="female")
    active_icd10_codes: List[str] = Field(..., example=["E11.22", "N18.3", "I10"])
    egfr: Optional[float] = Field(42.0, example=42.0)
    platelets: Optional[float] = Field(180.0, example=180.0)
    bilirubin: Optional[float] = Field(0.9, example=0.9)
    genomic_mutations: Optional[List[str]] = Field(default_factory=list, example=["EGFR:exon20ins"])


@router.post("/qsofa")
def compute_qsofa(payload: QSOFARequest):
    res = calculate_qsofa(payload.respiratory_rate, payload.gcs_score, payload.systolic_bp)
    return res.__dict__


@router.post("/sofa")
def compute_sofa(payload: SOFARequest):
    res = calculate_sofa(
        pao2_fio2_ratio=payload.pao2_fio2_ratio,
        on_mechanical_ventilation=payload.on_mechanical_ventilation,
        platelets=payload.platelets,
        bilirubin_mg_dl=payload.bilirubin_mg_dl,
        mean_arterial_pressure=payload.mean_arterial_pressure,
        vasopressors=payload.vasopressors,
        gcs_score=payload.gcs_score,
        creatinine_mg_dl=payload.creatinine_mg_dl,
        urine_output_ml_day=payload.urine_output_ml_day,
    )
    return res.__dict__


@router.post("/ascvd")
def compute_ascvd(payload: ASCVDRequest):
    res = calculate_ascvd_risk(
        age=payload.age,
        gender=payload.gender,
        race=payload.race,
        total_cholesterol_mg_dl=payload.total_cholesterol,
        hdl_cholesterol_mg_dl=payload.hdl_cholesterol,
        systolic_bp=payload.systolic_bp,
        treated_for_bp=payload.treated_for_bp,
        smoker=payload.smoker,
        diabetic=payload.diabetic,
    )
    return res.__dict__


@router.post("/ddi-check")
def check_drug_interactions(payload: DDIRequest):
    interactions = ddi_checker.check_medication_list(payload.medications)
    return {
        "medications_screened": payload.medications,
        "interaction_count": len(interactions),
        "interactions": [i.__dict__ for i in interactions],
    }


@router.post("/trial-match")
def match_clinical_trials(payload: TrialMatchRequest):
    matches = trial_matcher.evaluate_patient(
        patient_age=payload.age,
        patient_gender=payload.gender,
        active_icd10_codes=payload.active_icd10_codes,
        egfr=payload.egfr,
        platelets=payload.platelets,
        bilirubin=payload.bilirubin,
        genomic_mutations=payload.genomic_mutations,
    )
    return {
        "total_trials_evaluated": len(matches),
        "eligible_trials": [m.__dict__ for m in matches if m.is_eligible],
        "all_trials": [m.__dict__ for m in matches],
    }
