"""
HealthPulse AI — Evidence-Based Psychiatry & Psychopharmacology Clinical Practice Guidelines.
Implements APA (American Psychiatric Association) and CANMAT clinical practice guidelines:
- Major Depressive Disorder (MDD: PHQ-9 Staging, SSRI / SNRI Selection, Treatment-Resistant Algorithms)
- Bipolar Disorder (Type I & II: Acute Mania Lithium / Valproate vs Bipolar Depression Quetiapine / Lurasidone)
- Schizophrenia & Psychosis (Second-Generation Antipsychotics, Clozapine for Treatment Resistance & ANC Monitoring)
- Delirium in Hospitalized / ICU Patients (CAM-ICU, Non-Pharmacologic Sleep Bundles, Antipsychotic De-escalation)
- Alcohol Withdrawal Syndrome (CIWA-Ar Protocol & Symptom-Triggered Benzodiazepines / Chlordiazepoxide)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class PsychiatryGuidelineEvaluation:
    guideline_source: str
    psychiatric_disorder: str
    severity_assessment: str
    first_line_psychopharmacology: List[str]
    critical_black_box_monitoring: List[str]
    evidence_based_psychotherapy: str


class PsychiatryGuidelineEngine:
    """Evaluates psychiatric rating scales, drug interactions, and neuromodulation indications."""

    @staticmethod
    def evaluate_mdd_pharmacotherapy(
        phq9_score: int,
        has_treatment_resistance: bool = False,
        has_anxiety_comorbidity: bool = True,
        has_insomnia: bool = True,
    ) -> PsychiatryGuidelineEvaluation:
        """
        APA 2019 / CANMAT 2023 Guidelines for the Management of Major Depressive Disorder.
        PHQ-9 10-14: Moderate, 15-19: Moderately Severe, 20-27: Severe.
        """
        first_line = []
        if has_treatment_resistance:
            first_line.append("Atypical Antipsychotic Augmentation: Aripiprazole (2-5mg daily) OR Brexpiprazole (0.5-2mg daily) added to current antidepressant (Category 1 Evidence).")
            first_line.append("Alternative Augmentation: Lithium Carbonate (target serum level 0.6-0.8 mEq/L) OR Esketamine Nasal Spray (Spravato) + Oral SSRI.")
            first_line.append("Neuromodulation: Repetitive Transcranial Magnetic Stimulation (rTMS) or Electroconvulsive Therapy (ECT) for severe treatment-resistant or catatonic depression.")
        else:
            first_line.append("First-Line SSRI Monotherapy: Escitalopram 10-20mg daily OR Sertraline 50-100mg daily (optimal balance of efficacy and tolerability).")
            if has_insomnia and has_anxiety_comorbidity:
                first_line.append("Alternative: Mirtazapine 15-30mg at bedtime (promotes sleep and appetite without sexual dysfunction).")

        return PsychiatryGuidelineEvaluation(
            guideline_source="APA / CANMAT 2023 Major Depression Guidelines",
            psychiatric_disorder="Major Depressive Disorder (MDD)",
            severity_assessment=f"PHQ-9 Score: {phq9_score}/27 ({'Severe MDD' if phq9_score >= 20 else 'Moderately Severe MDD' if phq9_score >= 15 else 'Moderate MDD'})",
            first_line_psychopharmacology=first_line,
            critical_black_box_monitoring=[
                "FDA Boxed Warning: Antidepressants increase the risk of suicidal thoughts and behaviors in pediatric and young adult patients (aged <= 24). Monitor closely during initial 4-8 weeks.",
                "Screen for Bipolar mania history before starting antidepressant monotherapy to avoid precipitating manic switch.",
            ],
            evidence_based_psychotherapy="Cognitive Behavioral Therapy (CBT) or Interpersonal Psychotherapy (IPT) combined with pharmacotherapy provides superior outcomes compared to monotherapy alone.",
        )
