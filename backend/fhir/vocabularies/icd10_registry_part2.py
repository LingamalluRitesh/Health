"""
HealthPulse AI — Structured ICD-10-CM Clinical Knowledge Registry (Part 2: Circulatory, Respiratory & Renal).
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


ICD10_REGISTRY_PART2: Dict[str, DiagnosticRegistryEntry] = {
    # Circulatory System (I00-I99)
    "I05.0": DiagnosticRegistryEntry("I05.0", "Rheumatic mitral stenosis", "Chronic rheumatic valvular heart disease with mitral orifice narrowing.", "Chapter IX: Circulatory", "HCC 87", 0.180, True, 4.0),
    "I06.0": DiagnosticRegistryEntry("I06.0", "Rheumatic aortic stenosis", "Rheumatic aortic valve stenosis with commisural fusion.", "Chapter IX: Circulatory", "HCC 87", 0.180, True, 4.5),
    "I20.1": DiagnosticRegistryEntry("I20.1", "Angina pectoris with documented spasm", "Prinzmetal / vasospastic variant angina with transient ST-segment elevation.", "Chapter IX: Circulatory", None, 0.0, True, 2.0),
    "I21.01": DiagnosticRegistryEntry("I21.01", "STEMI involving left main coronary artery", "Catastrophic transmural anterior/lateral myocardial infarction.", "Chapter IX: Circulatory", "HCC 86", 0.290, False, 5.0),
    "I21.02": DiagnosticRegistryEntry("I21.02", "STEMI involving left anterior descending coronary artery", "LAD anterior wall myocardial infarction with high risk of cardiogenic shock.", "Chapter IX: Circulatory", "HCC 86", 0.290, False, 4.5),
    "I21.11": DiagnosticRegistryEntry("I21.11", "STEMI involving right coronary artery", "Inferior wall acute STEMI with risk of right ventricular involvement and AV block.", "Chapter IX: Circulatory", "HCC 86", 0.290, False, 4.0),
    "I21.19": DiagnosticRegistryEntry("I21.19", "STEMI involving other coronary artery of inferior wall", "Posterior / inferior myocardial infarction.", "Chapter IX: Circulatory", "HCC 86", 0.290, False, 4.0),
    "I21.21": DiagnosticRegistryEntry("I21.21", "STEMI involving left circumflex coronary artery", "Lateral wall transmural infarction.", "Chapter IX: Circulatory", "HCC 86", 0.290, False, 4.0),
    "I21.A1": DiagnosticRegistryEntry("I21.A1", "Myocardial infarction type 2", "Myocardial ischemia secondary to supply-demand mismatch (sepsis, hypotension, severe anemia).", "Chapter IX: Circulatory", "HCC 86", 0.290, False, 3.5),
    "I25.2": DiagnosticRegistryEntry("I25.2", "Old myocardial infarction", "Healed prior myocardial infarction (Q waves on ECG) without current acute symptoms.", "Chapter IX: Circulatory", "HCC 87", 0.180, True, 0.0),
    "I27.0": DiagnosticRegistryEntry("I27.0", "Primary pulmonary hypertension", "Idiopathic pulmonary arterial hypertension (WHO Group 1 PAH).", "Chapter IX: Circulatory", "HCC 107", 0.480, True, 6.0),
    "I27.20": DiagnosticRegistryEntry("I27.20", "Pulmonary hypertension, unspecified", "Elevated mean pulmonary artery pressure > 20 mmHg at rest.", "Chapter IX: Circulatory", "HCC 107", 0.480, True, 5.0),
    "I30.0": DiagnosticRegistryEntry("I30.0", "Acute nonspecific idiopathic pericarditis", "Acute pericardial sac inflammation with PR depression and diffuse ST elevation.", "Chapter IX: Circulatory", None, 0.0, False, 2.5),
    "I31.39": DiagnosticRegistryEntry("I31.39", "Other nonrheumatic pericardial effusion", "Pericardial fluid accumulation without active cardiac tamponade.", "Chapter IX: Circulatory", None, 0.0, False, 3.0),
    "I31.4": DiagnosticRegistryEntry("I31.4", "Cardiac tamponade", "Life-threatening intrapericardial pressure elevation with Beck's triad and pulsus paradoxus.", "Chapter IX: Circulatory", "HCC 85", 0.368, False, 6.0),
    "I33.0": DiagnosticRegistryEntry("I33.0", "Acute and subacute infective endocarditis", "Bacterial or fungal microbial vegetation on cardiac valvular endothelium.", "Chapter IX: Circulatory", "HCC 85", 0.368, False, 18.0),
    "I34.0": DiagnosticRegistryEntry("I34.0", "Nonrheumatic mitral (valve) insufficiency", "Severe mitral regurgitation due to myxomatous degeneration / chordal rupture.", "Chapter IX: Circulatory", "HCC 87", 0.180, True, 3.5),
    "I35.0": DiagnosticRegistryEntry("I35.0", "Nonrheumatic aortic valve stenosis", "Calcific degenerative aortic stenosis with mean gradient >= 40 mmHg.", "Chapter IX: Circulatory", "HCC 87", 0.180, True, 4.0),
    "I35.1": DiagnosticRegistryEntry("I35.1", "Nonrheumatic aortic valve insufficiency", "Chronic or acute aortic regurgitation with wide pulse pressure.", "Chapter IX: Circulatory", "HCC 87", 0.180, True, 4.0),
    "I44.1": DiagnosticRegistryEntry("I44.1", "Atrioventricular block, second degree", "Mobitz Type I (Wenckebach) or Mobitz Type II AV nodal / infranodal conduction block.", "Chapter IX: Circulatory", "HCC 96", 0.268, True, 2.5),
    "I44.2": DiagnosticRegistryEntry("I44.2", "Atrioventricular block, complete", "Third-degree complete heart block with AV dissociation requiring pacemaker.", "Chapter IX: Circulatory", "HCC 96", 0.268, True, 4.0),
    "I45.6": DiagnosticRegistryEntry("I45.6", "Pre-excitation syndrome (Wolff-Parkinson-White)", "Accessory atrioventricular pathway (Bundle of Kent) with delta wave on ECG.", "Chapter IX: Circulatory", "HCC 96", 0.268, True, 1.5),
    "I47.1": DiagnosticRegistryEntry("I47.1", "Supraventricular tachycardia", "Paroxysmal SVT (AVNRT or AVRT) responsive to IV Adenosine or vagal maneuvers.", "Chapter IX: Circulatory", "HCC 96", 0.268, False, 1.0),
    "I48.20": DiagnosticRegistryEntry("I48.20", "Chronic atrial fibrillation, unspecified", "Permanent or long-standing persistent AFib.", "Chapter IX: Circulatory", "HCC 96", 0.268, True, 2.0),
    "I48.3": DiagnosticRegistryEntry("I48.3", "Typical atrial flutter", "Macroreentrant cavotricuspid isthmus-dependent atrial flutter (sawtooth F waves).", "Chapter IX: Circulatory", "HCC 96", 0.268, True, 2.0),
    "I50.1": DiagnosticRegistryEntry("I50.1", "Left ventricular failure, unspecified", "Acute pulmonary edema secondary to acute left ventricular decompensation.", "Chapter IX: Circulatory", "HCC 85", 0.368, False, 4.5),
    "I50.40": DiagnosticRegistryEntry("I50.40", "Unspecified combined systolic and diastolic heart failure", "Mixed systolic and diastolic heart failure.", "Chapter IX: Circulatory", "HCC 85", 0.368, True, 4.0),
    "I50.42": DiagnosticRegistryEntry("I50.42", "Chronic combined systolic and diastolic heart failure", "Chronic heart failure with both reduced LVEF and elevated filling pressures.", "Chapter IX: Circulatory", "HCC 85", 0.368, True, 3.8),
    "I50.814": DiagnosticRegistryEntry("I50.814", "Right heart failure due to left heart failure", "Secondary pulmonary hypertension-induced right ventricular decompensation.", "Chapter IX: Circulatory", "HCC 85", 0.368, True, 5.0),
    "I70.201": DiagnosticRegistryEntry("I70.201", "Unspecified atherosclerosis of native arteries of extremities, right leg", "Peripheral arterial disease (PAD) with claudication.", "Chapter IX: Circulatory", "HCC 108", 0.280, True, 1.0),
    "I71.01": DiagnosticRegistryEntry("I71.01", "Dissection of thoracic aorta", "Stanford Type A (surgical emergency) or Type B aortic dissection.", "Chapter IX: Circulatory", "HCC 106", 0.880, False, 10.0),
    "I71.4": DiagnosticRegistryEntry("I71.4", "Abdominal aortic aneurysm, without rupture", "Infrarenal AAA with diameter >= 3.0 cm.", "Chapter IX: Circulatory", "HCC 107", 0.480, True, 3.0),
    "I71.3": DiagnosticRegistryEntry("I71.3", "Abdominal aortic aneurysm, ruptured", "Catastrophic ruptured AAA presenting with abdominal/back pain, pulsatile mass, and shock.", "Chapter IX: Circulatory", "HCC 106", 0.880, False, 12.0),

    # Respiratory System (J00-J99)
    "J09.X2": DiagnosticRegistryEntry("J09.X2", "Influenza due to identified novel influenza A virus with other respiratory manifestations", "Avian or pandemic influenza infection.", "Chapter X: Respiratory", None, 0.0, False, 4.0),
    "J10.00": DiagnosticRegistryEntry("J10.00", "Influenza due to other identified influenza virus with unspecified type of pneumonia", "Seasonal Influenza A or B viral pneumonia.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 4.5),
    "J12.82": DiagnosticRegistryEntry("J12.82", "Coronavirus disease 2019 (COVID-19) pneumonia", "Severe SARS-CoV-2 viral pneumonia with bilateral ground-glass opacities.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 7.5),
    "J13": DiagnosticRegistryEntry("J13", "Pneumonia due to Streptococcus pneumoniae", "Classic lobar pneumococcal pneumonia with rusty sputum.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 4.0),
    "J14": DiagnosticRegistryEntry("J14", "Pneumonia due to Hemophilus influenzae", "Bacterial pneumonia caused by H. influenzae in COPD/elderly.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 4.0),
    "J15.6": DiagnosticRegistryEntry("J15.6", "Pneumonia due to other Gram-negative bacteria", "Hospital-acquired Enterobacter, Proteus, or Serratia pneumonia.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 6.5),
    "J15.7": DiagnosticRegistryEntry("J15.7", "Pneumonia due to Mycoplasma pneumoniae", "Atypical 'walking' pneumonia with cold agglutinins.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 2.0),
    "J18.0": DiagnosticRegistryEntry("J18.0", "Bronchopneumonia, unspecified organism", "Patchy consolidation affecting one or more pulmonary lobules.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 3.8),
    "J43.9": DiagnosticRegistryEntry("J43.9", "Emphysema, unspecified", "Panacinar or centriacinar pulmonary parenchymal destruction.", "Chapter X: Respiratory", "HCC 111", 0.335, True, 2.0),
    "J47.9": DiagnosticRegistryEntry("J47.9", "Bronchiectasis, uncomplicated", "Permanent irreversible dilation of bronchi with chronic purulent sputum.", "Chapter X: Respiratory", "HCC 112", 0.280, True, 3.0),
    "J84.10": DiagnosticRegistryEntry("J84.10", "Pulmonary fibrosis, unspecified", "Idiopathic pulmonary fibrosis or interstitial lung disease (UIP pattern).", "Chapter X: Respiratory", "HCC 112", 0.280, True, 5.0),
    "J85.2": DiagnosticRegistryEntry("J85.2", "Abscess of lung without pneumonia", "Cavity filled with purulent fluid resulting from lung tissue necrosis.", "Chapter X: Respiratory", "HCC 114", 0.210, False, 12.0),
    "J90": DiagnosticRegistryEntry("J90", "Pleural effusion, not elsewhere classified", "Transudative or exudative fluid accumulation in the pleural cavity.", "Chapter X: Respiratory", None, 0.0, False, 3.0),
    "J91.0": DiagnosticRegistryEntry("J91.0", "Malignant pleural effusion", "Pleural fluid containing malignant tumor cells.", "Chapter X: Respiratory", "HCC 26", 0.880, True, 4.0),
    "J93.0": DiagnosticRegistryEntry("J93.0", "Spontaneous tension pneumothorax", "One-way valve air trapping in pleural space with mediastinal shift and shock.", "Chapter X: Respiratory", None, 0.0, False, 4.0),
};
