"""
HealthPulse AI — SNOMED CT Clinical Findings, Observations & Pathophysiological Signs.
Contains standardized SNOMED codes mapped to emergency medicine, critical care, and primary care findings.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SNOMEDFindingEntry:
    concept_id: str
    preferred_term: str
    semantic_tag: str
    organ_system: str
    is_critical_alarm: bool
    clinical_pearl: str


SNOMED_FINDINGS_DATABASE: Dict[str, SNOMEDFindingEntry] = {
    # Critical Care & Hemodynamic Signs
    "3424008": SNOMEDFindingEntry("3424008", "Tachycardia", "finding", "Cardiovascular", True, "Heart rate > 100 bpm; initial physiological compensation for shock or fever."),
    "48867003": SNOMEDFindingEntry("48867003", "Bradycardia", "finding", "Cardiovascular", True, "Heart rate < 60 bpm; screen for AV block, hyperkalemia, or elevated ICP (Cushing reflex)."),
    "45007003": SNOMEDFindingEntry("45007003", "Hypotension", "finding", "Cardiovascular", True, "Systolic BP < 90 mmHg or MAP < 65 mmHg; hallmark of circulatory shock."),
    "38341003": SNOMEDFindingEntry("38341003", "Hypertension", "finding", "Cardiovascular", False, "Blood pressure >= 130/80 mmHg."),
    "248587009": SNOMEDFindingEntry("248587009", "Prolonged capillary refill", "finding", "Cardiovascular", True, "Capillary refill time > 3 seconds; sensitive marker of tissue hypoperfusion."),
    "422400008": SNOMEDFindingEntry("422400008", "Disturbed consciousness (Altered Mental Status)", "finding", "Neurological", True, "GCS < 15 or acute delirium; cardinal sign of cerebral hypoperfusion/sepsis."),
    "271825005": SNOMEDFindingEntry("271825005", "Respiratory arrest", "finding", "Respiratory", True, "Immediate bag-valve-mask ventilation and endotracheal intubation required."),
    "431314004": SNOMEDFindingEntry("431314004", "Hypoxemia", "finding", "Respiratory", True, "PaO2 < 60 mmHg or SpO2 < 90%; mandates supplemental oxygen therapy."),
    "52448006": SNOMEDFindingEntry("52448006", "Cyanosis", "finding", "Respiratory", True, "Bluish discoloration of skin indicating deoxygenated hemoglobin >= 5 g/dL."),
    "248626009": SNOMEDFindingEntry("248626009", "Stridor", "finding", "Respiratory", True, "High-pitched inspiratory sound indicating impending upper airway obstruction."),
    "128601007": SNOMEDFindingEntry("128601007", "Crackles (Rales)", "finding", "Respiratory", False, "Discontinuous adventitious breath sounds from alveolar fluid or fibrosis."),
    "247410004": SNOMEDFindingEntry("247410004", "Wheeze", "finding", "Respiratory", False, "Continuous musical sound caused by bronchoconstriction / airflow limitation."),
    "28905009": SNOMEDFindingEntry("28905009", "Jugular venous distension (JVD)", "finding", "Cardiovascular", False, "Elevation of internal jugular venous pressure > 3-4 cm above sternal angle."),
    "271795006": SNOMEDFindingEntry("271795006", "Pitting edema of lower extremity", "finding", "Cardiovascular", False, "Peripheral interstitial fluid expansion in congestive heart failure or cirrhosis."),
    "3006004": SNOMEDFindingEntry("3006004", "Ascites", "finding", "Gastroenterology", False, "Pathological fluid accumulation in peritoneal cavity with positive shifting dullness."),
    "18165001": SNOMEDFindingEntry("18165001", "Jaundice (Icterus)", "finding", "Hepatology", False, "Yellowish pigmentation of sclerae and skin when total bilirubin > 2.5-3.0 mg/dL."),
    "248234008": SNOMEDFindingEntry("248234008", "Asterixis (Flapping tremor)", "finding", "Neurological", True, "Negative myoclonus characteristic of hepatic encephalopathy or severe uremia."),
    "29857009": SNOMEDFindingEntry("29857009", "Precordial chest pain", "finding", "Cardiovascular", True, "Substernal pressure radiating to left arm/jaw; assess with TIMI / HEART scores."),
    "267036007": SNOMEDFindingEntry("267036007", "Dyspnea on exertion", "finding", "Respiratory", False, "Shortness of breath out of proportion to physical exertion."),
    "386661006": SNOMEDFindingEntry("386661006", "Pyrexia (Fever)", "finding", "General", False, "Core body temperature >= 38.0 C (100.4 F)."),
    "386689009": SNOMEDFindingEntry("386689009", "Hypothermia", "finding", "General", True, "Core body temperature < 35.0 C (95.0 F); adverse prognostic marker in sepsis."),
    "48447003": SNOMEDFindingEntry("48447003", "Anuria", "finding", "Renal", True, "Urine output < 50-100 mL in 24 hours; acute renal cortical necrosis or complete obstruction."),
    "28651003": SNOMEDFindingEntry("28651003", "Oliguria", "finding", "Renal", True, "Urine output < 0.5 mL/kg/hour for > 6 hours; hallmark of AKI / shock."),
    "274780009": SNOMEDFindingEntry("274780009", "Proteinuria", "finding", "Renal", False, "Elevated urinary protein excretion > 150 mg/day or uACR > 30 mg/g."),
    "83884004": SNOMEDFindingEntry("83884004", "Hematuria", "finding", "Renal", False, ">= 3 RBCs per high-power field on microscopic urine examination."),
};
