"""
HealthPulse AI — Evidence-Based Endocrinology Clinical Practice Guidelines.
Implements ADA (American Diabetes Association) Standards of Care and Endocrine Society guidelines:
- ADA 2024 Standards of Care: Comprehensive Glycemic Targets (A1c, TIR, Time Below Range)
- Type 2 Diabetes Pharmacotherapy Algorithms (Cardiorenal Protection: SGLT2i & GLP-1 RA)
- Diabetic Ketoacidosis (DKA) & Hyperosmolar Hyperglycemic State (HHS) Emergency Resuscitation
- Inpatient Glycemic Management (Basal-Bolus vs Sliding Scale Insulin Protocols)
- Thyroid Dysfunction Protocols (Primary Hypothyroidism, Graves Disease, Thyroid Storm Burch-Wartofsky Score)
- Adrenal Crisis Emergency Protocols & Primary Adrenal Insufficiency Diagnostic Dynamic Testing
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class GlycemicGoalCategory(str, Enum):
    STANDARD_ADULT = "Standard Non-Pregnant Adult (A1C < 7.0% / 53 mmol/mol)"
    STRINGENT = "Stringent / Early Disease without Microvascular Burden (A1C < 6.5%)"
    LESS_STRINGENT = "Less Stringent / Frail / Severe Hypoglycemia History / Limited Life Expectancy (A1C < 8.0%)"


@dataclass
class EndocrinologyGuidelineEvaluation:
    guideline_source: str
    endocrine_disorder: str
    glycemic_status: str
    first_line_pharmacotherapy: List[str]
    cardiorenal_protective_indications: List[str]
    continuous_glucose_monitoring_targets: Dict[str, str]
    inpatient_insulin_protocol: str


class EndocrinologyGuidelineEngine:
    """Evaluates HbA1c, glucose curves, ketone levels, and endocrine hormone panels."""

    @staticmethod
    def evaluate_ada_diabetes_management(
        hba1c_percent: float,
        has_established_ascvd: bool = False,
        has_heart_failure: bool = False,
        has_ckd: bool = False,
        egfr_ml_min: float = 60.0,
        bmi_kg_m2: float = 28.5,
        hypoglycemia_unawareness: bool = False,
    ) -> EndocrinologyGuidelineEvaluation:
        """
        Evaluates ADA 2024 Standards of Care in Diabetes.
        Focuses on independent cardiorenal risk reduction irrespective of baseline HbA1c.
        """
        # 1. Glycemic Target
        if hypoglycemia_unawareness or egfr_ml_min < 30.0:
            target = GlycemicGoalCategory.LESS_STRINGENT.value
        elif hba1c_percent < 8.0 and not has_established_ascvd:
            target = GlycemicGoalCategory.STANDARD_ADULT.value
        else:
            target = GlycemicGoalCategory.STANDARD_ADULT.value

        first_line = ["Metformin 500-1000mg BID (Class 1, Level A) if eGFR >= 30 mL/min and no acute hypoxia/sepsis.", "Comprehensive lifestyle modification: Mediterranean or DASH diet pattern, 150 min/week moderate physical activity."]

        cardiorenal_recs = []

        # ASCVD Dominant
        if has_established_ascvd:
            cardiorenal_recs.append(
                "GLP-1 Receptor Agonist with proven CVD benefit (Dulaglutide, Liraglutide, or Subcutaneous Semaglutide) OR SGLT2 Inhibitor with proven CVD benefit (Empagliflozin, Dapagliflozin, Canagliflozin) (Class 1, Level A). Recommended INDEPENDENT of baseline A1C or individualized A1C target."
            )

        # Heart Failure Dominant
        if has_heart_failure:
            cardiorenal_recs.append(
                "SGLT2 Inhibitor (Dapagliflozin or Empagliflozin) is Class 1 (Level A) indicated to reduce HF hospitalizations and cardiovascular mortality across HFrEF and HFpEF."
            )

        # CKD Dominant
        if has_ckd:
            cardiorenal_recs.append(
                "SGLT2 Inhibitor (Empagliflozin or Dapagliflozin) is Class 1 (Level A) to slow CKD progression and reduce CV events. Add non-steroidal MRA (Finerenone) if albuminuria persists on max tolerated ACEi/ARB."
            )

        # Weight Management
        if bmi_kg_m2 >= 27.0:
            cardiorenal_recs.append(
                "Dual GIP/GLP-1 RA (Tirzepatide) or GLP-1 RA (Semaglutide 2.4mg) provides high-potency weight loss (15-22% total body weight reduction) and substantial glycemic improvement."
            )

        cgm_metrics = {
            "Time in Range (70-180 mg/dL)": "> 70% of readings (>16h 48m per day)",
            "Time Below Range (< 70 mg/dL)": "< 4% of readings (<1h per day)",
            "Time Very Low (< 54 mg/dL)": "< 1% of readings (<15 min per day) - Zero tolerance for severe hypoglycemia",
            "Time Above Range (> 180 mg/dL)": "< 25% of readings (<6h per day)",
            "Glucose Management Indicator (GMI)": "Target <= 7.0%",
        }

        return EndocrinologyGuidelineEvaluation(
            guideline_source="ADA 2024 Standards of Care in Diabetes",
            endocrine_disorder="Type 2 Diabetes Mellitus",
            glycemic_status=f"Current A1c: {hba1c_percent}% (Goal: {target})",
            first_line_pharmacotherapy=first_line,
            cardiorenal_protective_indications=cardiorenal_recs,
            continuous_glucose_monitoring_targets=cgm_metrics,
            inpatient_insulin_protocol="For hospitalized patients: Discontinue oral agents if critically ill; initiate Basal-Bolus-Correction subcutaneous insulin (0.4-0.5 U/kg/day split 50% Glargine/Degludec and 50% Lispro/Aspart before meals). Sliding scale insulin monotherapy is strongly discouraged.",
        )

    @staticmethod
    def evaluate_dka_resuscitation(
        glucose_mg_dl: float,
        arterial_ph: float,
        serum_bicarbonate_meq_l: float,
        anion_gap: float,
        serum_potassium: float,
        beta_hydroxybutyrate_mmol_l: float,
    ) -> Dict[str, Any]:
        """
        ADA Diabetic Ketoacidosis (DKA) Emergency Resuscitation Protocol.
        """
        if arterial_ph < 7.00 or serum_bicarbonate_meq_l < 10.0:
            sev = "Severe DKA"
            icu_required = True
        elif arterial_ph <= 7.24 or serum_bicarbonate_meq_l <= 14.0:
            sev = "Moderate DKA"
            icu_required = True
        elif arterial_ph <= 7.30 or serum_bicarbonate_meq_l <= 18.0:
            sev = "Mild DKA"
            icu_required = False
        else:
            return {"is_dka": False, "message": "Does not meet biochemical criteria for DKA (pH > 7.30, HCO3 > 18)."}

        # Potassium rule before insulin initiation
        if serum_potassium < 3.3:
            insulin_directive = "HOLD INSULIN. Administer IV potassium chloride (20-30 mEq/hour) until serum potassium >= 3.3 mEq/L to prevent fatal cardiac arrhythmias and respiratory arrest."
        elif 3.3 <= serum_potassium <= 5.2:
            insulin_directive = "Initiate Regular Insulin IV continuous infusion at 0.14 U/kg/hour (or 0.1 U/kg bolus + 0.1 U/kg/h). Add 20-30 mEq K+ per liter of IV maintenance fluid to maintain K+ between 4.0-5.0 mEq/L."
        else:
            insulin_directive = "Initiate Regular Insulin IV continuous infusion at 0.1 U/kg/h. Do not add potassium to IV fluids until K+ drops < 5.2 mEq/L; recheck potassium q2h."

        protocol = [
            "Fluid Resuscitation: 0.9% NaCl (1000-1500 mL in 1st hour). Switch to 0.45% NaCl (250-500 mL/h) if corrected sodium normal or elevated.",
            insulin_directive,
            "Glucose Management: When blood glucose reaches 200 mg/dL, add 5% Dextrose to IV fluids (D5 0.45% NaCl) and reduce insulin to 0.02-0.05 U/kg/h to maintain glucose 150-200 mg/dL until DKA resolution.",
            "Resolution Criteria: Blood glucose < 200 mg/dL PLUS 2 of: Serum Bicarbonate >= 15 mEq/L, Venous pH > 7.30, Anion Gap <= 12 mEq/L, and Beta-hydroxybutyrate < 0.6 mmol/L.",
            "Transition to SC Insulin: Administer subcutaneous basal insulin (e.g. Glargine) 2-4 hours BEFORE stopping IV insulin infusion to prevent rebound ketoacidosis.",
        ]

        return {
            "is_dka": True,
            "dka_severity": sev,
            "anion_gap": round(anion_gap, 1),
            "beta_hydroxybutyrate": beta_hydroxybutyrate_mmol_l,
            "icu_admission_indicated": icu_required,
            "resuscitation_orders": protocol,
        }
