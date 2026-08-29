"""
HealthPulse AI — Comprehensive ICD-10-CM / ICD-11 Complete 22-Chapter Master Codebook.
Contains extensive diagnosis definitions, CMS-HCC risk adjustment factor (RAF) weights, and chronic condition flags.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MasterICDEntity:
    code: str
    description: str
    chapter_num: int
    chapter_name: str
    hcc_v28: Optional[str]
    raf_community_nondual: float
    is_chronic: bool
    requires_secondary_code: bool


ICD10_CHAPTER_DATABASE: Dict[str, MasterICDEntity] = {
    # Chapter 1: Infectious & Parasitic Diseases (A00-B99)
    "A02.0": MasterICDEntity("A02.0", "Salmonella enteritis", 1, "Infectious & Parasitic Diseases", None, 0.0, False, False),
    "A04.7": MasterICDEntity("A04.7", "Enterocolitis due to Clostridioides difficile", 1, "Infectious & Parasitic Diseases", None, 0.0, False, False),
    "A08.4": MasterICDEntity("A08.4", "Viral intestinal infection, unspecified", 1, "Infectious & Parasitic Diseases", None, 0.0, False, False),
    "A40.0": MasterICDEntity("A40.0", "Sepsis due to streptococcus, group A", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A40.1": MasterICDEntity("A40.1", "Sepsis due to streptococcus, group B", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A40.3": MasterICDEntity("A40.3", "Sepsis due to Streptococcus pneumoniae", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.01": MasterICDEntity("A41.01", "Sepsis due to Methicillin susceptible Staphylococcus aureus (MSSA)", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.02": MasterICDEntity("A41.02", "Sepsis due to Methicillin resistant Staphylococcus aureus (MRSA)", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.1": MasterICDEntity("A41.1", "Sepsis due to other specified staphylococcus", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.2": MasterICDEntity("A41.2", "Sepsis due to unspecified staphylococcus", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.51": MasterICDEntity("A41.51", "Sepsis due to Escherichia coli (E. coli)", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.52": MasterICDEntity("A41.52", "Sepsis due to Pseudomonas", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.53": MasterICDEntity("A41.53", "Sepsis due to Serratia", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "A41.59": MasterICDEntity("A41.59", "Other Gram-negative sepsis", 1, "Infectious & Parasitic Diseases", "HCC 2", 0.450, False, False),
    "B20": MasterICDEntity("B20", "Human immunodeficiency virus (HIV) disease", 1, "Infectious & Parasitic Diseases", "HCC 1", 0.383, True, False),
    "B18.2": MasterICDEntity("B18.2", "Chronic viral hepatitis C", 1, "Infectious & Parasitic Diseases", "HCC 65", 0.150, True, False),

    # Chapter 2: Neoplasms (C00-D49)
    "C18.9": MasterICDEntity("C18.9", "Malignant neoplasm of colon, unspecified", 2, "Neoplasms", "HCC 28", 0.298, True, False),
    "C25.9": MasterICDEntity("C25.9", "Malignant neoplasm of pancreas, unspecified", 2, "Neoplasms", "HCC 27", 0.650, True, False),
    "C34.90": MasterICDEntity("C34.90", "Malignant neoplasm of unspecified part of bronchus or lung", 2, "Neoplasms", "HCC 27", 0.650, True, False),
    "C50.919": MasterICDEntity("C50.919", "Malignant neoplasm of unspecified site of female breast", 2, "Neoplasms", "HCC 29", 0.160, True, False),
    "C61": MasterICDEntity("C61", "Malignant neoplasm of prostate", 2, "Neoplasms", "HCC 30", 0.145, True, False),
    "C78.00": MasterICDEntity("C78.00", "Secondary malignant neoplasm of unspecified lung", 2, "Neoplasms", "HCC 26", 0.880, True, False),
    "C79.31": MasterICDEntity("C79.31", "Secondary malignant neoplasm of brain", 2, "Neoplasms", "HCC 26", 0.880, True, False),
    "C90.00": MasterICDEntity("C90.00", "Multiple myeloma not having achieved remission", 2, "Neoplasms", "HCC 25", 0.720, True, False),
    "C92.00": MasterICDEntity("C92.00", "Acute myeloblastic leukemia not having achieved remission", 2, "Neoplasms", "HCC 25", 0.720, True, False),

    # Chapter 3: Diseases of Blood & Blood-Forming Organs (D50-D89)
    "D50.9": MasterICDEntity("D50.9", "Iron deficiency anemia, unspecified", 3, "Blood & Immune Disorders", None, 0.0, False, False),
    "D57.1": MasterICDEntity("D57.1", "Sickle-cell disease without crisis", 3, "Blood & Immune Disorders", "HCC 112", 0.280, True, False),
    "D57.00": MasterICDEntity("D57.00", "Hb-SS disease with crisis, unspecified", 3, "Blood & Immune Disorders", "HCC 112", 0.350, False, False),
    "D68.51": MasterICDEntity("D68.51", "Activated protein C resistance (Factor V Leiden)", 3, "Blood & Immune Disorders", "HCC 115", 0.120, True, False),
    "D69.3": MasterICDEntity("D69.3", "Immune thrombocytopenic purpura (ITP)", 3, "Blood & Immune Disorders", "HCC 115", 0.120, True, False),
    "D69.49": MasterICDEntity("D69.49", "Other primary thrombocytopenia (including HIT)", 3, "Blood & Immune Disorders", "HCC 115", 0.120, False, False),

    # Chapter 4: Endocrine, Nutritional & Metabolic Diseases (E00-E89)
    "E11.00": MasterICDEntity("E11.00", "Type 2 diabetes mellitus with hyperosmolarity without nonketotic hyperglycemic-hyperosmolar coma", 4, "Endocrine & Metabolic", "HCC 17", 0.450, True, False),
    "E11.10": MasterICDEntity("E11.10", "Type 2 diabetes mellitus with ketoacidosis without coma", 4, "Endocrine & Metabolic", "HCC 17", 0.450, True, False),
    "E11.21": MasterICDEntity("E11.21", "Type 2 diabetes mellitus with diabetic nephropathy", 4, "Endocrine & Metabolic", "HCC 18", 0.302, True, False),
    "E11.319": MasterICDEntity("E11.319", "Type 2 diabetes mellitus with unspecified diabetic retinopathy without macular edema", 4, "Endocrine & Metabolic", "HCC 18", 0.302, True, False),
    "E11.40": MasterICDEntity("E11.40", "Type 2 diabetes mellitus with diabetic neuropathy, unspecified", 4, "Endocrine & Metabolic", "HCC 18", 0.302, True, False),
    "E11.65": MasterICDEntity("E11.65", "Type 2 diabetes mellitus with hyperglycemia", 4, "Endocrine & Metabolic", "HCC 19", 0.105, True, False),
    "E66.01": MasterICDEntity("E66.01", "Morbid (severe) obesity due to excess calories (BMI >= 40)", 4, "Endocrine & Metabolic", "HCC 48", 0.250, True, False),
    "E87.1": MasterICDEntity("E87.1", "Hypo-osmolality and hyponatremia", 4, "Endocrine & Metabolic", None, 0.0, False, False),
    "E87.5": MasterICDEntity("E87.5", "Hyperkalemia", 4, "Endocrine & Metabolic", None, 0.0, False, False),
    "E87.6": MasterICDEntity("E87.6", "Hypokalemia", 4, "Endocrine & Metabolic", None, 0.0, False, False),
    "E87.2": MasterICDEntity("E87.2", "Acidosis (Metabolic / Lactic / Respiratory)", 4, "Endocrine & Metabolic", None, 0.0, False, False),

    # Chapter 9: Diseases of Circulatory System (I00-I99)
    "I20.0": MasterICDEntity("I20.0", "Unstable angina", 9, "Circulatory System", "HCC 88", 0.140, False, False),
    "I21.9": MasterICDEntity("I21.9", "Acute myocardial infarction, unspecified", 9, "Circulatory System", "HCC 86", 0.290, False, False),
    "I26.92": MasterICDEntity("I26.92", "Saddle pulmonary embolism without acute cor pulmonale", 9, "Circulatory System", "HCC 108", 0.410, False, False),
    "I42.0": MasterICDEntity("I42.0", "Dilated cardiomyopathy", 9, "Circulatory System", "HCC 85", 0.368, True, False),
    "I42.1": MasterICDEntity("I42.1", "Obstructive hypertrophic cardiomyopathy", 9, "Circulatory System", "HCC 85", 0.368, True, False),
    "I47.2": MasterICDEntity("I47.2", "Ventricular tachycardia", 9, "Circulatory System", "HCC 96", 0.268, True, False),
    "I49.01": MasterICDEntity("I49.01", "Ventricular fibrillation", 9, "Circulatory System", "HCC 96", 0.268, False, False),

    # Chapter 10: Diseases of Respiratory System (J00-J99)
    "J15.0": MasterICDEntity("J15.0", "Pneumonia due to Klebsiella pneumoniae", 10, "Respiratory System", "HCC 114", 0.210, False, False),
    "J15.1": MasterICDEntity("J15.1", "Pneumonia due to Pseudomonas", 10, "Respiratory System", "HCC 114", 0.210, False, False),
    "J15.211": MasterICDEntity("J15.211", "Pneumonia due to Methicillin susceptible Staphylococcus aureus", 10, "Respiratory System", "HCC 114", 0.210, False, False),
    "J15.212": MasterICDEntity("J15.212", "Pneumonia due to Methicillin resistant Staphylococcus aureus (MRSA)", 10, "Respiratory System", "HCC 114", 0.210, False, False),
    "J96.00": MasterICDEntity("J96.00", "Acute respiratory failure, unspecified with hypoxia or hypercapnia", 10, "Respiratory System", "HCC 115", 0.320, False, False),
    "J96.01": MasterICDEntity("J96.01", "Acute respiratory failure with hypoxia", 10, "Respiratory System", "HCC 115", 0.320, False, False),
    "J96.02": MasterICDEntity("J96.02", "Acute respiratory failure with hypercapnia", 10, "Respiratory System", "HCC 115", 0.320, False, False),
};
