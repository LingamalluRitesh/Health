"""
HealthPulse AI — EU AI Act Annex IV & FDA SaMD (Software as a Medical Device) Model Card Generator.
Standardizes clinical AI model documentation, validation metrics, demographic benchmarks, and human oversight controls.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EUAIActRiskClass(str, Enum):
    HIGH_RISK = "Class III / High Risk (Annex III Medical Device / Critical Healthcare Infrastructure)"
    SPECIFIC_TRANSPARENCY = "Specific Transparency Risk"
    MINIMAL_RISK = "Minimal / No Risk"


@dataclass
class ClinicalModelCard:
    model_id: str
    model_name: str
    version: str
    release_date: str
    developer: str
    intended_clinical_use: str
    target_patient_population: str
    clinical_contraindications: List[str]
    regulatory_classification: str
    eu_ai_act_risk_tier: EUAIActRiskClass
    fda_device_class: str
    training_cohort_summary: Dict[str, Any]
    validation_cohort_summary: Dict[str, Any]
    performance_metrics: Dict[str, float]
    subgroup_fairness_summary: Dict[str, Any]
    human_in_the_loop_protocol: str
    known_limitations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "model_name": self.model_name,
            "version": self.version,
            "release_date": self.release_date,
            "developer": self.developer,
            "intended_clinical_use": self.intended_clinical_use,
            "target_patient_population": self.target_patient_population,
            "clinical_contraindications": self.clinical_contraindications,
            "regulatory_classification": self.regulatory_classification,
            "eu_ai_act_risk_tier": self.eu_ai_act_risk_tier.value,
            "fda_device_class": self.fda_device_class,
            "training_cohort_summary": self.training_cohort_summary,
            "validation_cohort_summary": self.validation_cohort_summary,
            "performance_metrics": self.performance_metrics,
            "subgroup_fairness_summary": self.subgroup_fairness_summary,
            "human_in_the_loop_protocol": self.human_in_the_loop_protocol,
            "known_limitations": self.known_limitations,
        }


class ModelCardGenerator:
    """Produces standardized governance model cards for platform clinical neural engines."""

    @classmethod
    def generate_sepsis_model_card(cls) -> ClinicalModelCard:
        return ClinicalModelCard(
            model_id="healthpulse-sepsis-net-v1",
            model_name="HealthPulse Deep Sepsis Early Warning Neural Engine",
            version="1.2.0",
            release_date="2026-01-15",
            developer="HealthPulse AI Clinical Intelligence Lab",
            intended_clinical_use=(
                "Continuous automated surveillance of adult ICU and step-down unit patients "
                "to predict onset of severe sepsis or septic shock 4 to 6 hours prior to clinical recognition."
            ),
            target_patient_population="Inpatient adults aged 18 and older in ICU and telemetry-monitored beds.",
            clinical_contraindications=[
                "Do not use in pediatric populations (age < 18).",
                "Do not use as an autonomous order-triggering device; all treatment bundles require licensed physician approval.",
                "Patients undergoing active palliative care / comfort measures only.",
            ],
            regulatory_classification="FDA SaMD Class II (510(k) Pre-Market Notification Pathway)",
            eu_ai_act_risk_tier=EUAIActRiskClass.HIGH_RISK,
            fda_device_class="Class II",
            training_cohort_summary={
                "cohort_source": "MIMIC-IV & eICU Collaborative Research Database",
                "total_patients": 64200,
                "icu_encounters": 78500,
                "gender_split": {"male": "53.4%", "female": "46.6%"},
                "median_age": 63.8,
            },
            validation_cohort_summary={
                "cohort_source": "Multi-Center Prospective Hospital Network Validation",
                "total_patients": 12800,
                "icu_encounters": 14250,
            },
            performance_metrics={
                "AUROC": 0.912,
                "AUPRC": 0.684,
                "Sensitivity_at_80pct_Spec": 0.842,
                "Specificity": 0.887,
                "Lead_Time_Hours": 5.4,
                "Brier_Score": 0.052,
            },
            subgroup_fairness_summary={
                "Disparate_Impact_Ratio_Sex": 0.96,
                "Equalized_Odds_Disparity_Max": 0.038,
                "Demographic_Parity_Passed": True,
            },
            human_in_the_loop_protocol=(
                "When alert triggers (risk score >= 0.70), ICU nurse receives an inline EHR advisory card. "
                "The nurse conducts a bedside clinical assessment within 15 minutes and notifies attending physician if bundle indicated."
            ),
            known_limitations=[
                "Performance may degrade during severe hypothermia or targeted temperature management protocols.",
                "Transient tachycardia from anxiety or physical agitation may increase false alert frequency.",
            ],
        )
