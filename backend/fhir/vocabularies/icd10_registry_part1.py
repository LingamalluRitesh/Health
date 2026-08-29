"""
HealthPulse AI — Structured ICD-10-CM Clinical Knowledge Registry (Part 1: Infectious, Neoplasms & Endocrine).
Contains validated clinical diagnostic codes, HCC risk weights, and clinical documentation guidelines.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DiagnosticRegistryEntry:
    code: str
    preferred_term: str
    clinical_definition: str
    who_chapter: str
    hcc_v28_category: Optional[str]
    raf_coefficient: float
    is_chronic: bool
    typical_los_days: float


ICD10_REGISTRY_PART1: Dict[str, DiagnosticRegistryEntry] = {
    # Infectious Diseases (A00-B99)
    "A00.0": DiagnosticRegistryEntry("A00.0", "Cholera due to Vibrio cholerae 01, biovar cholerae", "Acute severe watery diarrheal illness caused by toxigenic V. cholerae.", "Chapter I: Infectious Diseases", None, 0.0, False, 3.5),
    "A00.1": DiagnosticRegistryEntry("A00.1", "Cholera due to Vibrio cholerae 01, biovar eltor", "Epidemic cholera infection caused by the El Tor biotype.", "Chapter I: Infectious Diseases", None, 0.0, False, 3.2),
    "A00.9": DiagnosticRegistryEntry("A00.9", "Cholera, unspecified", "Cholera enterotoxin gastroenteritis NOS.", "Chapter I: Infectious Diseases", None, 0.0, False, 3.0),
    "A01.00": DiagnosticRegistryEntry("A01.00", "Typhoid fever, unspecified", "Systemic invasive Salmonella enterica serotype Typhi infection.", "Chapter I: Infectious Diseases", None, 0.0, False, 5.2),
    "A01.01": DiagnosticRegistryEntry("A01.01", "Typhoid meningitis", "Central nervous system Salmonella Typhi infection with meningeal inflammation.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 14.0),
    "A01.02": DiagnosticRegistryEntry("A01.02", "Typhoid fever with heart involvement", "Myocarditis or endocarditis secondary to typhoid bacteremia.", "Chapter I: Infectious Diseases", "HCC 85", 0.368, False, 10.5),
    "A01.03": DiagnosticRegistryEntry("A01.03", "Typhoid pneumonia", "Lower respiratory tract infection caused by Salmonella Typhi.", "Chapter I: Infectious Diseases", "HCC 114", 0.210, False, 7.0),
    "A01.04": DiagnosticRegistryEntry("A01.04", "Typhoid arthritis", "Septic joint infection caused by Salmonella Typhi bacteremia.", "Chapter I: Infectious Diseases", None, 0.0, False, 8.0),
    "A01.05": DiagnosticRegistryEntry("A01.05", "Typhoid osteomyelitis", "Bone marrow and osseous infection caused by Salmonella Typhi.", "Chapter I: Infectious Diseases", None, 0.0, False, 12.0),
    "A02.1": DiagnosticRegistryEntry("A02.1", "Salmonella sepsis", "Invasive non-typhoidal Salmonella bloodstream infection with organ dysfunction.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 8.4),
    "A04.0": DiagnosticRegistryEntry("A04.0", "Enteropathogenic Escherichia coli infection", "EPEC-mediated acute infantile and adult secretory diarrhea.", "Chapter I: Infectious Diseases", None, 0.0, False, 2.8),
    "A04.1": DiagnosticRegistryEntry("A04.1", "Enterotoxigenic Escherichia coli infection", "ETEC traveler's diarrhea mediated by heat-labile and heat-stable enterotoxins.", "Chapter I: Infectious Diseases", None, 0.0, False, 2.5),
    "A04.2": DiagnosticRegistryEntry("A04.2", "Enteroinvasive Escherichia coli infection", "EIEC acute invasive colitis resembling shigellosis.", "Chapter I: Infectious Diseases", None, 0.0, False, 3.2),
    "A04.3": DiagnosticRegistryEntry("A04.3", "Enterohemorrhagic Escherichia coli infection", "EHEC / STEC O157:H7 infection producing Shiga-like toxins with HUS risk.", "Chapter I: Infectious Diseases", None, 0.0, False, 6.5),
    "A04.4": DiagnosticRegistryEntry("A04.4", "Other intestinal Escherichia coli infections", "Enteroaggregative and diffusely adherent E. coli gastroenteritis.", "Chapter I: Infectious Diseases", None, 0.0, False, 2.4),
    "A04.5": DiagnosticRegistryEntry("A04.5", "Campylobacter enteritis", "Acute inflammatory enterocolitis caused by Campylobacter jejuni with Guillain-Barre risk.", "Chapter I: Infectious Diseases", None, 0.0, False, 3.1),
    "A04.6": DiagnosticRegistryEntry("A04.6", "Enteritis due to Yersinia enterocolitica", "Yersinia enterocolitis presenting with pseudoappendicitis and mesenteric adenitis.", "Chapter I: Infectious Diseases", None, 0.0, False, 4.0),
    "A05.0": DiagnosticRegistryEntry("A05.0", "Foodborne staphylococcal intoxication", "Preformed enterotoxin food poisoning with rapid onset emesis within 1-6 hours.", "Chapter I: Infectious Diseases", None, 0.0, False, 1.2),
    "A05.1": DiagnosticRegistryEntry("A05.1", "Botulism food poisoning", "Clostridium botulinum neurotoxin-mediated descending flaccid paralysis.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 18.0),
    "A08.0": DiagnosticRegistryEntry("A08.0", "Rotaviral enteritis", "Rotavirus severe dehydrating infantile diarrhea.", "Chapter I: Infectious Diseases", None, 0.0, False, 2.5),
    "A08.11": DiagnosticRegistryEntry("A08.11", "Acute gastroenteropathy due to Norwalk agent", "Norovirus acute viral gastroenteritis with high secondary attack rate.", "Chapter I: Infectious Diseases", None, 0.0, False, 1.5),
    "A15.0": DiagnosticRegistryEntry("A15.0", "Tuberculosis of lung", "Acid-fast Mycobacterium tuberculosis pulmonary cavitary disease.", "Chapter I: Infectious Diseases", None, 0.0, True, 14.0),
    "A17.0": DiagnosticRegistryEntry("A17.0", "Tuberculous meningitis", "Mycobacterial basilar meningitis with cranial neuropathies and CSF lymphocytic pleocytosis.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, True, 21.0),
    "A39.0": DiagnosticRegistryEntry("A39.0", "Meningococcal meningitis", "Neisseria meningitidis acute purulent leptomeningitis with petechial purpura.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 9.5),
    "A39.1": DiagnosticRegistryEntry("A39.1", "Waterhouse-Friderichsen syndrome", "Fulminant meningococcemia with bilateral adrenal hemorrhage and shock.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 16.0),
    "A48.0": DiagnosticRegistryEntry("A48.0", "Gas gangrene", "Clostridium perfringens myonecrosis with crepitus and systemic toxemia.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 14.0),
    "A48.3": DiagnosticRegistryEntry("A48.3", "Toxic shock syndrome", "Staphylococcal TSST-1 or Streptococcal pyrogenic exotoxin superantigen shock.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 11.0),
    "B00.1": DiagnosticRegistryEntry("B00.1", "Herpesviral vesicular dermatitis", "HSV-1 or HSV-2 cutaneous grouped vesicles on an erythematous base.", "Chapter I: Infectious Diseases", None, 0.0, False, 1.0),
    "B00.4": DiagnosticRegistryEntry("B00.4", "Herpesviral encephalitis", "HSV-1 temporal lobe necrotizing encephalitis requiring IV Acyclovir STAT.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 14.0),
    "B02.9": DiagnosticRegistryEntry("B02.9", "Zoster without complications", "Varicella-zoster virus dermatomal reactivated shingles.", "Chapter I: Infectious Diseases", None, 0.0, False, 1.0),
    "B25.0": DiagnosticRegistryEntry("B25.0", "Cytomegaloviral pneumonitis", "CMV interstitial pneumonitis in immunocompromised/transplant host.", "Chapter I: Infectious Diseases", "HCC 114", 0.210, False, 12.0),
    "B37.0": DiagnosticRegistryEntry("B37.0", "Candidal stomatitis", "Oral candidiasis / thrush with scrapable pseudomembranous plaques.", "Chapter I: Infectious Diseases", None, 0.0, False, 1.0),
    "B37.7": DiagnosticRegistryEntry("B37.7", "Candidal sepsis", "Invasive candidemia with positive blood cultures requiring Echinocandin therapy.", "Chapter I: Infectious Diseases", "HCC 2", 0.450, False, 14.5),
    "B44.0": DiagnosticRegistryEntry("B44.0", "Invasive pulmonary aspergillosis", "Angioinvasive Aspergillus mold infection in neutropenic host (Halo sign on CT).", "Chapter I: Infectious Diseases", "HCC 114", 0.210, False, 18.0),
    "B59": DiagnosticRegistryEntry("B59", "Pneumocystosis", "Pneumocystis jirovecii pneumonia (PCP) in advanced HIV/AIDS or immunosuppression.", "Chapter I: Infectious Diseases", "HCC 114", 0.210, False, 10.0),

    # Neoplasms (C00-D49)
    "C15.9": DiagnosticRegistryEntry("C15.9", "Malignant neoplasm of esophagus, unspecified", "Esophageal adenocarcinoma or squamous cell carcinoma.", "Chapter II: Neoplasms", "HCC 28", 0.298, True, 7.5),
    "C16.9": DiagnosticRegistryEntry("C16.9", "Malignant neoplasm of stomach, unspecified", "Gastric adenocarcinoma (intestinal or diffuse linitis plastica type).", "Chapter II: Neoplasms", "HCC 28", 0.298, True, 8.0),
    "C22.0": DiagnosticRegistryEntry("C22.0", "Liver cell carcinoma", "Primary hepatocellular carcinoma (HCC) in cirrhotic liver.", "Chapter II: Neoplasms", "HCC 27", 0.650, True, 7.0),
    "C22.1": DiagnosticRegistryEntry("C22.1", "Intrahepatic bile duct carcinoma", "Intrahepatic cholangiocarcinoma arising from biliary epithelium.", "Chapter II: Neoplasms", "HCC 27", 0.650, True, 8.5),
    "C34.11": DiagnosticRegistryEntry("C34.11", "Malignant neoplasm of upper lobe, right bronchus or lung", "Right upper lobe primary lung adenocarcinoma or squamous cell carcinoma.", "Chapter II: Neoplasms", "HCC 27", 0.650, True, 6.0),
    "C34.12": DiagnosticRegistryEntry("C34.12", "Malignant neoplasm of upper lobe, left bronchus or lung", "Left upper lobe primary bronchogenic carcinoma.", "Chapter II: Neoplasms", "HCC 27", 0.650, True, 6.0),
    "C43.9": DiagnosticRegistryEntry("C43.9", "Malignant melanoma of skin, unspecified", "Cutaneous malignant melanoma with deep invasion / Breslow depth.", "Chapter II: Neoplasms", "HCC 29", 0.160, True, 2.0),
    "C56.9": DiagnosticRegistryEntry("C56.9", "Malignant neoplasm of unspecified ovary", "High-grade serous ovarian adenocarcinoma with BRCA1/2 association.", "Chapter II: Neoplasms", "HCC 28", 0.298, True, 7.0),
    "C64.9": DiagnosticRegistryEntry("C64.9", "Malignant neoplasm of unspecified kidney, except renal pelvis", "Clear cell renal cell carcinoma arising from proximal tubular epithelium.", "Chapter II: Neoplasms", "HCC 28", 0.298, True, 5.0),
    "C67.9": DiagnosticRegistryEntry("C67.9", "Malignant neoplasm of bladder, unspecified", "Urothelial (transitional cell) carcinoma of urinary bladder.", "Chapter II: Neoplasms", "HCC 28", 0.298, True, 4.5),
    "C71.9": DiagnosticRegistryEntry("C71.9", "Malignant neoplasm of brain, unspecified", "Glioblastoma multiforme (IDH-wildtype Grade 4 astrocytoma).", "Chapter II: Neoplasms", "HCC 27", 0.650, True, 9.0),
    "C81.90": DiagnosticRegistryEntry("C81.90", "Hodgkin lymphoma, unspecified, not having achieved remission", "Classic Hodgkin lymphoma characterized by Reed-Sternberg cells.", "Chapter II: Neoplasms", "HCC 25", 0.720, True, 6.5),
    "C83.30": DiagnosticRegistryEntry("C83.30", "Diffuse large B-cell lymphoma not having achieved remission", "Aggressive DLBCL requiring R-CHOP chemo-immunotherapy.", "Chapter II: Neoplasms", "HCC 25", 0.720, True, 8.0),
    "C85.90": DiagnosticRegistryEntry("C85.90", "Non-Hodgkin lymphoma, unspecified, not having achieved remission", "B-cell or T-cell non-Hodgkin lymphoma NOS.", "Chapter II: Neoplasms", "HCC 25", 0.720, True, 6.0),
    "C91.00": DiagnosticRegistryEntry("C91.00", "Acute lymphoblastic leukemia not having achieved remission", "Pre-B or Pre-T acute lymphoblastic leukemia / blast crisis.", "Chapter II: Neoplasms", "HCC 25", 0.720, True, 28.0),
    "C92.10": DiagnosticRegistryEntry("C92.10", "Chronic myeloid leukemia, BCR/ABL-positive, not having achieved remission", "Philadelphia chromosome t(9;22) CML responsive to Imatinib/Dasatinib TKIs.", "Chapter II: Neoplasms", "HCC 25", 0.720, True, 4.0),
};
