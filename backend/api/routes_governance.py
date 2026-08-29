"""
HealthPulse AI — AI Governance, EU AI Act Model Cards, and Explainability Endpoints.
"""

from fastapi import APIRouter
from typing import Dict, List, Any
from pydantic import BaseModel, Field

from backend.governance.model_card import ModelCardGenerator
from backend.governance.explainability import ClinicalFeatureExplainer
from backend.governance.fairness_auditor import ClinicalFairnessAuditor
from backend.governance.drift_monitor import ClinicalDataDriftMonitor


router = APIRouter()
explainer = ClinicalFeatureExplainer()
fairness_auditor = ClinicalFairnessAuditor()
drift_monitor = ClinicalDataDriftMonitor()


class ExplainRequest(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        example={"respiratory_rate": 26.0, "serum_lactate": 3.2, "heart_rate": 115.0, "mean_arterial_pressure": 62.0}
    )
    predicted_risk: float = Field(0.82, example=0.82)


class DriftCheckRequest(BaseModel):
    feature_name: str = Field("heart_rate", example="heart_rate")
    baseline_values: List[float] = Field(..., example=[72, 75, 78, 80, 82, 76, 74, 79])
    current_values: List[float] = Field(..., example=[95, 102, 110, 105, 98, 112, 108])


@router.get("/model-card/sepsis")
def get_sepsis_model_card():
    card = ModelCardGenerator.generate_sepsis_model_card()
    return card.to_dict()


@router.post("/explain-features")
def explain_features(payload: ExplainRequest):
    attributions = explainer.explain_prediction(payload.features, payload.predicted_risk)
    return {
        "predicted_risk": payload.predicted_risk,
        "attributions": [a.__dict__ for a in attributions],
    }


@router.post("/drift-evaluate")
def evaluate_drift(payload: DriftCheckRequest):
    report = drift_monitor.evaluate_feature_drift(
        feature_name=payload.feature_name,
        baseline_values=payload.baseline_values,
        current_values=payload.current_values,
    )
    return report.__dict__
