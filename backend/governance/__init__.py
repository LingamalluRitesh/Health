"""
HealthPulse AI — AI Governance, Explainability and Model Safety Module.
Implements EU AI Act Annex IV / FDA SaMD Model Cards, SHAP attribution, fairness auditing, and drift monitors.
"""

from backend.governance.model_card import (
    ModelCardGenerator,
    ClinicalModelCard,
    EUAIActRiskClass,
)
from backend.governance.explainability import (
    ClinicalFeatureExplainer,
    FeatureAttribution,
)
from backend.governance.fairness_auditor import (
    ClinicalFairnessAuditor,
    FairnessEvaluationReport,
)
from backend.governance.drift_monitor import (
    ClinicalDataDriftMonitor,
    DriftReport,
)

__all__ = [
    "ModelCardGenerator",
    "ClinicalModelCard",
    "EUAIActRiskClass",
    "ClinicalFeatureExplainer",
    "FeatureAttribution",
    "ClinicalFairnessAuditor",
    "FairnessEvaluationReport",
    "ClinicalDataDriftMonitor",
    "DriftReport",
]
