"""
HealthPulse AI — Evidence-Based Geriatric Medicine & Polypharmacy Guidelines.
Implements AGS (American Geriatrics Society) Beers Criteria (2023 Update) and STOPP/START criteria:
- AGS Beers Criteria 2023: Potentially Inappropriate Medications (PIMs) in Older Adults (Aged >= 65)
- Fall Risk Assessment & Anticholinergic Cognitive Burden (ACB Score)
- Dementia Behavioral Symptoms (BPSD De-escalation & Antipsychotic Safety Warnings)
- Inpatient Delirium Prevention Protocols (Hospital Elder Life Program / HELP Model)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class BeersCriteriaAlert:
    medication_name: str
    drug_class: str
    rationale: str
    recommendation: str
    quality_of_evidence: str
    strength_of_recommendation: str


BEERS_CRITERIA_CATALOG: Dict[str, BeersCriteriaAlert] = {
    "diphenhydramine": BeersCriteriaAlert(
        medication_name="Diphenhydramine",
        drug_class="First-Generation Antihistamine",
        rationale="Highly anticholinergic; clearance reduced with advanced age; high risk of confusion, dry mouth, constipation, urinary retention, and acute delirium.",
        recommendation="Avoid. Use non-pharmacological sleep hygiene or saline nasal spray/second-generation antihistamines (Cetirizine, Fexofenadine).",
        quality_of_evidence="High",
        strength_of_recommendation="Strong",
    ),
    "zolpidem": BeersCriteriaAlert(
        medication_name="Zolpidem / Z-drugs",
        drug_class="Nonbenzodiazepine Benzodiazepine Receptor Agonist",
        rationale="Increased risk of motor vehicle crashes, falls, hip fractures, cognitive decline, and emergency department visits; minimal improvement in sleep latency.",
        recommendation="Avoid. Recommend Cognitive Behavioral Therapy for Insomnia (CBT-I) as first-line.",
        quality_of_evidence="Moderate",
        strength_of_recommendation="Strong",
    ),
    "amitriptyline": BeersCriteriaAlert(
        medication_name="Amitriptyline",
        drug_class="Tricyclic Antidepressant (TCA)",
        rationale="Highly anticholinergic, sedating, and causes orthostatic hypotension; significant cardiac conduction toxicity.",
        recommendation="Avoid. Use SSRIs (Escitalopram, Sertraline) or SNRIs (Duloxetine for neuropathic pain).",
        quality_of_evidence="High",
        strength_of_recommendation="Strong",
    ),
    "indomethacin": BeersCriteriaAlert(
        medication_name="Indomethacin",
        drug_class="Nonsteroidal Anti-inflammatory Drug (NSAID)",
        rationale="Increased risk of gastrointestinal bleeding/peptic ulcer disease, acute kidney injury, fluid retention, and worsening hypertension; most CNS adverse effects among NSAIDs.",
        recommendation="Avoid. Use Topical NSAIDs (Diclofenac gel) or Acetaminophen for localized osteoarthritis.",
        quality_of_evidence="Moderate",
        strength_of_recommendation="Strong",
    ),
    "metoclopramide": BeersCriteriaAlert(
        medication_name="Metoclopramide",
        drug_class="Dopamine Antagonist / Prokinetic",
        rationale="Can cause extrapyramidal symptoms, including irreversible tardive dyskinesia; increased risk in older adults and prolonged use.",
        recommendation="Avoid, unless for gastroparesis with duration <= 12 weeks.",
        quality_of_evidence="Moderate",
        strength_of_recommendation="Strong",
    ),
};
