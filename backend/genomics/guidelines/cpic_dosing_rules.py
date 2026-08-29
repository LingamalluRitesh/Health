"""
HealthPulse AI — CPIC Clinical Pharmacogenomics Dosing & Therapeutic Guideline Rules.
Implements level-A gene-drug interaction clinical rules for high-risk medications.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CPICDosingGuideline:
    gene: str
    drug: str
    phenotype: str
    therapeutic_recommendation: str
    classification_level: str
    alternative_agents: List[str]
    implication: str


CPIC_RULES_DATABASE: List[CPICDosingGuideline] = [
    # CYP2C19 & Clopidogrel
    CPICDosingGuideline(
        gene="CYP2C19",
        drug="Clopidogrel",
        phenotype="Poor Metabolizer (*2/*2, *2/*3, *3/*3)",
        therapeutic_recommendation="Avoid clopidogrel. Prescribe alternative antiplatelet agent (Prasugrel 10mg daily or Ticagrelor 90mg BID) at standard dosing if no contraindications.",
        classification_level="Level A (Strong)",
        alternative_agents=["Ticagrelor", "Prasugrel"],
        implication="Significantly reduced active metabolite levels, diminished platelet inhibition, and markedly increased risk of major adverse cardiovascular events (MACE) and stent thrombosis.",
    ),
    CPICDosingGuideline(
        gene="CYP2C19",
        drug="Clopidogrel",
        phenotype="Intermediate Metabolizer (*1/*2, *1/*3)",
        therapeutic_recommendation="Avoid clopidogrel in acute coronary syndrome (ACS) / PCI. Prescribe Prasugrel or Ticagrelor.",
        classification_level="Level A (Strong)",
        alternative_agents=["Ticagrelor", "Prasugrel"],
        implication="Suboptimal platelet inhibition with increased residual ischemic risk.",
    ),

    # CYP2D6 & Codeine / Tramadol
    CPICDosingGuideline(
        gene="CYP2D6",
        drug="Codeine",
        phenotype="Ultra-Rapid Metabolizer (*1/*1xN, *1/*2xN)",
        therapeutic_recommendation="Avoid codeine. High risk of morphine toxicity including fatal respiratory depression. Use non-opioid analgesics or non-CYP2D6 metabolized opioids (Morphine, Hydromorphone).",
        classification_level="Level A (Strong)",
        alternative_agents=["Morphine", "Hydromorphone", "Acetaminophen", "NSAIDs"],
        implication="Rapid conversion of codeine to morphine leads to potentially life-threatening opioid overdose symptoms at standard therapeutic doses.",
    ),
    CPICDosingGuideline(
        gene="CYP2D6",
        drug="Codeine",
        phenotype="Poor Metabolizer (*4/*4, *4/*5, *5/*5)",
        therapeutic_recommendation="Avoid codeine. Greatly reduced morphine formation leads to analgesic failure. Prescribe non-CYP2D6 metabolized opioids.",
        classification_level="Level A (Strong)",
        alternative_agents=["Morphine", "Hydromorphone", "Oxycodone (with monitoring)"],
        implication="Inadequate pain relief due to inability to bioactivate codeine prodrug to active morphine.",
    ),

    # DPYD & Fluoropyrimidines (5-FU, Capecitabine)
    CPICDosingGuideline(
        gene="DPYD",
        drug="Fluorouracil / Capecitabine",
        phenotype="Poor Metabolizer (Activity Score 0.0)",
        therapeutic_recommendation="STRICTLY AVOID 5-Fluorouracil, Capecitabine, and Tegafur. Severe, life-threatening, and fatal hematologic/GI toxicities occur. Select alternative non-fluoropyrimidine chemotherapy.",
        classification_level="Level A (Strong)",
        alternative_agents=["Irinotecan", "Oxaliplatin", "Targeted / Immunotherapy regimens"],
        implication="Complete deficiency of dihydropyrimidine dehydrogenase results in profound drug accumulation, severe mucositis, neutropenic sepsis, and fatal neurotoxicity.",
    ),
    CPICDosingGuideline(
        gene="DPYD",
        drug="Fluorouracil / Capecitabine",
        phenotype="Intermediate Metabolizer (Activity Score 1.0 - 1.5)",
        therapeutic_recommendation="Reduce starting dose by 50% for Activity Score 1.0 (or 25-50% for AS 1.5). Titrate dose based on therapeutic drug monitoring (TDM) and clinical tolerance.",
        classification_level="Level A (Strong)",
        alternative_agents=["Dose-reduced 5-FU/Capecitabine"],
        implication="Partial DPD deficiency increases risk of severe grade 3-4 chemotherapy toxicities.",
    ),

    # TPMT & NUDT15 with Thiopurines (Azathioprine, 6-MP)
    CPICDosingGuideline(
        gene="TPMT",
        drug="Azathioprine / 6-Mercaptopurine",
        phenotype="Poor Metabolizer (*3A/*3A, *2/*3A)",
        therapeutic_recommendation="For non-malignant conditions, choose non-thiopurine alternative. For malignancy, reduce starting dose by 90% (e.g. give 10% of normal dose) and dose 3 times per week instead of daily.",
        classification_level="Level A (Strong)",
        alternative_agents=["Methotrexate", "Biologics (Anti-TNF)", "Mycophenolate"],
        implication="Profound accumulation of cytotoxic thioguanine nucleotides (TGN) causing fatal pancytopenia and bone marrow suppression.",
    ),

    # SLCO1B1 & Simvastatin
    CPICDosingGuideline(
        gene="SLCO1B1",
        drug="Simvastatin",
        phenotype="Poor Function (*5/*5, rs4149056 CC genotype)",
        therapeutic_recommendation="Avoid Simvastatin 80mg or 40mg. Prescribe alternative statin with lower myopathy risk (Rosuvastatin, Pravastatin, or Pitavastatin).",
        classification_level="Level A (Strong)",
        alternative_agents=["Rosuvastatin", "Pravastatin", "Atorvastatin"],
        implication="Impaired hepatic OATP1B1 uptake leads to elevated systemic plasma concentrations of active simvastatin acid and high risk of statin-associated rhabdomyolysis.",
    ),
]


def find_cpic_guideline(gene: str, drug: str) -> Optional[CPICDosingGuideline]:
    """Finds matching CPIC guideline for given gene and drug pair."""
    for rule in CPIC_RULES_DATABASE:
        if rule.gene.upper() == gene.upper() and rule.drug.lower() in drug.lower():
            return rule
    return None
