"""
HealthPulse AI — API Routing and CDS Hooks Integration Tests.
"""

from backend.api.routes_clinical import compute_qsofa, compute_sofa, compute_ascvd, check_drug_interactions, match_clinical_trials, QSOFARequest, SOFARequest, ASCVDRequest, DDIRequest, TrialMatchRequest
from backend.api.routes_imaging import evaluate_nodule, compute_ctr, window_transform, NoduleEvalSchema, CTRSchema, WindowingSchema
from backend.api.routes_governance import get_sepsis_model_card, explain_features, ExplainRequest
from backend.api.routes_cds_hooks import get_services, evaluate_sepsis_service, CDSHookRequest


def test_api_qsofa_endpoint():
    req = QSOFARequest(respiratory_rate=25.0, gcs_score=14.0, systolic_bp=92.0)
    res = compute_qsofa(req)
    assert res["score"] == 3
    assert res["is_high_risk"] is True


def test_api_ddi_endpoint():
    req = DDIRequest(medications=["simvastatin", "clarithromycin"])
    res = check_drug_interactions(req)
    assert res["interaction_count"] == 1
    assert res["interactions"][0]["severity"] == "contraindicated"


def test_api_imaging_ctr_endpoint():
    req = CTRSchema(cardiac_diameter_mm=170.0, thoracic_diameter_mm=300.0)
    res = compute_ctr(req)
    assert res["is_cardiomegaly"] is True


def test_api_model_card_endpoint():
    card = get_sepsis_model_card()
    assert card["model_id"] == "healthpulse-sepsis-net-v1"
    assert "High Risk" in card["eu_ai_act_risk_tier"]


def test_api_cds_discovery_endpoint():
    services = get_services()
    assert len(services["services"]) >= 3
    hook_names = [s["hook"] for s in services["services"]]
    assert "patient-view" in hook_names
    assert "order-select" in hook_names


def test_api_cds_sepsis_evaluation():
    req = CDSHookRequest(
        hook="patient-view",
        hookInstance="test-uuid",
        context={"patientId": "P-100234", "userId": "Practitioner/DOC-101"},
    )
    res = evaluate_sepsis_service(req)
    assert len(res["cards"]) >= 1
    assert res["cards"][0]["indicator"] == "critical"
