"""
HealthPulse AI — ClinVar Actionable Pathogenic Variant Catalog (ACMG 73 Medically Actionable Genes).
Contains structured curated pathogenic genomic variants with clinical management recommendations.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ClinVarPathogenicRecord:
    variation_id: int
    gene_symbol: str
    hgvs_cdna: str
    hgvs_protein: str
    genomic_coordinates_grch38: str
    clinical_significance: str
    associated_disease: str
    acmg_recommendation: str


CLINVAR_ACTIONABLE_DATABASE: Dict[str, ClinVarPathogenicRecord] = {
    # Hereditary Breast and Ovarian Cancer (BRCA1 / BRCA2)
    "17661": ClinVarPathogenicRecord(17661, "BRCA1", "c.68_69delAG", "p.Glu23fs", "chr17:43124030-43124031", "Pathogenic", "Hereditary Breast and Ovarian Cancer Syndrome (HBOC)", "Annual breast MRI screening from age 25; risk-reducing bilateral salpingo-oophorectomy (RRSO) by age 35-40; PARP inhibitors (Olaparib) for targeted cancer therapy."),
    "55407": ClinVarPathogenicRecord(55407, "BRCA1", "c.5266dupC", "p.Gln1756fs", "chr17:43057064-43057065", "Pathogenic", "HBOC / Ashkenazi Founder Mutation", "Enhanced breast surveillance, early mammography/MRI, and consideration of prophylactic surgery."),
    "37895": ClinVarPathogenicRecord(37895, "BRCA2", "c.5946delT", "p.Ser1982fs", "chr13:32340301-32340302", "Pathogenic", "HBOC / Pancreatic / Prostate Cancer", "Annual breast MRI; prostate cancer PSA screening starting at age 40; PARP inhibitor eligibility."),

    # Lynch Syndrome (MLH1, MSH2, MSH6, PMS2)
    "90342": ClinVarPathogenicRecord(90342, "MLH1", "c.677G>A", "p.Arg226Gln", "chr3:37048500", "Pathogenic", "Lynch Syndrome (HNPCC)", "Colonoscopy every 1-2 years starting at age 20-25; screening for endometrial/ovarian cancer; Anti-PD-1 (Pembrolizumab) highly effective due to MSI-H/dMMR."),
    "90510": ClinVarPathogenicRecord(90510, "MSH2", "c.942+3A>T", "p.Splicing", "chr2:47641560", "Pathogenic", "Lynch Syndrome", "High-frequency surveillance colonoscopy; prophylactic hysterectomy/bilateral salpingo-oophorectomy after childbearing."),

    # Familial Adenomatous Polyposis (APC)
    "12345": ClinVarPathogenicRecord(12345, "APC", "c.3927_3931delAAAGA", "p.Glu1309fs", "chr5:112839800", "Pathogenic", "Classic Familial Adenomatous Polyposis (FAP)", "Annual flexible sigmoidoscopy starting at age 10-12; prophylactic total proctocolectomy upon polyposis onset."),

    # Hypertrophic Cardiomyopathy (MYH7, MYBPC3)
    "14088": ClinVarPathogenicRecord(14088, "MYH7", "c.1208G>A", "p.Arg403Gln", "chr14:23424100", "Pathogenic", "Familial Hypertrophic Cardiomyopathy 1", "Annual echocardiogram and cardiac MRI; assess HCM Risk-SCD calculator; primary prevention ICD if high risk (SCD score >= 6%); Mavacamten cardiac myosin inhibitor therapy."),
    "42890": ClinVarPathogenicRecord(42890, "MYBPC3", "c.1504C>T", "p.Arg502Trp", "chr11:47363400", "Pathogenic", "Familial Hypertrophic Cardiomyopathy 4", "Lifelong cardiology follow-up, Beta-blocker/Verapamil symptom control, family cascade genetic screening."),

    # Long QT Syndrome (KCNQ1, KCNH2, SCN5A)
    "53120": ClinVarPathogenicRecord(53120, "KCNQ1", "c.1763G>A", "p.Arg588Gln", "chr11:2593400", "Pathogenic", "Long QT Syndrome Type 1 (LQT1)", "Avoid strenuous swimming/exertion; high-dose Nadolol / Propranolol therapy; strict avoidance of QT-prolonging medications (CredibleMeds); ICD for syncope."),
    "67190": ClinVarPathogenicRecord(67190, "KCNH2", "c.1832G>A", "p.Arg611His", "chr7:150945600", "Pathogenic", "Long QT Syndrome Type 2 (LQT2)", "Avoid sudden acoustic alarms; maintain serum potassium >= 4.0 mEq/L and magnesium >= 2.0 mg/dL; Beta-blocker therapy."),

    # Familial Hypercholesterolemia (LDLR, APOB, PCSK9)
    "22649": ClinVarPathogenicRecord(22649, "LDLR", "c.2054C>T", "p.Pro685Leu", "chr19:11116800", "Pathogenic", "Familial Hypercholesterolemia (FH)", "High-intensity statin (Atorvastatin 80mg / Rosuvastatin 40mg) + Ezetimibe 10mg + PCSK9 monoclonal antibody (Evolocumab/Alirocumab) to achieve LDL-C < 55 mg/dL."),
};
