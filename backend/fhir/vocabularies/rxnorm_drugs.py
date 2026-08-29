"""
HealthPulse AI — RxNorm Normalized Clinical Drug & Active Ingredient Dictionary.
Standardized medication terminologies and cross-references for EHR interoperability.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RxNormDrugEntity:
    rxcui: str
    name: str
    term_type: str  # IN (Ingredient), SCD (Semantic Clinical Drug), SBD (Semantic Branded Drug)
    dose_form: Optional[str]
    active_ingredients: List[str]
    brand_names: List[str]
    atc_class: str


RXNORM_DICTIONARY: Dict[str, RxNormDrugEntity] = {
    # Anticoagulants & Antiplatelets
    "11289": RxNormDrugEntity("11289", "Warfarin", "IN", None, ["Warfarin"], ["Coumadin", "Jantoven"], "B01AA03"),
    "855332": RxNormDrugEntity("855332", "Warfarin Sodium 5 MG Oral Tablet", "SCD", "Oral Tablet", ["Warfarin Sodium"], ["Coumadin 5 MG"], "B01AA03"),
    "32968": RxNormDrugEntity("32968", "Clopidogrel", "IN", None, ["Clopidogrel"], ["Plavix"], "B01AC04"),
    "309362": RxNormDrugEntity("309362", "Clopidogrel 75 MG Oral Tablet", "SCD", "Oral Tablet", ["Clopidogrel Bisulfate"], ["Plavix 75 MG"], "B01AC04"),
    "1364430": RxNormDrugEntity("1364430", "Apixaban", "IN", None, ["Apixaban"], ["Eliquis"], "B01AF02"),
    "1364435": RxNormDrugEntity("1364435", "Apixaban 5 MG Oral Tablet", "SCD", "Oral Tablet", ["Apixaban"], ["Eliquis 5 MG"], "B01AF02"),
    "1114195": RxNormDrugEntity("1114195", "Rivaroxaban", "IN", None, ["Rivaroxaban"], ["Xarelto"], "B01AF01"),
    "1114201": RxNormDrugEntity("1114201", "Rivaroxaban 20 MG Oral Tablet", "SCD", "Oral Tablet", ["Rivaroxaban"], ["Xarelto 20 MG"], "B01AF01"),
    "1191": RxNormDrugEntity("1191", "Aspirin", "IN", None, ["Aspirin"], ["Bayer Aspirin", "Ecotrin"], "B01AC06"),
    "243670": RxNormDrugEntity("243670", "Aspirin 81 MG Delayed Release Oral Tablet", "SCD", "Delayed Release Tablet", ["Aspirin"], ["Baby Aspirin"], "B01AC06"),

    # Cardiovascular & Antihypertensives
    "29046": RxNormDrugEntity("29046", "Lisinopril", "IN", None, ["Lisinopril"], ["Prinivil", "Zestril"], "C09AA03"),
    "314076": RxNormDrugEntity("314076", "Lisinopril 10 MG Oral Tablet", "SCD", "Oral Tablet", ["Lisinopril"], ["Zestril 10 MG"], "C09AA03"),
    "656659": RxNormDrugEntity("656659", "Losartan", "IN", None, ["Losartan"], ["Cozaar"], "C09CA01"),
    "6918": RxNormDrugEntity("6918", "Metoprolol", "IN", None, ["Metoprolol"], ["Lopressor", "Toprol-XL"], "C07AB02"),
    "866416": RxNormDrugEntity("866416", "Metoprolol Succinate 50 MG Extended Release Oral Tablet", "SCD", "Extended Release Tablet", ["Metoprolol Succinate"], ["Toprol-XL 50 MG"], "C07AB02"),
    "20352": RxNormDrugEntity("20352", "Carvedilol", "IN", None, ["Carvedilol"], ["Coreg"], "C07AG02"),
    "17767": RxNormDrugEntity("17767", "Amlodipine", "IN", None, ["Amlodipine"], ["Norvasc"], "C08CA01"),
    "4603": RxNormDrugEntity("4603", "Furosemide", "IN", None, ["Furosemide"], ["Lasix"], "C03CA01"),
    "9997": RxNormDrugEntity("9997", "Spironolactone", "IN", None, ["Spironolactone"], ["Aldactone"], "C03DA01"),
    "83367": RxNormDrugEntity("83367", "Atorvastatin", "IN", None, ["Atorvastatin"], ["Lipitor"], "C10AA05"),
    "259255": RxNormDrugEntity("259255", "Atorvastatin 40 MG Oral Tablet", "SCD", "Oral Tablet", ["Atorvastatin Calcium"], ["Lipitor 40 MG"], "C10AA05"),
    "1656328": RxNormDrugEntity("1656328", "Sacubitril / Valsartan", "IN", None, ["Sacubitril", "Valsartan"], ["Entresto"], "C09DX04"),

    # Antimicrobial Agents
    "11124": RxNormDrugEntity("11124", "Vancomycin", "IN", None, ["Vancomycin"], ["Vancocin"], "J01XA01"),
    "312444": RxNormDrugEntity("312444", "Piperacillin / Tazobactam", "IN", None, ["Piperacillin", "Tazobactam"], ["Zosyn"], "J01CR05"),
    "2231": RxNormDrugEntity("2231", "Cefepime", "IN", None, ["Cefepime"], ["Maxipime"], "J01DE01"),
    "2193": RxNormDrugEntity("2193", "Ceftriaxone", "IN", None, ["Ceftriaxone"], ["Rocephin"], "J01DD04"),
    "6845": RxNormDrugEntity("6845", "Meropenem", "IN", None, ["Meropenem"], ["Merrem"], "J01DH02"),
    "18631": RxNormDrugEntity("18631", "Azithromycin", "IN", None, ["Azithromycin"], ["Zithromax"], "J01FA10"),
    "2551": RxNormDrugEntity("2551", "Ciprofloxacin", "IN", None, ["Ciprofloxacin"], ["Cipro"], "J01MA02"),

    # Endocrine & Diabetes
    "6809": RxNormDrugEntity("6809", "Metformin", "IN", None, ["Metformin"], ["Glucophage"], "A10BA02"),
    "1488564": RxNormDrugEntity("1488564", "Empagliflozin", "IN", None, ["Empagliflozin"], ["Jardiance"], "A10BK03"),
    "1484857": RxNormDrugEntity("1484857", "Dapagliflozin", "IN", None, ["Dapagliflozin"], ["Farxiga"], "A10BK01"),
    "1991302": RxNormDrugEntity("1991302", "Semaglutide", "IN", None, ["Semaglutide"], ["Ozempic", "Wegovy", "Rybelsus"], "A10BJ06"),
    "2601736": RxNormDrugEntity("2601736", "Tirzepatide", "IN", None, ["Tirzepatide"], ["Mounjaro", "Zepbound"], "A10BX16"),
    "274783": RxNormDrugEntity("274783", "Insulin Glargine", "IN", None, ["Insulin Glargine"], ["Lantus", "Basaglar", "Toujeo"], "A10AE04"),
    "5856": RxNormDrugEntity("5856", "Insulin Regular", "IN", None, ["Insulin Regular"], ["Humulin R", "Novolin R"], "A10AB01"),
    "10582": RxNormDrugEntity("10582", "Levothyroxine", "IN", None, ["Levothyroxine"], ["Synthroid", "Levoxyl"], "H03AA01"),
}


def lookup_rxnorm(rxcui: str) -> Optional[RxNormDrugEntity]:
    """Retrieves normalized clinical drug definition by RxNorm CUI."""
    return RXNORM_DICTIONARY.get(rxcui)
