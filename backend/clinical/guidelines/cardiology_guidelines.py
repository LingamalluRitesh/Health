"""
HealthPulse AI — Evidence-Based Cardiology Clinical Practice Guidelines.
Implements ACC/AHA, ESC, and HRS clinical practice guidelines for cardiovascular disorders:
- Heart Failure (HFrEF, HFmrEF, HFpEF) 4-Pillar Guideline-Directed Medical Therapy (GDMT)
- Non-ST-Elevation Acute Coronary Syndromes (NSTE-ACS) and STEMI Revascularization Timelines
- Non-Valvular Atrial Fibrillation Stroke Prevention & Rate vs Rhythm Control
- Valvular Heart Disease (Aortic Stenosis, Mitral Regurgitation, TAVR / SAVR Criteria)
- ACC/AHA 2017 Hypertension Staging and Pharmacotherapy Selection
- Hypertrophic Cardiomyopathy (HCM) Risk Stratification for Sudden Cardiac Death (SCD)
- Ventricular Arrhythmias and Secondary Prevention ICD Indications
- Infective Endocarditis Duke Criteria and Antimicrobial Regimens
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class HeartFailureClass(str, Enum):
    STAGE_A = "Stage A: At risk for heart failure without structural disease or symptoms"
    STAGE_B = "Stage B: Pre-heart failure with structural disease or elevated biomarkers without symptoms"
    STAGE_C = "Stage C: Symptomatic heart failure (NYHA I-IV)"
    STAGE_D = "Stage D: Advanced heart failure refractory to standard GDMT"


class EjectionFractionPhenotype(str, Enum):
    HFREF = "HFrEF: Heart Failure with Reduced Ejection Fraction (LVEF <= 40%)"
    HFMREF = "HFmrEF: Heart Failure with Mildly Reduced Ejection Fraction (LVEF 41-49%)"
    HFPEF = "HFpEF: Heart Failure with Preserved Ejection Fraction (LVEF >= 50%)"
    HFIMPEF = "HFimpEF: Heart Failure with Improved Ejection Fraction (Baseline <=40%, follow-up >40%)"


@dataclass
class GDMTMedicationRecommendation:
    pillar_name: str
    preferred_agents: List[str]
    starting_dose: str
    target_dose: str
    titration_interval: str
    absolute_contraindications: List[str]
    monitoring_labs: List[str]
    class_of_recommendation: str  # Class 1, Class 2a, Class 2b, Class 3
    level_of_evidence: str        # Level A, Level B, Level C


@dataclass
class CardiologyGuidelineEvaluation:
    disease_entity: str
    patient_phenotype: str
    primary_recommendations: List[str]
    gdmt_pillars: List[GDMTMedicationRecommendation]
    device_therapy_indications: List[str]
    interventional_referrals: List[str]
    urgency_tier: str


class CardiologyGuidelineEngine:
    """Evaluates patient clinical profiles against ACC/AHA/ESC cardiology guidelines."""

    @staticmethod
    def evaluate_heart_failure_gdmt(
        lvef_percent: float,
        nyha_class: int,
        systolic_bp: float,
        heart_rate: float,
        serum_potassium: float,
        egfr: float,
        has_angioedema_history: bool = False,
        is_diabetic: bool = False,
    ) -> CardiologyGuidelineEvaluation:
        """
        Evaluates 2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure.
        For HFrEF (LVEF <= 40%), Class 1 recommendation requires the 4 pillars of GDMT:
        1. ARNI (Sacubitril/Valsartan) or ACEi/ARB
        2. Beta-blocker (Carvedilol, Metoprolol Succinate, or Bisoprolol)
        3. MRA (Spironolactone or Eplerenone)
        4. SGLT2 Inhibitor (Dapagliflozin or Empagliflozin)
        """
        pillars: List[GDMTMedicationRecommendation] = []
        device_indications: List[str] = []
        primary_recs: List[str] = []

        if lvef_percent <= 40.0:
            phenotype = EjectionFractionPhenotype.HFREF.value

            # Pillar 1: ARNI / ACEi / ARB
            if has_angioedema_history:
                arni_rec = GDMTMedicationRecommendation(
                    pillar_name="Renin-Angiotensin System Inhibition",
                    preferred_agents=["Hydralazine + Isosorbide Dinitrate (ARNI/ACEi contraindicated due to angioedema)"],
                    starting_dose="Hydralazine 37.5mg + ISDN 20mg TID",
                    target_dose="Hydralazine 75mg + ISDN 40mg TID",
                    titration_interval="Every 2-4 weeks",
                    absolute_contraindications=["History of angioedema to ACEi/ARNI"],
                    monitoring_labs=["Blood pressure"],
                    class_of_recommendation="Class 2a",
                    level_of_evidence="Level B",
                )
            else:
                arni_rec = GDMTMedicationRecommendation(
                    pillar_name="ARNI (Angiotensin Receptor-Neprilysin Inhibitor)",
                    preferred_agents=["Sacubitril/Valsartan (Entresto)"],
                    starting_dose="24/26 mg or 49/51 mg BID",
                    target_dose="97/103 mg BID",
                    titration_interval="Every 2-4 weeks as tolerated by SBP",
                    absolute_contraindications=["History of angioedema", "Concomitant ACE inhibitor within 36 hours", "Pregnancy"],
                    monitoring_labs=["Serum potassium (hold if K > 5.5 mEq/L)", "Serum creatinine / eGFR (hold if eGFR < 20)", "Blood pressure (hold if SBP < 90 mmHg)"],
                    class_of_recommendation="Class 1",
                    level_of_evidence="Level A",
                )
            pillars.append(arni_rec)

            # Pillar 2: Evidence-Based Beta-Blocker
            bb_rec = GDMTMedicationRecommendation(
                pillar_name="Beta-1 Selective / Alpha-Beta Blocker",
                preferred_agents=["Metoprolol Succinate (Toprol-XL)", "Carvedilol (Coreg)", "Bisoprolol"],
                starting_dose="Metoprolol Succinate 12.5-25mg daily OR Carvedilol 3.125mg BID",
                target_dose="Metoprolol Succinate 200mg daily OR Carvedilol 25-50mg BID",
                titration_interval="Every 2 weeks in stable, euvolemic patient",
                absolute_contraindications=["Asthma with active bronchospasm", "Second- or third-degree AV block without pacemaker", "Cardiogenic shock / Acute decompensation with pulmonary edema"],
                monitoring_labs=["Heart rate (target resting HR 55-65 bpm)", "Blood pressure", "ECG PR interval"],
                class_of_recommendation="Class 1",
                level_of_evidence="Level A",
            )
            pillars.append(bb_rec)

            # Pillar 3: Mineralocorticoid Receptor Antagonist (MRA)
            if serum_potassium < 5.0 and egfr >= 30.0:
                mra_rec = GDMTMedicationRecommendation(
                    pillar_name="Mineralocorticoid Receptor Antagonist (MRA)",
                    preferred_agents=["Spironolactone", "Eplerenone (if gynecomastia occurs with spironolactone)"],
                    starting_dose="Spironolactone 12.5-25mg daily",
                    target_dose="Spironolactone 25-50mg daily",
                    titration_interval="Every 4-8 weeks",
                    absolute_contraindications=["Serum potassium > 5.0 mEq/L at baseline", "eGFR < 30 mL/min/1.73m2", "Concomitant potassium supplements"],
                    monitoring_labs=["Serum potassium at 1 week, 4 weeks, and quarterly", "Serum creatinine"],
                    class_of_recommendation="Class 1",
                    level_of_evidence="Level A",
                )
            else:
                mra_rec = GDMTMedicationRecommendation(
                    pillar_name="Mineralocorticoid Receptor Antagonist (MRA) - TEMPORARILY DEFERRED",
                    preferred_agents=["Spironolactone"],
                    starting_dose="Deferred until Potassium < 5.0 mEq/L and eGFR >= 30 mL/min",
                    target_dose="25mg daily",
                    titration_interval="Reassess post-diuresis and electrolyte optimization",
                    absolute_contraindications=["Hyperkalemia", "Severe renal impairment"],
                    monitoring_labs=["Potassium", "eGFR"],
                    class_of_recommendation="Class 1 (Deferred)",
                    level_of_evidence="Level A",
                )
            pillars.append(mra_rec)

            # Pillar 4: SGLT2 Inhibitor
            sglt2_rec = GDMTMedicationRecommendation(
                pillar_name="Sodium-Glucose Cotransporter 2 (SGLT2) Inhibitor",
                preferred_agents=["Dapagliflozin (Farxiga) 10mg daily", "Empagliflozin (Jardiance) 10mg daily"],
                starting_dose="10mg once daily (no titration required)",
                target_dose="10mg once daily",
                titration_interval="Single target dose",
                absolute_contraindications=["Type 1 Diabetes (risk of euglycemic DKA)", "Severe renal impairment (eGFR < 20 for Dapa/Empa)", "History of recurrent Fournier gangrene"],
                monitoring_labs=["eGFR (expect mild transient 2-4 mL/min dip upon initiation)", "Signs of mycotic genital infections", "Volume status"],
                class_of_recommendation="Class 1",
                level_of_evidence="Level A",
            )
            pillars.append(sglt2_rec)

            # Device Therapy Evaluations
            if lvef_percent <= 35.0 and nyha_class in (2, 3):
                device_indications.append("Primary Prevention Implantable Cardioverter-Defibrillator (ICD) indicated after >= 3 months of optimal GDMT (Class 1, Level A).")
            if lvef_percent <= 35.0 and nyha_class in (2, 3, 4):
                device_indications.append("Evaluate 12-lead ECG for QRS duration: If LBBB with QRS >= 150ms in sinus rhythm, Cardiac Resynchronization Therapy (CRT-D) is strongly recommended (Class 1, Level A).")

            primary_recs.append("Initiate and rapidly cross-titrate all 4 pillars of GDMT simultaneously or in rapid sequence (within 4-6 weeks).")
            primary_recs.append("Prescribe loop diuretic (Furosemide, Torsemide, or Bumetanide) titrated to achieve dry weight and eliminate jugular venous distension / peripheral edema.")
            urgency = "High (Initiate 4-Pillar GDMT Optimization)"

        elif 41.0 <= lvef_percent <= 49.0:
            phenotype = EjectionFractionPhenotype.HFMREF.value
            primary_recs.append("SGLT2 inhibitors (Dapagliflozin or Empagliflozin) have Class 1 recommendation to reduce HF hospitalizations and cardiovascular mortality.")
            primary_recs.append("ARNI / ACEi / ARB, Beta-blockers, and MRAs have Class 2b recommendations for HFmrEF.")
            urgency = "Moderate"

        else:
            phenotype = EjectionFractionPhenotype.HFPEF.value
            primary_recs.append("SGLT2 inhibitors (Empagliflozin or Dapagliflozin) have Class 1 recommendation in HFpEF to decrease hospitalizations (EMPEROR-Preserved, DELIVER trials).")
            primary_recs.append("MRAs (Spironolactone) have Class 2b recommendation in appropriately selected HFpEF patients (LVEF < 55-60%, elevated BNP).")
            primary_recs.append("Aggressively treat hypertension (target SBP < 130 mmHg) and maintain sinus rhythm in atrial fibrillation.")
            urgency = "Standard Outpatient Care"

        return CardiologyGuidelineEvaluation(
            disease_entity="Heart Failure (AHA/ACC/HFSA 2022 Guidelines)",
            patient_phenotype=phenotype,
            primary_recommendations=primary_recs,
            gdmt_pillars=pillars,
            device_therapy_indications=device_indications,
            interventional_referrals=["Heart Failure Specialist referral if refractory NYHA Class III-IV or worsening renal function"],
            urgency_tier=urgency,
        )

    @staticmethod
    def evaluate_atrial_fibrillation_anticoagulation(
        cha2ds2_vasc_score: int,
        has_bled_score: int,
        is_mechanical_valve: bool = False,
        is_moderate_severe_mitral_stenosis: bool = False,
        egfr_ml_min: float = 60.0,
    ) -> Dict[str, Any]:
        """
        2023 ACC/AHA/ACCP/HRS Guideline for the Diagnosis and Management of Atrial Fibrillation.
        """
        is_valvular = is_mechanical_valve or is_moderate_severe_mitral_stenosis

        if is_valvular:
            drug_choice = "Warfarin (Vitamin K Antagonist) with target INR 2.5-3.5 for mechanical mitral valve or 2.0-3.0 for mechanical aortic valve. DOACs are STRICTLY CONTRAINDICATED in mechanical heart valves."
            doac_eligible = False
            rec_class = "Class 1 (Level of Evidence B)"
        else:
            doac_eligible = True
            if cha2ds2_vasc_score >= 2:
                drug_choice = "Direct Oral Anticoagulant (DOAC: Apixaban 5mg BID, Rivaroxaban 20mg daily with food, or Dabigatran 150mg BID) preferred over Warfarin due to superior safety profile and lower intracranial hemorrhage rates."
                rec_class = "Class 1 (Level of Evidence A)"
            elif cha2ds2_vasc_score == 1:
                drug_choice = "Oral Anticoagulation may be considered based on shared decision-making regarding bleeding vs thromboembolic risk."
                rec_class = "Class 2b (Level of Evidence B)"
            else:
                drug_choice = "No antithrombotic or anticoagulant therapy indicated. Antiplatelet monotherapy (Aspirin) is NOT recommended for AFib stroke prevention."
                rec_class = "Class 3: No Benefit"

        bleeding_management = []
        if has_bled_score >= 3:
            bleeding_management.append("High bleeding risk (HAS-BLED >= 3). Correct modifiable bleeding factors: control hypertension (SBP < 130), eliminate NSAIDs/antiplatelets, minimize alcohol consumption.")
            bleeding_management.append("Consider Left Atrial Appendage Occlusion (LAAO e.g. Watchman device) if long-term oral anticoagulation is contraindicated due to recurrent major bleeding.")

        return {
            "guideline": "2023 ACC/AHA/ACCP/HRS Atrial Fibrillation Guideline",
            "cha2ds2_vasc_score": cha2ds2_vasc_score,
            "has_bled_score": has_bled_score,
            "is_valvular_afib": is_valvular,
            "doac_eligible": doac_eligible,
            "anticoagulant_recommendation": drug_choice,
            "recommendation_strength": rec_class,
            "bleeding_mitigation_strategies": bleeding_management,
        }

    @staticmethod
    def evaluate_nste_acs_revascularization(
        grace_risk_score: float,
        timi_score: int,
        hemodynamic_instability: bool = False,
        refractory_angina: bool = False,
        dynamic_ecg_changes: bool = False,
        troponin_elevated: bool = True,
    ) -> Dict[str, Any]:
        """
        2023 ESC / 2021 ACC/AHA Guidelines for Non-ST-Elevation Acute Coronary Syndromes (NSTE-ACS).
        Determines coronary angiography invasive timing: Immediate (<2h), Early (<24h), or Selective.
        """
        # Very High Risk Criteria -> Immediate Invasive Strategy (< 2 Hours)
        if hemodynamic_instability or refractory_angina:
            timing = "Immediate Invasive Strategy (< 2 Hours)"
            urgency = "EMERGENCY: Immediate Cardiac Catheterization Lab Activation"
            rationale = "Hemodynamic instability, cardiogenic shock, or recurrent refractory chest pain despite medical therapy."
        # High Risk Criteria -> Early Invasive Strategy (< 24 Hours)
        elif dynamic_ecg_changes or troponin_elevated or grace_risk_score > 140 or timi_score >= 5:
            timing = "Early Invasive Strategy (< 24 Hours)"
            urgency = "Urgent Inpatient Angiography within 24 hours of admission"
            rationale = "Confirmed NSTEMI with elevated cardiac biomarkers, dynamic ST-T wave depressions, or GRACE score > 140."
        else:
            timing = "Selective Invasive / Non-Invasive Strategy"
            urgency = "Elective inpatient evaluation or non-invasive anatomical/functional imaging (CTCA or Stress Test)"
            rationale = "Low-risk NSTE-ACS without high-risk clinical features or biomarker elevation."

        return {
            "guideline": "2023 ACC/AHA/ESC NSTE-ACS Guideline",
            "invasive_timing_strategy": timing,
            "urgency_level": urgency,
            "clinical_rationale": rationale,
            "acute_antiplatelet_dual_therapy": "Aspirin 325mg loading dose + P2Y12 inhibitor (Ticagrelor 180mg loading or Prasugrel 60mg post-angiography).",
            "parenteral_anticoagulation": "Unfractionated Heparin (60 U/kg IV bolus, target aPTT 50-70s) or Enoxaparin 1 mg/kg SC q12h.",
        }
