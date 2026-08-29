"""
HealthPulse AI — Structured ICD-10-CM Clinical Knowledge Registry (Part 3: Neurology, GI, Musculoskeletal & Injuries).
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


ICD10_REGISTRY_PART3: Dict[str, DiagnosticRegistryEntry] = {
    # Diseases of the Nervous System (G00-G99)
    "G00.1": DiagnosticRegistryEntry("G00.1", "Pneumococcal meningitis", "Streptococcus pneumoniae acute purulent leptomeningitis.", "Chapter VI: Nervous System", "HCC 2", 0.450, False, 14.0),
    "G00.2": DiagnosticRegistryEntry("G00.2", "Streptococcal meningitis", "Group B or other streptococcal CNS infection.", "Chapter VI: Nervous System", "HCC 2", 0.450, False, 12.0),
    "G00.3": DiagnosticRegistryEntry("G00.3", "Staphylococcal meningitis", "Post-neurosurgical or bacteremic S. aureus meningitis.", "Chapter VI: Nervous System", "HCC 2", 0.450, False, 14.0),
    "G03.9": DiagnosticRegistryEntry("G03.9", "Meningitis, unspecified", "Aseptic or bacterial leptomeningeal inflammation.", "Chapter VI: Nervous System", "HCC 2", 0.450, False, 6.0),
    "G04.90": DiagnosticRegistryEntry("G04.90", "Encephalitis and encephalomyelitis, unspecified", "Inflammation of the brain parenchyma.", "Chapter VI: Nervous System", "HCC 2", 0.450, False, 10.0),
    "G06.0": DiagnosticRegistryEntry("G06.0", "Intracranial abscess and granuloma", "Cerebral brain abscess requiring surgical drainage and prolonged IV antibiotics.", "Chapter VI: Nervous System", "HCC 2", 0.450, False, 21.0),
    "G12.21": DiagnosticRegistryEntry("G12.21", "Amyotrophic lateral sclerosis (ALS)", "Progressive neurodegenerative disease affecting upper and lower motor neurons (Lou Gehrig disease).", "Chapter VI: Nervous System", "HCC 180", 1.050, True, 4.0),
    "G20": DiagnosticRegistryEntry("G20", "Parkinson's disease", "Neurodegenerative movement disorder characterized by resting tremor, rigidity, bradykinesia, and postural instability.", "Chapter VI: Nervous System", "HCC 182", 0.520, True, 3.5),
    "G30.9": DiagnosticRegistryEntry("G30.9", "Alzheimer's disease, unspecified", "Primary degenerative dementia with extracellular amyloid-beta plaques and neurofibrillary tangles.", "Chapter VI: Nervous System", "HCC 127", 0.350, True, 4.0),
    "G35": DiagnosticRegistryEntry("G35", "Multiple sclerosis", "Autoimmune demyelinating disease of the central nervous system with periventricular white matter lesions.", "Chapter VI: Nervous System", "HCC 181", 0.450, True, 4.5),
    "G40.309": DiagnosticRegistryEntry("G40.309", "Generalized idiopathic epilepsy and epileptic syndromes, not intractable, without status epilepticus", "Grand mal convulsive seizure disorder.", "Chapter VI: Nervous System", "HCC 183", 0.280, True, 1.5),
    "G40.802": DiagnosticRegistryEntry("G40.802", "Other epilepsy, not intractable, with status epilepticus", "Epilepsy complicated by status epilepticus.", "Chapter VI: Nervous System", "HCC 183", 0.280, False, 5.0),
    "G40.901": DiagnosticRegistryEntry("G40.901", "Epilepsy, unspecified, not intractable, with status epilepticus", "Unspecified status epilepticus requiring ICU neurocritical care.", "Chapter VI: Nervous System", "HCC 183", 0.280, False, 5.5),
    "G43.909": DiagnosticRegistryEntry("G43.909", "Age-related migraine, unspecified, not intractable, without status migrainosus", "Unilateral throbbing vascular headache with nausea and photophobia.", "Chapter VI: Nervous System", None, 0.0, True, 0.0),
    "G45.9": DiagnosticRegistryEntry("G45.9", "Transient cerebral ischemic attack, unspecified", "Focal neurological deficit resolving within 24 hours without acute infarction on MRI.", "Chapter VI: Nervous System", "HCC 248", 0.120, False, 1.5),
    "G61.0": DiagnosticRegistryEntry("G61.0", "Guillain-Barre syndrome (GBS)", "Acute inflammatory demyelinating polyneuropathy (AIDP) presenting with ascending weakness and areflexia.", "Chapter VI: Nervous System", "HCC 180", 1.050, False, 14.0),
    "G70.00": DiagnosticRegistryEntry("G70.00", "Myasthenia gravis without (acute) exacerbation", "Autoimmune neuromuscular junction disorder with anti-AChR antibodies and fatigable weakness.", "Chapter VI: Nervous System", "HCC 180", 1.050, True, 2.0),
    "G70.01": DiagnosticRegistryEntry("G70.01", "Myasthenia gravis with (acute) exacerbation (Crisis)", "Myasthenic crisis with acute bulbar and diaphragm respiratory failure requiring plasmapheresis / IVIG.", "Chapter VI: Nervous System", "HCC 180", 1.050, False, 12.0),
    "G93.1": DiagnosticRegistryEntry("G93.1", "Anoxic brain damage", "Hypoxic-ischemic encephalopathy (HIE) following cardiac arrest or profound asphyxia.", "Chapter VI: Nervous System", "HCC 178", 0.480, True, 10.0),
    "G93.41": DiagnosticRegistryEntry("G93.41", "Metabolic encephalopathy", "Reversible toxic/metabolic altered mental status (hepatic, uremic, septic).", "Chapter VI: Nervous System", None, 0.0, False, 3.5),

    # Diseases of Digestive System (K00-K95)
    "K21.0": DiagnosticRegistryEntry("K21.0", "Gastro-esophageal reflux disease with esophagitis", "Erosive GERD with mucosal breaks on endoscopy.", "Chapter XI: Digestive", None, 0.0, True, 0.0),
    "K25.0": DiagnosticRegistryEntry("K25.0", "Acute gastric ulcer with hemorrhage", "Bleeding stomach peptic ulcer requiring endoscopic clipping / thermal coagulation.", "Chapter XI: Digestive", None, 0.0, False, 3.0),
    "K26.0": DiagnosticRegistryEntry("K26.0", "Acute duodenal ulcer with hemorrhage", "Bleeding duodenal bulb ulcer eroding into gastroduodenal artery.", "Chapter XI: Digestive", None, 0.0, False, 3.5),
    "K50.90": DiagnosticRegistryEntry("K50.90", "Crohn's disease, unspecified, without complications", "Transmural granulomatous inflammatory bowel disease with skip lesions.", "Chapter XI: Digestive", "HCC 68", 0.260, True, 2.0),
    "K51.90": DiagnosticRegistryEntry("K51.90", "Ulcerative colitis, unspecified, without complications", "Continuous mucosal inflammation of the colon extending proximally from rectum.", "Chapter XI: Digestive", "HCC 68", 0.260, True, 2.5),
    "K56.60": DiagnosticRegistryEntry("K56.60", "Unspecified intestinal obstruction", "Mechanical bowel obstruction (small or large intestine).", "Chapter XI: Digestive", None, 0.0, False, 4.0),
    "K57.32": DiagnosticRegistryEntry("K57.32", "Diverticulitis of large intestine without perforation or abscess without bleeding", "Acute sigmoid diverticulitis with left lower quadrant pain and fever.", "Chapter XI: Digestive", None, 0.0, False, 3.0),
    "K65.0": DiagnosticRegistryEntry("K65.0", "Generalized (acute) peritonitis", "Purulent intra-abdominal peritonitis secondary to hollow viscus perforation.", "Chapter XI: Digestive", "HCC 2", 0.450, False, 8.0),
    "K70.30": DiagnosticRegistryEntry("K70.30", "Alcoholic cirrhosis of liver without ascites", "End-stage alcoholic liver disease with bridging fibrosis and regenerative nodules.", "Chapter XI: Digestive", "HCC 64", 0.420, True, 3.0),
    "K70.31": DiagnosticRegistryEntry("K70.31", "Alcoholic cirrhosis of liver with ascites", "Decompensated alcoholic cirrhosis with peritoneal fluid accumulation.", "Chapter XI: Digestive", "HCC 64", 0.420, True, 5.0),
    "K74.60": DiagnosticRegistryEntry("K74.60", "Unspecified cirrhosis of liver", "Non-alcoholic steatohepatitis (NASH) or cryptogenic cirrhosis.", "Chapter XI: Digestive", "HCC 64", 0.420, True, 3.5),
    "K76.7": DiagnosticRegistryEntry("K76.7", "Hepatorenal syndrome", "Severe functional vasoconstrictive renal failure in end-stage cirrhosis (HRS-AKI).", "Chapter XI: Digestive", "HCC 64", 0.420, False, 10.5),
    "K80.00": DiagnosticRegistryEntry("K80.00", "Calculus of gallbladder with acute cholecystitis without obstruction", "Acute cystic duct gallstone impaction with Murphy sign.", "Chapter XI: Digestive", None, 0.0, False, 2.5),
    "K81.0": DiagnosticRegistryEntry("K81.0", "Acute cholecystitis", "Acute gallbladder inflammation requiring laparoscopic cholecystectomy.", "Chapter XI: Digestive", None, 0.0, False, 2.5),
    "K83.01": DiagnosticRegistryEntry("K83.01", "Primary sclerosing cholangitis", "Chronic progressive fibro-obliterative cholestatic disease of intra- and extrahepatic bile ducts.", "Chapter XI: Digestive", "HCC 65", 0.150, True, 4.0),
    "K85.90": DiagnosticRegistryEntry("K85.90", "Acute pancreatitis without necrosis or infection, unspecified", "Acute enzymatic autodigestion of pancreatic parenchyma.", "Chapter XI: Digestive", None, 0.0, False, 3.5),
    "K85.91": DiagnosticRegistryEntry("K85.91", "Acute pancreatitis with uninfected necrosis, unspecified", "Necrotizing acute pancreatitis without secondary bacterial contamination.", "Chapter XI: Digestive", "HCC 65", 0.150, False, 12.0),
    "K85.92": DiagnosticRegistryEntry("K85.92", "Acute pancreatitis with infected necrosis, unspecified", "Infected pancreatic parenchymal necrosis requiring step-up necrosectomy.", "Chapter XI: Digestive", "HCC 2", 0.450, False, 24.0),
};
