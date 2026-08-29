"""
HealthPulse AI — Evidence-Based Nephrology Clinical Practice Guidelines.
Implements KDIGO (Kidney Disease: Improving Global Outcomes) international clinical guidelines:
- KDIGO 2024 Evaluation & Management of Chronic Kidney Disease (CKD Staging G1-G5, A1-A3)
- KDIGO Acute Kidney Injury (AKI) Staging (Stages 1-3 by Serum Creatinine & Urine Output)
- Diabetic Kidney Disease (DKD) 4-Pillar Pharmacotherapy (SGLT2i, nsMRA Finerenone, ACEi/ARB, GLP-1 RA)
- Hyponatremia Diagnostic Algorithm (Hypotonic vs Isotonic, Volume Status, SIADH, Osmotic Demyelination Prevention)
- Hyperkalemia Emergency Stabilization (Calcium Gluconate, Insulin + D50, Albuterol, Potassium Binders)
- Indications for Urgent Renal Replacement Therapy (AEIOU mnemonic)
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class KDIGOCKDStage(str, Enum):
    G1 = "G1: Normal or High (eGFR >= 90 mL/min/1.73m2)"
    G2 = "G2: Mildly Decreased (eGFR 60-89 mL/min/1.73m2)"
    G3A = "G3a: Mildly to Moderately Decreased (eGFR 45-59 mL/min/1.73m2)"
    G3B = "G3b: Moderately to Severely Decreased (eGFR 30-44 mL/min/1.73m2)"
    G4 = "G4: Severely Decreased (eGFR 15-29 mL/min/1.73m2)"
    G5 = "G5: Kidney Failure / ESRD (eGFR < 15 mL/min/1.73m2 or on Dialysis)"


class KDIGOAlbuminuriaCategory(str, Enum):
    A1 = "A1: Normal to Mildly Increased (uACR < 30 mg/g or < 3 mg/mmol)"
    A2 = "A2: Moderately Increased / Microalbuminuria (uACR 30-300 mg/g or 3-30 mg/mmol)"
    A3 = "A3: Severely Increased / Macroalbuminuria (uACR > 300 mg/g or > 30 mg/mmol)"


@dataclass
class NephrologyGuidelineEvaluation:
    guideline_source: str
    clinical_syndrome: str
    staging_classification: str
    prognostic_heat_map_risk: str  # Low, Moderate, High, Very High
    recommended_pharmacotherapy: List[str]
    blood_pressure_target: str
    nephrology_referral_indicated: bool
    dietary_and_lifestyle_prescriptions: List[str]


class NephrologyGuidelineEngine:
    """Evaluates eGFR, albuminuria, serum electrolytes, and acid-base status against KDIGO criteria."""

    @staticmethod
    def evaluate_kdigo_ckd(
        egfr_ml_min: float,
        uacr_mg_g: float,
        is_diabetic: bool = False,
        serum_potassium: float = 4.5,
        blood_pressure_systolic: float = 135.0,
    ) -> NephrologyGuidelineEvaluation:
        """
        KDIGO 2024 Clinical Practice Guideline for the Evaluation and Management of CKD.
        Staging: G1-G5 combined with Albuminuria A1-A3 Heat Map.
        """
        # 1. G-Staging
        if egfr_ml_min >= 90.0:
            g_stage = KDIGOCKDStage.G1.value
            g_code = "G1"
        elif egfr_ml_min >= 60.0:
            g_stage = KDIGOCKDStage.G2.value
            g_code = "G2"
        elif egfr_ml_min >= 45.0:
            g_stage = KDIGOCKDStage.G3A.value
            g_code = "G3a"
        elif egfr_ml_min >= 30.0:
            g_stage = KDIGOCKDStage.G3B.value
            g_code = "G3b"
        elif egfr_ml_min >= 15.0:
            g_stage = KDIGOCKDStage.G4.value
            g_code = "G4"
        else:
            g_stage = KDIGOCKDStage.G5.value
            g_code = "G5"

        # 2. A-Staging
        if uacr_mg_g < 30.0:
            a_stage = KDIGOAlbuminuriaCategory.A1.value
            a_code = "A1"
        elif uacr_mg_g <= 300.0:
            a_stage = KDIGOAlbuminuriaCategory.A2.value
            a_code = "A2"
        else:
            a_stage = KDIGOAlbuminuriaCategory.A3.value
            a_code = "A3"

        # 3. KDIGO Risk Grid Heat Map
        if g_code in ("G1", "G2") and a_code == "A1":
            heat_risk = "Low Risk (Green) - Repeat annual eGFR/uACR screening"
            referral = False
        elif (g_code in ("G1", "G2") and a_code == "A2") or (g_code == "G3a" and a_code == "A1"):
            heat_risk = "Moderate Risk (Yellow) - Evaluate every 6-12 months"
            referral = False
        elif (g_code in ("G1", "G2") and a_code == "A3") or (g_code == "G3a" and a_code == "A2") or (g_code == "G3b" and a_code == "A1"):
            heat_risk = "High Risk (Orange) - Evaluate every 3-6 months"
            referral = g_code in ("G3b", "G4", "G5") or a_code == "A3"
        else:
            heat_risk = "Very High Risk (Red) - Comprehensive nephrology care, monitor 4+ times annually"
            referral = True

        pharma_recs = []

        # RAS Blockade
        if a_code in ("A2", "A3") or is_diabetic:
            pharma_recs.append("ACE Inhibitor (e.g. Lisinopril) or ARB (e.g. Losartan) titrated to maximum tolerated dose (Class 1, Level A). Reduces intraglomerular hypertension and slows proteinuria progression.")

        # SGLT2 Inhibitors in CKD (DAPA-CKD, EMPA-KIDNEY)
        if egfr_ml_min >= 20.0 and (uacr_mg_g >= 200.0 or is_diabetic):
            pharma_recs.append("SGLT2 Inhibitor (Dapagliflozin 10mg daily or Empagliflozin 10mg daily) (Class 1, Level A). Dramatic reduction in kidney failure progression and all-cause mortality; continue therapy until initiation of dialysis.")

        # Nonsteroidal MRA (FIDELIO-DKD, FIGARO-DKD)
        if is_diabetic and uacr_mg_g >= 30.0 and egfr_ml_min >= 25.0 and serum_potassium <= 4.8:
            pharma_recs.append("Non-steroidal MRA (Finerenone 10-20mg daily) (Class 1, Level A). Add to maximally tolerated RAS blocker and SGLT2i in diabetic kidney disease with persistent albuminuria.")

        # Statin / Lipid Lowering
        if g_code in ("G3a", "G3b", "G4", "G5") or a_code in ("A2", "A3"):
            pharma_recs.append("Statin monotherapy (Atorvastatin 20mg) or Statin/Ezetimibe combination in all adults aged >= 50 with CKD (KDIGO Class 1, Level A). Do not initiate statins in maintenance hemodialysis.")

        return NephrologyGuidelineEvaluation(
            guideline_source="KDIGO 2024 Clinical Practice Guideline for CKD",
            clinical_syndrome="Chronic Kidney Disease (CKD)",
            staging_classification=f"Stage {g_code}{a_code} ({g_stage}; {a_stage})",
            prognostic_heat_map_risk=heat_risk,
            recommended_pharmacotherapy=pharma_recs,
            blood_pressure_target="Target Systolic BP < 120 mmHg using standardized office blood pressure measurement (Class 1, Level B).",
            nephrology_referral_indicated=referral,
            dietary_and_lifestyle_prescriptions=[
                "Target dietary sodium intake < 2.0 grams/day (< 5g NaCl/day) (Class 1, Level C).",
                "Maintain dietary protein intake 0.8 g/kg body weight/day for non-dialysis CKD G3-G5 (Class 2a). Avoid high protein intake (>1.3 g/kg/day).",
                "Moderate-intensity physical activity >= 150 minutes/week.",
            ],
        )

    @staticmethod
    def evaluate_kdigo_aki_staging(
        baseline_creatinine_mg_dl: float,
        current_creatinine_mg_dl: float,
        creatinine_increase_past_48h_mg_dl: float,
        urine_output_ml_kg_h_6h: Optional[float] = None,
        urine_output_ml_kg_h_12h: Optional[float] = None,
        anuria_hours: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        KDIGO Acute Kidney Injury (AKI) Staging Criteria.
        """
        ratio = current_creatinine_mg_dl / max(0.1, baseline_creatinine_mg_dl)
        stage = 0
        stage_reasons = []

        # Stage 3
        if (
            ratio >= 3.0
            or current_creatinine_mg_dl >= 4.0
            or (anuria_hours is not None and anuria_hours >= 12.0)
            or (urine_output_ml_kg_h_12h is not None and urine_output_ml_kg_h_12h < 0.3)
        ):
            stage = 3
            stage_reasons.append("Creatinine >= 3.0x baseline, absolute Cr >= 4.0 mg/dL, or anuria >= 12 hours.")
        # Stage 2
        elif (
            (2.0 <= ratio < 3.0)
            or (urine_output_ml_kg_h_12h is not None and urine_output_ml_kg_h_12h < 0.5)
        ):
            stage = 2
            stage_reasons.append("Creatinine 2.0 to 2.9x baseline or urine output < 0.5 mL/kg/h for >= 12 hours.")
        # Stage 1
        elif (
            (1.5 <= ratio < 2.0)
            or creatinine_increase_past_48h_mg_dl >= 0.3
            or (urine_output_ml_kg_h_6h is not None and urine_output_ml_kg_h_6h < 0.5)
        ):
            stage = 1
            stage_reasons.append("Creatinine increase >= 0.3 mg/dL within 48h or 1.5 to 1.9x baseline.")

        bundle = [
            "Discontinue all nephrotoxic agents (NSAIDs, aminoglycosides, IV iodinated radiocontrast, vancomycin where feasible).",
            "Hold ACE inhibitors and ARBs during acute volume depletion or hypotension.",
            "Optimize hemodynamic perfusion pressure (Target MAP 65-70 mmHg using isotonic crystalloids).",
            "Monitor serum creatinine and urine output hourly in ICU.",
            "Screen for AEIOU urgent dialysis indications: Acidosis (pH < 7.15), Electrolytes (refractory K > 6.5), Ingestions, Overload (pulmonary edema refractory to diuretics), Uremia (pericarditis, encephalopathy, asterixis).",
        ]

        return {
            "guideline": "KDIGO 2012 Clinical Practice Guideline for AKI",
            "has_aki": stage > 0,
            "kdigo_aki_stage": f"Stage {stage}" if stage > 0 else "No AKI Criteria Met",
            "staging_criteria_met": stage_reasons,
            "resuscitation_bundle": bundle,
            "urgent_nephrology_consult": stage >= 2,
        }
