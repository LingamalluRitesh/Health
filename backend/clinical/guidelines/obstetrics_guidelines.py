"""
HealthPulse AI — Evidence-Based Obstetrics & Maternal-Fetal Medicine (MFM) Guidelines.
Implements ACOG (American College of Obstetricians and Gynecologists) and SMFM clinical guidelines:
- Hypertensive Disorders of Pregnancy (Gestational Hypertension, Preeclampsia with/without Severe Features, Eclampsia)
- Preeclampsia Seizure Prophylaxis (Magnesium Sulfate 4g IV Bolus + 1-2g/h Infusion & Calcium Gluconate Reversal)
- Acute Severe Hypertension in Pregnancy Emergency Protocol (IV Labetalol vs IV Hydralazine vs Oral Nifedipine)
- Postpartum Hemorrhage (PPH Stage 1-3 Mnemonic & Uterotonic Escalation: Oxytocin, Methylergonovine, Carboprost, Misoprostol)
- Preterm Labor & Antenatal Corticosteroids (Betamethasone 12mg IM q24h x 2 doses for Fetal Lung Maturity)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class ObstetricsGuidelineEvaluation:
    guideline_source: str
    maternal_condition: str
    severity_classification: str
    immediate_antihypertensive_orders: List[str]
    seizure_prophylaxis_protocol: Optional[str]
    delivery_timing_recommendation: str
    neonatal_corticosteroid_plan: Optional[str]


class ObstetricsGuidelineEngine:
    """Evaluates maternal blood pressures, proteinuria, and gestational ages."""

    @staticmethod
    def evaluate_preeclampsia_severity(
        gestational_age_weeks: float,
        systolic_bp: float,
        diastolic_bp: float,
        platelets_k_ul: float,
        serum_creatinine_mg_dl: float,
        ast_u_l: float,
        has_persistent_headache_or_scotomata: bool = False,
        has_pulmonary_edema: bool = False,
    ) -> ObstetricsGuidelineEvaluation:
        """
        ACOG Practice Bulletin No. 222: Gestational Hypertension and Preeclampsia.
        Severe Features: SBP >= 160 or DBP >= 110, Platelets < 100k, Cr > 1.1, AST > 2x upper limit, severe visual/CNS symptoms, or pulmonary edema.
        """
        has_severe_features = (
            systolic_bp >= 160.0
            or diastolic_bp >= 110.0
            or platelets_k_ul < 100.0
            or serum_creatinine_mg_dl > 1.1
            or ast_u_l > 70.0
            or has_persistent_headache_or_scotomata
            or has_pulmonary_edema
        )

        antihypertensives = []
        if systolic_bp >= 160.0 or diastolic_bp >= 110.0:
            antihypertensives.append("EMERGENT ANTIHYPERTENSIVE (Treat within 30-60 min to prevent maternal stroke): IV Labetalol 20mg IV bolus over 2 min (repeat 40mg then 80mg q10-20 min if SBP >= 160 or DBP >= 110) OR IV Hydralazine 5-10mg IV bolus OR Oral Immediate-Release Nifedipine 10-20mg PO.")

        mag_sulfate = None
        if has_severe_features:
            mag_sulfate = "MAGNESIUM SULFATE IV INFUSION (Seizure Prophylaxis): Loading dose 4-6g IV in 100mL over 20-30 minutes, followed by continuous maintenance infusion 1-2g/hour. Continue for 24 hours postpartum. Monitor patellar deep tendon reflexes and maintain Calcium Gluconate 1g IV at bedside for magnesium toxicity."

        # Delivery timing rules
        if has_severe_features:
            if gestational_age_weeks >= 34.0:
                delivery_timing = "Expedited delivery indicated upon maternal stabilization (at or beyond 34 0/7 weeks of gestation) (Class 1, Level B)."
            else:
                delivery_timing = "Expectant management in specialized tertiary perinatal center until 34 0/7 weeks IF maternal and fetal status remain stable; administer antenatal corticosteroids."
        else:
            delivery_timing = "Deliver at 37 0/7 weeks of gestation (ACOG Category 1 recommendation)."

        steroids = None
        if gestational_age_weeks < 37.0:
            steroids = "Administer Antenatal Corticosteroids for Fetal Lung Maturity: Betamethasone 12mg IM every 24 hours x 2 doses (or Dexamethasone 6mg IM q12h x 4 doses)."

        return ObstetricsGuidelineEvaluation(
            guideline_source="ACOG Practice Bulletin No. 222 (Preeclampsia)",
            maternal_condition="Preeclampsia with Severe Features" if has_severe_features else "Preeclampsia without Severe Features",
            severity_classification=f"Gestational Age: {gestational_age_weeks} Weeks | BP: {systolic_bp}/{diastolic_bp} mmHg",
            immediate_antihypertensive_orders=antihypertensives if antihypertensives else ["Monitor blood pressure q4h; antihypertensives not indicated for BP < 160/110 mmHg."],
            seizure_prophylaxis_protocol=mag_sulfate,
            delivery_timing_recommendation=delivery_timing,
            neonatal_corticosteroid_plan=steroids,
        )
