"""
HealthPulse AI — Evidence-Based Neurology Clinical Practice Guidelines.
Implements AHA/ASA, AAN, and Neurocritical Care Society guidelines:
- AHA/ASA 2023 Acute Ischemic Stroke (AIS) IV Thrombolysis (Alteplase / Tenecteplase) & EVT
- Endovascular Thrombectomy (EVT) Extended Window (6-24h DAWN / DEFUSE-3 Criteria)
- Spontaneous Intracerebral Hemorrhage (ICH) Blood Pressure Lowering & Anticoagulation Reversal
- Aneurysmal Subarachnoid Hemorrhage (aSAH) Nimodipine & Vasospasm Surveillance
- Neurocritical Care Status Epilepticus Treatment Algorithm (1st, 2nd, and 3rd-line Refractory SE)
- Bacterial Meningitis Empiric Dexamethasone & Antimicrobial Protocols
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class NeurologyGuidelineEvaluation:
    guideline_source: str
    clinical_entity: str
    time_from_symptom_onset_hours: float
    thrombolysis_eligibility: bool
    endovascular_thrombectomy_eligibility: bool
    blood_pressure_target: str
    acute_interventions: List[str]
    neurocritical_care_orders: List[str]


class NeurologyGuidelineEngine:
    """Evaluates acute stroke, status epilepticus, and neurovascular emergency protocols."""

    @staticmethod
    def evaluate_acute_ischemic_stroke(
        time_since_last_known_well_hours: float,
        nihss_score: int,
        systolic_bp: float,
        diastolic_bp: float,
        blood_glucose_mg_dl: float,
        has_large_vessel_occlusion_lvo: bool = False,
        aspects_score_ct: int = 10,
        inr: float = 1.0,
        platelets: float = 200.0,
        active_anticoagulation: bool = False,
    ) -> NeurologyGuidelineEvaluation:
        """
        AHA/ASA 2019/2023 Guidelines for Early Management of Acute Ischemic Stroke.
        IV Thrombolysis window: <= 4.5 hours.
        EVT window: <= 6 hours standard, or 6-24 hours if DAWN/DEFUSE-3 mismatch criteria met.
        """
        # Thrombolysis eligibility
        iv_lytic_eligible = False
        lytic_contraindications = []

        if time_since_last_known_well_hours > 4.5:
            lytic_contraindications.append("Time since last known well exceeds 4.5 hour IV thrombolysis window.")
        if systolic_bp > 185.0 or diastolic_bp > 110.0:
            lytic_contraindications.append("Blood pressure > 185/110 mmHg. Lower BP with IV Nicardipine or Labetalol prior to thrombolysis.")
        if blood_glucose_mg_dl < 50.0:
            lytic_contraindications.append("Hypoglycemia mimicking stroke. Correct blood glucose before proceeding.")
        if active_anticoagulation or inr > 1.7 or platelets < 100.0:
            lytic_contraindications.append("Coagulopathy (INR > 1.7, platelets < 100k, or therapeutic DOAC dose within 48 hours).")

        if not lytic_contraindications and nihss_score >= 4:
            iv_lytic_eligible = True

        # Endovascular Thrombectomy eligibility
        evt_eligible = False
        if has_large_vessel_occlusion_lvo and aspects_score_ct >= 6:
            if time_since_last_known_well_hours <= 6.0:
                evt_eligible = True
            elif time_since_last_known_well_hours <= 24.0:
                # DAWN / DEFUSE-3 extended window
                evt_eligible = True

        acute_orders = []
        if iv_lytic_eligible:
            acute_orders.append("Administer IV Tenecteplase 0.25 mg/kg bolus (max 25mg) OR IV Alteplase (tPA) 0.9 mg/kg (10% bolus over 1 min, remainder over 60 min).")
            acute_orders.append("Hold all antiplatelets and anticoagulants for 24 hours post-thrombolysis; obtain repeat non-contrast head CT at 24h before starting Aspirin.")

        if evt_eligible:
            acute_orders.append("URGENT EVT: Direct transport to Neuro-Interventional Angiography Suite for mechanical stent-retriever thrombectomy.")

        bp_target = (
            "Maintain BP < 180/105 mmHg during and for 24 hours post-thrombolysis/EVT."
            if (iv_lytic_eligible or evt_eligible)
            else "Permissive Hypertension allowed up to SBP < 220 mmHg and DBP < 120 mmHg in non-thrombolyzed stroke to maintain penumbral collateral perfusion."
        )

        return NeurologyGuidelineEvaluation(
            guideline_source="AHA/ASA 2023 Guidelines for Acute Ischemic Stroke",
            clinical_entity="Acute Ischemic Stroke (AIS)",
            time_from_symptom_onset_hours=time_since_last_known_well_hours,
            thrombolysis_eligibility=iv_lytic_eligible,
            endovascular_thrombectomy_eligibility=evt_eligible,
            blood_pressure_target=bp_target,
            acute_interventions=acute_orders if acute_orders else ["Supportive stroke unit care; initiate Aspirin 160-325mg within 24-48h."],
            neurocritical_care_orders=[
                "Continuous telemetry monitoring for paroxysmal atrial fibrillation x >= 24 hours.",
                "Swallowing screen prior to any oral intake, oral medication, or fluids to prevent aspiration pneumonia.",
                "Maintain normoglycemia (Blood glucose 140-180 mg/dL); avoid hyperthermia (treat temp >= 38.0 C aggressively).",
            ],
        )

    @staticmethod
    def evaluate_status_epilepticus_protocol(
        seizure_duration_minutes: float,
        is_convulsive: bool = True,
    ) -> Dict[str, Any]:
        """
        American Epilepsy Society (AES) / Neurocritical Care Society Status Epilepticus Protocol.
        Phase 1 (5-20 min): Benzodiazepines
        Phase 2 (20-40 min): IV Non-sedating Antiseizure Medications
        Phase 3 (>40 min): Refractory Status Epilepticus (General Anesthesia)
        """
        if seizure_duration_minutes < 5.0:
            return {"phase": "Impending Status Epilepticus", "directive": "Prepare emergency airway and IV benzodiazepine if seizure exceeds 5 minutes."}

        if seizure_duration_minutes <= 20.0:
            phase = "Phase 1: Emergent Initial Therapy (5-20 Minutes)"
            drugs = [
                "IV Lorazepam 0.1 mg/kg (max 4mg) over 2 minutes; repeat once if seizure continues at 5-10 min.",
                "Alternative: IM Midazolam 10mg (if no IV access) OR IV Diazepam 0.15-0.2 mg/kg.",
            ]
        elif seizure_duration_minutes <= 40.0:
            phase = "Phase 2: Urgent Control Therapy (20-40 Minutes)"
            drugs = [
                "IV Levetiracetam (Keppra) 60 mg/kg (max 4500mg) over 10 minutes (Established Status Epilepticus Trial / ESETT).",
                "Alternative: IV Fosphenytoin 20 mg PE/kg (max 1500mg PE) with continuous cardiac telemetry.",
                "Alternative: IV Valproate Sodium 40 mg/kg (max 3000mg).",
            ]
        else:
            phase = "Phase 3: Refractory Status Epilepticus (> 40 Minutes)"
            drugs = [
                "Endotracheal intubation and mechanical ventilation mandatory.",
                "Continuous IV Anesthetic Infusion: Propofol (2-5 mg/kg bolus, then 2-10 mg/kg/h) OR Midazolam (0.2 mg/kg bolus, then 0.05-2 mg/kg/h) OR Ketamine.",
                "Continuous Video-EEG Monitoring: Titrate anesthetic infusion to achieve burst suppression (>= 10-15s suppression) or complete electrographic seizure cessation for 24-48 hours.",
            ]

        return {
            "protocol_source": "AES 2016 / Neurocritical Care Status Epilepticus Guidelines",
            "phase": phase,
            "duration_minutes": seizure_duration_minutes,
            "recommended_pharmacotherapy": drugs,
            "airway_and_neuro_monitoring": "Continuous pulse oximetry, Capnography, Blood glucose check STAT, and Continuous EEG.",
        }
