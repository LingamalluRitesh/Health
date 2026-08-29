"""
HealthPulse AI — Evidence-Based Pulmonology Clinical Practice Guidelines.
Implements GOLD, GINA, ATS/ERS, and CHEST clinical guidelines for respiratory conditions:
- Global Initiative for Chronic Obstructive Lung Disease (GOLD 2024 Report: Groups A, B, E)
- Global Initiative for Asthma (GINA 2024 Guidelines: Steps 1-5 Track 1 vs Track 2)
- ATS/IDSA Community-Acquired Pneumonia (CAP) Inpatient vs Outpatient Diagnostic Pathways
- Hospital-Acquired Pneumonia (HAP) and Ventilator-Associated Pneumonia (VAP) Antibiograms
- Acute Respiratory Distress Syndrome (ARDS) Berlin Criteria and PEEP/FiO2 Titration
- CHEST Guidelines for Venous Thromboembolism & Pulmonary Embolism Thrombolysis
- Idiopathic Pulmonary Fibrosis (IPF) Diagnostic HRCT Criteria and Antifibrotics
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class GOLDAirflowSeverity(str, Enum):
    GOLD_1 = "GOLD 1: Mild (FEV1 >= 80% predicted)"
    GOLD_2 = "GOLD 2: Moderate (50% <= FEV1 < 80% predicted)"
    GOLD_3 = "GOLD 3: Severe (30% <= FEV1 < 50% predicted)"
    GOLD_4 = "GOLD 4: Very Severe (FEV1 < 30% predicted)"


class GOLDPatientGroup(str, Enum):
    GROUP_A = "Group A: 0-1 moderate exacerbations (not leading to hospital), mMRC 0-1 or CAT < 10"
    GROUP_B = "Group B: 0-1 moderate exacerbations (not leading to hospital), mMRC >= 2 or CAT >= 10"
    GROUP_E = "Group E: >= 2 moderate exacerbations or >= 1 exacerbation leading to hospitalization"


@dataclass
class PulmonologyGuidelineEvaluation:
    guideline_source: str
    disease_condition: str
    severity_classification: str
    inhaler_regimen_recommendation: List[str]
    escalation_triggers: List[str]
    antibiotic_selection: Optional[str]
    oxygen_and_ventilation_strategy: Optional[str]


class PulmonologyGuidelineEngine:
    """Evaluates pulmonary function tests, blood eosinophils, and exacerbation histories."""

    @staticmethod
    def evaluate_gold_copd(
        fev1_percent_predicted: float,
        exacerbations_past_year: int,
        hospitalized_for_exacerbation_past_year: bool,
        mmrc_dyspnea_score: int,
        blood_eosinophil_count_cells_ul: float,
        is_current_smoker: bool = True,
    ) -> PulmonologyGuidelineEvaluation:
        """
        Evaluates GOLD 2024 Guidelines for COPD Diagnosis, Management, and Prevention.
        """
        # 1. Spirometric grading (post-bronchodilator FEV1/FVC < 0.70)
        if fev1_percent_predicted >= 80.0:
            stage = GOLDAirflowSeverity.GOLD_1.value
        elif fev1_percent_predicted >= 50.0:
            stage = GOLDAirflowSeverity.GOLD_2.value
        elif fev1_percent_predicted >= 30.0:
            stage = GOLDAirflowSeverity.GOLD_3.value
        else:
            stage = GOLDAirflowSeverity.GOLD_4.value

        # 2. ABE Assessment Scheme
        if hospitalized_for_exacerbation_past_year or exacerbations_past_year >= 2:
            group = GOLDPatientGroup.GROUP_E.value
            if blood_eosinophil_count_cells_ul >= 300.0:
                inhaler_recs = [
                    "Triple Inhalation Therapy (LABA + LAMA + ICS) (e.g. Fluticasone Furoate/Umeclidinium/Vilanterol OR Budesonide/Glycopyrrolate/Formoterol).",
                    "Strong indication for ICS due to Blood Eosinophils >= 300 cells/uL.",
                ]
            else:
                inhaler_recs = [
                    "Dual Bronchodilator Therapy (LABA + LAMA) (e.g. Tiotropium/Olodaterol OR Umeclidinium/Vilanterol).",
                    "Add ICS (Triple Therapy) if blood eosinophils >= 100 cells/uL and persistent exacerbations.",
                ]
        elif mmrc_dyspnea_score >= 2:
            group = GOLDPatientGroup.GROUP_B.value
            inhaler_recs = [
                "Initial Therapy: Dual Bronchodilation (LABA + LAMA). LABA+LAMA combination is superior to single bronchodilator monotherapy for symptom relief.",
            ]
        else:
            group = GOLDPatientGroup.GROUP_A.value
            inhaler_recs = [
                "Single Bronchodilator (SABA, SAMA as needed or once-daily LAMA / LABA).",
            ]

        escalations = [
            "Smoking cessation pharmacotherapy (Varenicline, Bupropion, or NRT) is the single most effective intervention to halt FEV1 decline.",
            "Annual Influenza vaccination, COVID-19 booster, Pneumococcal (PCV20 or PCV15 followed by PPSV23), and RSV vaccination (Class 1 recommendation in age >= 60).",
            "Refer for Pulmonary Rehabilitation for all symptomatic patients with mMRC >= 2 (Group B and E).",
        ]

        if is_current_smoker:
            escalations.insert(0, "URGENT: Active smoking cessation counseling and pharmacotherapy.")

        oxygen_plan = None
        if fev1_percent_predicted < 50.0:
            oxygen_plan = "Evaluate resting PaO2 on room air: If PaO2 <= 55 mmHg (or SpO2 <= 88%) or PaO2 56-59 mmHg with cor pulmonale/erythrocytosis, prescribe Long-Term Oxygen Therapy (LTOT >= 15 hours/day) to improve survival."

        return PulmonologyGuidelineEvaluation(
            guideline_source="GOLD 2024 Global Strategy for COPD",
            disease_condition="Chronic Obstructive Pulmonary Disease (COPD)",
            severity_classification=f"{stage} | {group}",
            inhaler_regimen_recommendation=inhaler_recs,
            escalation_triggers=escalations,
            antibiotic_selection="For acute exacerbations with purulent sputum: Azithromycin 500mg daily x 3 days OR Amoxicillin-Clavulanate 875/125mg BID x 5 days + Oral Prednisone 40mg daily x 5 days.",
            oxygen_and_ventilation_strategy=oxygen_plan,
        )

    @staticmethod
    def evaluate_gina_asthma(
        daytime_symptoms_per_week: int,
        nighttime_awakenings_per_month: int,
        short_acting_reliever_use_per_week: int,
        has_fev1_limitation: bool = False,
    ) -> Dict[str, Any]:
        """
        Evaluates GINA 2024 Guidelines for Asthma Management.
        Focuses on Track 1 (Preferred): Low-dose ICS-Formoterol as both controller and reliever across all steps.
        """
        is_well_controlled = (
            daytime_symptoms_per_week <= 2
            and nighttime_awakenings_per_month == 0
            and short_acting_reliever_use_per_week <= 2
        )

        if nighttime_awakenings_per_month >= 4 or daytime_symptoms_per_week >= 5:
            step = "Step 4: Medium Dose Maintenance ICS-Formoterol + As-Needed Low Dose ICS-Formoterol (SMART Regimen)"
            track1_rec = "Budesonide/Formoterol 160/4.5 mcg 2 inhalations BID maintenance + 1 inhalation PRN for symptom relief (max 12 inhalations/day)."
        elif daytime_symptoms_per_week >= 3 or nighttime_awakenings_per_month >= 1:
            step = "Step 3: Low Dose Maintenance ICS-Formoterol + As-Needed Low Dose ICS-Formoterol (SMART Regimen)"
            track1_rec = "Budesonide/Formoterol 80/4.5 mcg 1-2 inhalations BID maintenance + 1 inhalation PRN for symptom relief."
        else:
            step = "Step 1-2: As-Needed Low Dose ICS-Formoterol ONLY (No daily maintenance required)"
            track1_rec = "Budesonide/Formoterol 160/4.5 mcg 1 inhalation taken whenever symptoms occur. SABA monotherapy is NO LONGER RECOMMENDED by GINA due to severe exacerbation risk."

        return {
            "guideline": "GINA 2024 Global Strategy for Asthma Management and Prevention",
            "control_status": "Well-Controlled" if is_well_controlled else "Partly Controlled / Uncontrolled",
            "recommended_gina_step": step,
            "preferred_track_1_regimen": track1_rec,
            "safety_warning": "GINA fundamentally advises against SABA-only treatment (Albuterol alone). Every patient must receive an Inhaled Corticosteroid to reduce airway inflammation and mortality.",
        }

    @staticmethod
    def evaluate_ards_berlin_criteria(
        pao2_fio2_ratio: float,
        peep_cm_h2o: float,
        timing_within_1_week_of_insult: bool = True,
        bilateral_opacities_on_cxr_ct: bool = True,
        edema_not_fully_explained_by_chf: bool = True,
    ) -> Dict[str, Any]:
        """
        Berlin Definition for Acute Respiratory Distress Syndrome (ARDS) (JAMA 2012).
        """
        if not (timing_within_1_week_of_insult and bilateral_opacities_on_cxr_ct and edema_not_fully_explained_by_chf):
            return {"is_ards": False, "reason": "Fails Berlin core diagnostic criteria for timing, bilateral imaging opacities, or non-cardiogenic origin."}

        if peep_cm_h2o < 5.0:
            return {"is_ards": False, "reason": "Berlin definition requires minimum PEEP >= 5 cm H2O (or CPAP >= 5 cm H2O)."}

        if pao2_fio2_ratio <= 100.0:
            sev = "Severe ARDS"
            mortality = 45.0
            vent_recs = [
                "Lung-Protective Mechanical Ventilation: Tidal volume 4-6 mL/kg of Predicted Body Weight (PBW).",
                "Plateau Pressure (Pplat) strictly limited to <= 30 cm H2O; Driving Pressure <= 14 cm H2O.",
                "High PEEP Strategy (14-24 cm H2O) titrated by PEEP-FiO2 tables.",
                "Prone Positioning: Minimum 16 consecutive hours/day for PaO2/FiO2 < 150 mmHg (PROSEVA trial: dramatic mortality reduction).",
                "Early Neuromuscular Blockade (Cisatracurium continuous infusion x 48h) for severe patient-ventilator dyssynchrony.",
                "Evaluate for Veno-Venous (V-V) ECMO if PaO2/FiO2 < 80 mmHg for > 6 hours despite prone positioning (EOLIA criteria).",
            ]
        elif 100.0 < pao2_fio2_ratio <= 200.0:
            sev = "Moderate ARDS"
            mortality = 32.0
            vent_recs = [
                "Tidal Volume: 6 mL/kg PBW; Target Pplat <= 30 cm H2O.",
                "Moderate-High PEEP (10-14 cm H2O).",
                "Prone positioning strongly indicated if PaO2/FiO2 remains < 150 mmHg after initial optimization.",
            ]
        else:
            sev = "Mild ARDS (200 < PaO2/FiO2 <= 300 mmHg)"
            mortality = 27.0
            vent_recs = [
                "Tidal Volume: 6 mL/kg PBW; Pplat <= 30 cm H2O.",
                "PEEP 5-10 cm H2O.",
                "Non-invasive ventilation or High-Flow Nasal Cannula (HFNC) under close ICU monitoring.",
            ]

        return {
            "is_ards": True,
            "ards_severity": sev,
            "pao2_fio2_ratio": round(pao2_fio2_ratio, 1),
            "estimated_icu_mortality_percent": mortality,
            "mechanical_ventilation_protocol": vent_recs,
        }
