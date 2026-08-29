"""
HealthPulse AI — Comprehensive CPT (Current Procedural Terminology) Clinical Procedure Master File.
Maps procedural codes, work relative value units (wRVUs), global surgery periods, and clinical descriptions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CPTProcedureEntry:
    code: str
    description: str
    section: str
    work_rvu: float
    total_nonfacility_rvu: float
    global_period_days: str
    is_major_surgery: bool


CPT_PROCEDURE_CATALOG: Dict[str, CPTProcedureEntry] = {
    # Evaluation & Management (E/M)
    "99281": CPTProcedureEntry("99281", "Emergency department visit, straightforward medical decision making", "E/M", 0.48, 0.72, "XXX", False),
    "99282": CPTProcedureEntry("99282", "Emergency department visit, low complexity medical decision making", "E/M", 0.93, 1.45, "XXX", False),
    "99283": CPTProcedureEntry("99283", "Emergency department visit, moderate complexity medical decision making", "E/M", 1.60, 2.38, "XXX", False),
    "99284": CPTProcedureEntry("99284", "Emergency department visit, high complexity medical decision making", "E/M", 2.74, 3.82, "XXX", False),
    "99285": CPTProcedureEntry("99285", "Emergency department visit, high complexity with imminent life threat", "E/M", 4.00, 5.56, "XXX", False),
    "99291": CPTProcedureEntry("99291", "Critical care, evaluation and management of the critically ill patient; first 30-74 minutes", "E/M", 4.86, 6.78, "XXX", False),
    "99292": CPTProcedureEntry("99292", "Critical care, each additional 30 minutes", "E/M", 2.40, 3.35, "XXX", False),
    "99221": CPTProcedureEntry("99221", "Initial hospital inpatient care, low complexity", "E/M", 1.92, 2.85, "XXX", False),
    "99222": CPTProcedureEntry("99222", "Initial hospital inpatient care, moderate complexity", "E/M", 2.61, 3.90, "XXX", False),
    "99223": CPTProcedureEntry("99223", "Initial hospital inpatient care, high complexity", "E/M", 3.86, 5.75, "XXX", False),

    # Cardiovascular Procedures & Interventions
    "92928": CPTProcedureEntry("92928", "Percutaneous transcatheter placement of intracoronary stent(s), with coronary angioplasty; single major coronary artery", "Surgery", 10.82, 17.50, "000", True),
    "92941": CPTProcedureEntry("92941", "Percutaneous transcatheter revascularization of acute total/subtotal occlusion during acute myocardial infarction (STEMI)", "Surgery", 13.54, 21.80, "000", True),
    "93458": CPTProcedureEntry("93458", "Left heart catheterization including intraprocedural coronary angiography and left ventriculography", "Surgery", 5.25, 8.90, "000", False),
    "93306": CPTProcedureEntry("93306", "Echocardiography, transthoracic, real-time with image documentation (2D), includes M-mode and Doppler", "Medicine", 1.30, 4.85, "XXX", False),
    "33533": CPTProcedureEntry("33533", "Coronary artery bypass graft (CABG), using single arterial graft", "Surgery", 33.40, 52.10, "090", True),
    "33361": CPTProcedureEntry("33361", "Transcatheter aortic valve replacement (TAVR/TAVI) with prosthetic valve; percutaneous femoral approach", "Surgery", 19.50, 31.20, "000", True),

    # Pulmonary & Critical Care Procedures
    "31500": CPTProcedureEntry("31500", "Emergency endotracheal intubation, airway procedure", "Surgery", 3.00, 4.25, "000", False),
    "31622": CPTProcedureEntry("31622", "Diagnostic flexible fiberoptic bronchoscopy", "Surgery", 2.78, 4.10, "000", False),
    "32551": CPTProcedureEntry("32551", "Tube thoracostomy, includes water seal (chest tube insertion)", "Surgery", 3.65, 5.40, "000", False),
    "32555": CPTProcedureEntry("32555", "Thoracentesis, needle or catheter, aspiration of pleural space; with imaging guidance", "Surgery", 1.85, 3.20, "000", False),
    "36556": CPTProcedureEntry("36556", "Insertion of non-tunneled central venous catheter (CVC); age 5 years or older", "Surgery", 2.25, 3.75, "000", False),
    "36620": CPTProcedureEntry("36620", "Arterial catheterization or cannulation for sampling, monitoring or transfusion (arterial line)", "Surgery", 1.15, 1.85, "000", False),

    # Gastrointestinal & Surgical Procedures
    "43239": CPTProcedureEntry("43239", "Esophagogastroduodenoscopy (EGD), flexible, transoral; with biopsy, single or multiple", "Surgery", 3.12, 5.80, "000", False),
    "43246": CPTProcedureEntry("43246", "Upper gastrointestinal endoscopy with directed placement of percutaneous gastrostomy (PEG) tube", "Surgery", 4.35, 7.10, "000", False),
    "45380": CPTProcedureEntry("45380", "Colonoscopy, flexible; with biopsy, single or multiple", "Surgery", 3.70, 6.95, "000", False),
    "47562": CPTProcedureEntry("47562", "Laparoscopic cholecystectomy", "Surgery", 10.95, 17.20, "090", True),
    "44970": CPTProcedureEntry("44970", "Laparoscopic appendectomy", "Surgery", 9.15, 14.80, "090", True),
    "49000": CPTProcedureEntry("49000", "Exploratory laparotomy, exploratory celiotomy with or without biopsy", "Surgery", 14.50, 22.80, "090", True),
};
