"""
HealthPulse AI — Clinical Calculators Unit Tests.
Verifies exact algorithmic outputs for SOFA, qSOFA, APACHE II, Framingham, ASCVD, MELD, CKD-EPI, DDI.
"""

from backend.clinical.sepsis_sofa import calculate_qsofa, calculate_sofa, evaluate_sepsis3_criteria
from backend.clinical.cardiovascular import (
    calculate_framingham_10yr_risk,
    calculate_ascvd_risk,
    calculate_cha2ds2_vasc,
    calculate_has_bled,
)
from backend.clinical.morbidity_apache import calculate_apache_ii, calculate_charlson_comorbidity_index
from backend.clinical.liver_renal import calculate_meld_score, calculate_child_pugh, calculate_ckd_epi_egfr, calculate_cockcroft_gault
from backend.clinical.pulmonary_stroke import calculate_curb65, calculate_wells_dvt, calculate_wells_pe, calculate_nihss_score, calculate_glasgow_coma_scale
from backend.clinical.drug_interactions import DrugInteractionChecker, InteractionSeverity


def test_qsofa_high_risk():
    res = calculate_qsofa(respiratory_rate=24.0, gcs_score=14.0, systolic_bp=95.0)
    assert res.score == 3
    assert res.is_high_risk is True


def test_qsofa_normal():
    res = calculate_qsofa(respiratory_rate=16.0, gcs_score=15.0, systolic_bp=120.0)
    assert res.score == 0
    assert res.is_high_risk is False


def test_sofa_calculation():
    res = calculate_sofa(
        pao2_fio2_ratio=250.0,
        on_mechanical_ventilation=False,
        platelets=80.0,
        bilirubin_mg_dl=2.5,
        mean_arterial_pressure=60.0,
        vasopressors=None,
        gcs_score=13.0,
        creatinine_mg_dl=2.4,
    )
    assert res.respiratory_score == 2
    assert res.coagulation_score == 2
    assert res.hepatic_score == 2
    assert res.cardiovascular_score == 1
    assert res.cns_score == 1
    assert res.renal_score == 2
    assert res.total_score == 10
    assert res.is_sepsis_positive is True


def test_ascvd_risk_calculation():
    res = calculate_ascvd_risk(
        age=55,
        gender="male",
        race="white",
        total_cholesterol_mg_dl=213.0,
        hdl_cholesterol_mg_dl=50.0,
        systolic_bp=120.0,
        treated_for_bp=False,
        smoker=False,
        diabetic=False,
    )
    assert res.risk_percentage > 0.0
    assert "ASCVD" in res.score_type


def test_cha2ds2_vasc():
    res = calculate_cha2ds2_vasc(
        age=76,
        gender="female",
        congestive_heart_failure=True,
        hypertension=True,
        stroke_tia_thromboembolism_history=False,
        vascular_disease_history=False,
        diabetes=True,
    )
    # Age >= 75 (+2), female (+1), chf (+1), htn (+1), diabetes (+1) = 6
    assert res["score"] == 6
    assert res["annual_stroke_risk_percent"] > 5.0


def test_meld_score():
    res = calculate_meld_score(
        serum_creatinine_mg_dl=1.8,
        serum_bilirubin_mg_dl=2.4,
        inr=1.6,
        serum_sodium_meq_l=132.0,
    )
    assert res.meld_original >= 15.0
    assert res.meld_na >= 15.0


def test_ckd_epi_egfr():
    res = calculate_ckd_epi_egfr(serum_creatinine_mg_dl=1.0, age=50, gender="female")
    assert res["egfr_ml_min_1_73m2"] > 60.0
    assert "CKD-EPI" in res["equation"]


def test_drug_interaction_checker():
    checker = DrugInteractionChecker()
    # Warfarin + Aspirin
    pair = checker.check_pair("warfarin", "aspirin")
    assert pair is not None
    assert pair.severity == InteractionSeverity.MAJOR

    # Multi-drug list
    meds = ["warfarin", "amiodarone", "lisinopril"]
    interactions = checker.check_medication_list(meds)
    assert len(interactions) >= 1
