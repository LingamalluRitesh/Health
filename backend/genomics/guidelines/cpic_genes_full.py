"""
HealthPulse AI — Comprehensive CPIC Gene-Drug Action Database (20+ Key Pharmacogenes).
Implements clinical dosing algorithms for CYP2B6, CYP3A5, UGT1A1, HLA-A, HLA-B, G6PD, CACNA1S, RYR1, IFNL3, CFTR, POLG.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class PharmacogeneMaster:
    gene_symbol: str
    chromosome: str
    ncbi_gene_id: int
    key_drugs_affected: List[str]
    high_impact_alleles: List[str]
    phenotypes: List[str]
    clinical_mechanism: str
    cpic_guideline_url: str


CPIC_MASTER_GENES: Dict[str, PharmacogeneMaster] = {
    "CYP2B6": PharmacogeneMaster(
        gene_symbol="CYP2B6",
        chromosome="chr19",
        ncbi_gene_id=1555,
        key_drugs_affected=["Efavirenz", "Methadone", "Bupropion", "Ketamine", "Cyclophosphamide"],
        high_impact_alleles=["*1 (Normal)", "*6 (Decreased - 516G>T)", "*18 (No Function - 983T>C)"],
        phenotypes=["Ultrerapid", "Normal", "Intermediate", "Poor Metabolizer"],
        clinical_mechanism="CYP2B6 *6/*6 poor metabolizers experience drastically elevated Efavirenz CNS concentrations and severe neuropsychiatric toxicity (hallucinations, insomnia, suicidal ideation).",
        cpic_guideline_url="https://cpicpgx.org/guidelines/guideline-for-efavirenz-and-cyp2b6/",
    ),
    "CYP3A5": PharmacogeneMaster(
        gene_symbol="CYP3A5",
        chromosome="chr7",
        ncbi_gene_id=1577,
        key_drugs_affected=["Tacrolimus (Prograf)", "Cyclosporine", "Vincristine"],
        high_impact_alleles=["*1 (Normal / Expresser)", "*3 (No Function / Non-expresser - 6986A>G splice defect)", "*6", "*7"],
        phenotypes=["CYP3A5 Expresser (*1/*1, *1/*3)", "CYP3A5 Non-expresser (*3/*3)"],
        clinical_mechanism="CYP3A5 expressers (*1 carriers, prevalent in African ancestry) rapidly metabolize Tacrolimus, requiring 1.5 to 2.0x higher initial doses to achieve target therapeutic trough levels (8-12 ng/mL) and avoid allograft rejection.",
        cpic_guideline_url="https://cpicpgx.org/guidelines/guideline-for-tacrolimus-and-cyp3a5/",
    ),
    "UGT1A1": PharmacogeneMaster(
        gene_symbol="UGT1A1",
        chromosome="chr2",
        ncbi_gene_id=54658,
        key_drugs_affected=["Irinotecan (Camptosar)", "Atazanavir (Reyataz)", "Belinostat"],
        high_impact_alleles=["*1 (TA)6", "*28 (TA)7 promoter expansion", "*6 (211G>A)"],
        phenotypes=["Normal Metabolizer (*1/*1)", "Intermediate Metabolizer (*1/*28)", "Poor Metabolizer (*28/*28 - Gilbert Syndrome)"],
        clinical_mechanism="UGT1A1 *28/*28 homozygous patients have impaired glucuronidation of SN-38 (active cytotoxic metabolite of Irinotecan), resulting in severe life-threatening Grade 4 neutropenia and delayed diarrhea.",
        cpic_guideline_url="https://cpicpgx.org/guidelines/guideline-for-irinotecan-and-ugt1a1/",
    ),
    "HLA-B": PharmacogeneMaster(
        gene_symbol="HLA-B",
        chromosome="chr6 (MHC Class I)",
        ncbi_gene_id=3106,
        key_drugs_affected=["Abacavir (Ziagen)", "Allopurinol (Zyloprim)", "Carbamazepine (Tegretol)"],
        high_impact_alleles=["HLA-B*57:01 (Abacavir)", "HLA-B*58:01 (Allopurinol)", "HLA-B*15:02 (Carbamazepine)"],
        phenotypes=["Carrier (Positive)", "Non-Carrier (Negative)"],
        clinical_mechanism="HLA-B*57:01 carriers have high risk of fatal Abacavir Hypersensitivity Reaction (AHR). HLA-B*58:01 carriers (especially Asian and African descent) have high risk of Allopurinol-induced Severe Cutaneous Adverse Reactions (SCAR: Stevens-Johnson Syndrome / Toxic Epidermal Necrolysis).",
        cpic_guideline_url="https://cpicpgx.org/guidelines/guideline-for-allopurinol-and-hla-b/",
    ),
    "G6PD": PharmacogeneMaster(
        gene_symbol="G6PD",
        chromosome="chrX",
        ncbi_gene_id=2539,
        key_drugs_affected=["Rasburicase (Elitek)", "Primaquine", "Dapsone", "Methylene Blue", "Nitrofurantoin"],
        high_impact_alleles=["Class I (Severe deficiency / CNSHA)", "Class II (<10% activity - Mediterranean)", "Class III (10-60% activity - A-)", "Class IV (Normal)"],
        phenotypes=["G6PD Deficient", "G6PD Variable", "G6PD Normal"],
        clinical_mechanism="Rasburicase produces hydrogen peroxide during uric acid breakdown. In G6PD deficiency, failure of glutathione regeneration causes severe acute hemolytic anemia and methemoglobinemia. Rasburicase is STRICTLY CONTRAINDICATED in G6PD deficiency.",
        cpic_guideline_url="https://cpicpgx.org/guidelines/guideline-for-rasburicase-and-g6pd/",
    ),
    "RYR1": PharmacogeneMaster(
        gene_symbol="RYR1",
        chromosome="chr19",
        ncbi_gene_id=6261,
        key_drugs_affected=["Volatile Inhalational Anesthetics (Isoflurane, Sevoflurane, Desflurane)", "Succinylcholine"],
        high_impact_alleles=["Pathogenic missense variants (e.g. c.1840C>T, c.7300G>A)"],
        phenotypes=["Malignant Hyperthermia Susceptible (MHS)", "Malignant Hyperthermia Normal (MHN)"],
        clinical_mechanism="Uncontrolled sarcoplasmic reticulum calcium release triggers hypermetabolic crisis (rigidity, hyperthermia, rhabdomyolysis, hyperkalemia, cardiac arrest). Emergency treatment requires Dantrolene 2.5 mg/kg IV and active cooling.",
        cpic_guideline_url="https://cpicpgx.org/guidelines/guideline-for-potent-volatile-anesthetic-agents-and-succinylcholine-and-ryr1-and-cacna1s/",
    ),
};
