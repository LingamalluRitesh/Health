"""
HealthPulse AI — Comprehensive LOINC Laboratory Diagnostic Test Suite & Reference Matrix.
Contains structured LOINC test definitions across Hematology, Chemistry, Toxicology, Immunology, and Microbiology.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CompleteLOINCEntry:
    loinc_num: str
    component_name: str
    subspecialty_class: str
    specimen_type: str
    units_of_measure: str
    normal_low: Optional[float]
    normal_high: Optional[float]
    critical_low: Optional[float]
    critical_high: Optional[float]
    clinical_rationale: str


LOINC_FULL_DATABASE: Dict[str, CompleteLOINCEntry] = {
    # Hematology & Coagulation
    "5902-2": CompleteLOINCEntry("5902-2", "Prothrombin time (PT)", "COAG", "PPP", "s", 11.0, 13.5, None, 30.0, "Evaluates extrinsic and common coagulation pathways (Factors VII, X, V, II, I)."),
    "6301-6": CompleteLOINCEntry("6301-6", "INR in Platelet poor plasma by Coagulation assay", "COAG", "PPP", "{INR}", 0.8, 1.1, None, 5.0, "Standardized ratio for monitoring Vitamin K Antagonist (Warfarin) anticoagulation."),
    "3173-2": CompleteLOINCEntry("3173-2", "Activated partial thromboplastin time (aPTT)", "COAG", "PPP", "s", 25.0, 35.0, None, 100.0, "Monitors intrinsic coagulation pathway and unfractionated heparin therapy."),
    "3084-1": CompleteLOINCEntry("3084-1", "D-dimer FEU", "COAG", "PPP", "ug/mL", 0.0, 0.5, None, None, "Fibrin degradation fragment used in venous thromboembolism (DVT/PE) rule-out algorithms."),
    "2276-4": CompleteLOINCEntry("2276-4", "Ferritin", "HEM", "Ser/Plas", "ng/mL", 30.0, 400.0, 10.0, 1000.0, "Intracellular iron storage protein and positive acute-phase reactant."),
    "2498-4": CompleteLOINCEntry("2498-4", "Iron", "HEM", "Ser/Plas", "ug/dL", 60.0, 170.0, 20.0, 300.0, "Circulating transferrin-bound serum iron."),
    "2500-7": CompleteLOINCEntry("2500-7", "Iron binding capacity.total (TIBC)", "HEM", "Ser/Plas", "ug/dL", 240.0, 450.0, None, None, "Maximum amount of iron that can be bound by transferrin."),
    "2502-3": CompleteLOINCEntry("2502-3", "Iron saturation (Transferrin Saturation)", "HEM", "Ser/Plas", "%", 20.0, 50.0, 10.0, 70.0, "Ratio of serum iron to TIBC; <20% indicates iron deficiency, >45% suggests hemochromatosis."),

    # Comprehensive Chemistry & Hepatic Panel
    "1751-7": CompleteLOINCEntry("1751-7", "Albumin", "CHEM", "Ser/Plas", "g/dL", 3.5, 5.2, 1.5, 6.0, "Major serum oncotic protein synthesized by hepatocytes."),
    "2885-2": CompleteLOINCEntry("2885-2", "Protein.total", "CHEM", "Ser/Plas", "g/dL", 6.4, 8.3, 4.0, 10.0, "Total serum albumin and globulin fraction."),
    "1975-2": CompleteLOINCEntry("1975-2", "Bilirubin.total", "CHEM", "Ser/Plas", "mg/dL", 0.2, 1.2, None, 15.0, "Total unconjugated and conjugated bile pigment."),
    "1968-7": CompleteLOINCEntry("1968-7", "Bilirubin.direct (Conjugated)", "CHEM", "Ser/Plas", "mg/dL", 0.0, 0.3, None, 5.0, "Water-soluble glucuronidated bilirubin; elevated in biliary obstruction."),
    "1920-8": CompleteLOINCEntry("1920-8", "Aspartate aminotransferase (AST / SGOT)", "CHEM", "Ser/Plas", "U/L", 10.0, 40.0, None, 1000.0, "Mitochondrial and cytosolic enzyme released in hepatocellular or myocardial necrosis."),
    "1742-6": CompleteLOINCEntry("1742-6", "Alanine aminotransferase (ALT / SGPT)", "CHEM", "Ser/Plas", "U/L", 7.0, 56.0, None, 1000.0, "Specific cytosolic marker of hepatocellular membrane damage."),
    "6768-6": CompleteLOINCEntry("6768-6", "Alkaline phosphatase (ALP)", "CHEM", "Ser/Plas", "U/L", 44.0, 147.0, None, 500.0, "Biliary canalicular and osteoblastic bone isoenzyme."),
    "2324-2": CompleteLOINCEntry("2324-2", "Gamma glutamyl transferase (GGT)", "CHEM", "Ser/Plas", "U/L", 8.0, 61.0, None, 300.0, "Biliary enzyme used to distinguish hepatic from osseous alkaline phosphatase elevation."),
    "17861-6": CompleteLOINCEntry("17861-6", "Calcium.total", "CHEM", "Ser/Plas", "mg/dL", 8.5, 10.2, 6.0, 13.0, "Total serum calcium (bound and ionized). Correct for albumin."),
    "1994-3": CompleteLOINCEntry("1994-3", "Calcium.ionized", "CHEM", "BldA/Ser", "mmol/L", 1.15, 1.33, 0.80, 1.60, "Physiologically active free ionized calcium."),
    "2601-3": CompleteLOINCEntry("2601-3", "Magnesium", "CHEM", "Ser/Plas", "mg/dL", 1.7, 2.2, 1.0, 4.0, "Critical intracellular cation; cofactor for Na+/K+-ATPase and cardiac conduction."),
    "2777-1": CompleteLOINCEntry("2777-1", "Phosphate (Inorganic Phosphorus)", "CHEM", "Ser/Plas", "mg/dL", 2.5, 4.5, 1.0, 8.0, "Serum inorganic phosphorus; severely depleted in refeeding syndrome and DKA."),

    # Endocrine & Lipid Panel
    "3016-3": CompleteLOINCEntry("3016-3", "Thyrotropin (TSH)", "ENDO", "Ser/Plas", "uIU/mL", 0.45, 4.50, 0.01, 20.0, "Anterior pituitary hormone governing thyroid follicular synthesis."),
    "3024-7": CompleteLOINCEntry("3024-7", "Thyroxine.free (Free T4)", "ENDO", "Ser/Plas", "ng/dL", 0.82, 1.77, 0.30, 4.0, "Unbound active thyroid hormone."),
    "4548-4": CompleteLOINCEntry("4548-4", "Hemoglobin A1c/Hemoglobin.total in Blood", "ENDO", "Bld", "%", 4.0, 5.6, None, 14.0, "Glycated hemoglobin reflecting weighted 3-month mean plasma glucose."),
    "2093-3": CompleteLOINCEntry("2093-3", "Cholesterol in Serum or Plasma (Total)", "LIPID", "Ser/Plas", "mg/dL", 100.0, 199.0, None, 400.0, "Total circulating sterol molecules in all lipoprotein fractions."),
    "2085-9": CompleteLOINCEntry("2085-9", "HDL Cholesterol in Serum or Plasma", "LIPID", "Ser/Plas", "mg/dL", 40.0, 60.0, 15.0, None, "High-density lipoprotein mediating reverse cholesterol transport."),
    "13457-7": CompleteLOINCEntry("13457-7", "LDL Cholesterol calculated by Friedewald equation", "LIPID", "Ser/Plas", "mg/dL", 0.0, 99.0, None, 250.0, "Atherogenic low-density lipoprotein particles (Target < 70 or < 55 mg/dL in high risk CVD)."),
    "2571-8": CompleteLOINCEntry("2571-8", "Triglycerides in Serum or Plasma", "LIPID", "Ser/Plas", "mg/dL", 0.0, 149.0, None, 1000.0, "Neutral fats; levels > 500-1000 mg/dL trigger acute hypertriglyceridemic pancreatitis."),

    # Toxicology & Therapeutic Drug Monitoring (TDM)
    "3298-7": CompleteLOINCEntry("3298-7", "Acetaminophen in Serum or Plasma", "TOX", "Ser/Plas", "ug/mL", 0.0, 20.0, None, 150.0, "Serum paracetamol concentration evaluated on Rumack-Matthew nomogram."),
    "4024-6": CompleteLOINCEntry("4024-6", "Salicylate in Serum or Plasma", "TOX", "Ser/Plas", "mg/dL", 0.0, 20.0, None, 50.0, "Aspirin metabolite; levels > 40-50 mg/dL cause uncoupling of oxidative phosphorylation."),
    "3563-7": CompleteLOINCEntry("3563-7", "Ethanol in Blood", "TOX", "Bld", "mg/dL", 0.0, 0.0, None, 300.0, "Blood alcohol concentration (BAC). Legal intoxication threshold >= 80 mg/dL (0.08%)."),
    "3561-1": CompleteLOINCEntry("3561-1", "Digoxin in Serum or Plasma", "TDM", "Ser/Plas", "ng/mL", 0.5, 0.9, None, 2.0, "Cardiac glycoside trough level (Target 0.5-0.9 ng/mL for HFrEF)."),
    "4092-3": CompleteLOINCEntry("4092-3", "Vancomycin in Serum or Plasma (Trough)", "TDM", "Ser/Plas", "ug/mL", 10.0, 20.0, None, 25.0, "Glycopeptide antibiotic trough level (Target 15-20 ug/mL for severe MRSA)."),
    "3647-8": CompleteLOINCEntry("3647-8", "Gentamicin in Serum or Plasma (Peak)", "TDM", "Ser/Plas", "ug/mL", 5.0, 10.0, None, 12.0, "Aminoglycoside post-distribution peak concentration (synergistic bactericidal killing)."),
};
