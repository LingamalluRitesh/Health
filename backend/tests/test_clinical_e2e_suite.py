"""
End-to-End Clinical Intelligence Test Suite.
Verifies multi-modal pipelines: Risk Scores + HIPAA De-id + DICOM Analytics + Genomics + CDS Hooks.
"""

import pytest
from backend.clinical.sepsis_sofa import calculate_sofa, calculate_qsofa
from backend.clinical.morbidity_apache import calculate_apache_ii
from backend.clinical.cardiovascular import calculate_cha2ds2_vasc
from backend.security.hipaa_scrubber import HIPAAScrubber
from backend.imaging.windowing import apply_voi_lut_window
from backend.genomics.acmg_classifier import ACMGVariantClassifier
from backend.api.routes_cds_hooks import evaluate_sepsis_service, CDSHookRequest


def test_clinical_risk_prediction_pipeline():
    # 1. SOFA Assessment
    sofa_res = calculate_sofa(
        pao2_fio2_ratio=150.0,
        on_mechanical_ventilation=True,
        platelets=45.0,
        bilirubin_mg_dl=6.5,
        mean_arterial_pressure=60.0,
        vasopressors=None,
        gcs_score=8.0,
        creatinine_mg_dl=3.8,
    )
    assert sofa_res.total_score >= 12
    assert sofa_res.is_sepsis_positive is True

    # 2. APACHE II Score
    apache_res = calculate_apache_ii(
        temp_celsius=39.2,
        mean_arterial_pressure=58.0,
        heart_rate=140.0,
        respiratory_rate=32.0,
        pao2=60.0,
        fio2=0.21,
        aado2=None,
        arterial_ph=7.22,
        serum_sodium=155.0,
        serum_potassium=5.8,
        serum_creatinine=3.5,
        hematocrit_pct=28.0,
        wbc_count_10e3=24.0,
        gcs_score=9.0,
        age=68,
        chronic_organ_failure=True,
    )
    assert apache_res.total_apache_points > 20

    # 3. CHA2DS2-VASc
    chads_score = calculate_cha2ds2_vasc(
        age=76,
        gender="female",
        congestive_heart_failure=True,
        hypertension=True,
        stroke_tia_thromboembolism_history=True,
        vascular_disease_history=True,
        diabetes=True,
    )
    assert chads_score["score"] >= 6
    assert "strongly recommended" in chads_score["anticoagulation_recommendation"].lower()


def test_security_phi_deidentification_pipeline():
    raw_note = "Patient Jane Doe (SSN: 000-11-2222, Phone: 617-555-0199) visited hospital on 04/15/2025."
    scrubber = HIPAAScrubber()
    sanitized = scrubber.scrub_text(raw_note).sanitized_text
    assert "000-11-2222" not in sanitized
    assert "617-555-0199" not in sanitized
    assert "[SOCIAL_SECURITY_NUMBER]" in sanitized


def test_imaging_and_genomics_pipelines():
    # Windowing
    hu_pixels = [-1000.0, 0.0, 40.0, 200.0, 1000.0]
    windowed = apply_voi_lut_window(hu_pixels, window_center=40.0, window_width=400.0)
    assert len(windowed) == 5
    assert windowed[0] == 0
    assert windowed[-1] == 255

    # ACMG Classification
    classifier = ACMGVariantClassifier()
    classification = classifier.classify_variant(
        variant_id="VAR-BRAF-V600E",
        gene="BRAF",
        criteria_codes=["PVS1", "PS1", "PM1"],
    )
    assert classification.classification.name in ["PATHOGENIC", "LIKELY_PATHOGENIC"]


def test_cds_hooks_patient_view_e2e():
    req = CDSHookRequest(
        hook="patient-view",
        hookInstance="e2e-test-instance-001",
        context={"patientId": "P-100234", "userId": "Practitioner/DOC-101"},
    )
    res = evaluate_sepsis_service(req)
    assert len(res["cards"]) >= 1
    assert res["cards"][0]["indicator"] in ["critical", "warning", "info"]
