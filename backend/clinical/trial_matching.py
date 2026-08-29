"""
HealthPulse AI — Precision Clinical Trial Eligibility Matcher.
Matches patient EHR profiles (demographics, ICD-10 diagnoses, lab thresholds, and genomic mutations)
against clinical trial inclusion/exclusion criteria.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ClinicalTrialCriteria:
    trial_id: str
    title: str
    phase: str
    condition: str
    min_age: int = 18
    max_age: int = 85
    required_genders: List[str] = field(default_factory=lambda: ["male", "female", "other"])
    required_icd10_codes: List[str] = field(default_factory=list)
    excluded_icd10_codes: List[str] = field(default_factory=list)
    min_egfr: Optional[float] = None
    min_platelets: Optional[float] = None
    max_bilirubin: Optional[float] = None
    required_mutations: List[str] = field(default_factory=list)
    excluded_mutations: List[str] = field(default_factory=list)


@dataclass
class TrialEligibilityResult:
    trial_id: str
    title: str
    is_eligible: bool
    match_score_percent: float
    passed_criteria: List[str]
    failed_criteria: List[str]
    pending_criteria: List[str]


class ClinicalTrialMatcher:
    """Evaluates patient clinical records against clinical trial protocols."""

    def __init__(self):
        self.trials: List[ClinicalTrialCriteria] = []
        self._init_sample_trials()

    def _init_sample_trials(self):
        self.trials.append(
            ClinicalTrialCriteria(
                trial_id="NCT04875321",
                title="Phase III Trial of SGLT2 Inhibitor in Advanced Diabetic Nephropathy",
                phase="Phase 3",
                condition="Diabetic Kidney Disease",
                min_age=25,
                max_age=75,
                required_icd10_codes=["E11.22", "N18.3", "N18.4"],
                excluded_icd10_codes=["E10", "N18.6"],
                min_egfr=25.0,
                min_platelets=100.0,
                max_bilirubin=2.0,
            )
        )
        self.trials.append(
            ClinicalTrialCriteria(
                trial_id="NCT05219904",
                title="Phase II Targeted Immunotherapy for EGFR Exon 20 Insertion Non-Small Cell Lung Cancer",
                phase="Phase 2",
                condition="NSCLC",
                min_age=18,
                max_age=80,
                required_icd10_codes=["C34.90", "C34.1"],
                required_mutations=["EGFR:exon20ins"],
                excluded_mutations=["KRAS:G12D"],
                min_egfr=45.0,
                min_platelets=100.0,
            )
        )
        self.trials.append(
            ClinicalTrialCriteria(
                trial_id="NCT03984112",
                title="Phase III Novel Anticoagulation vs Standard Care in Atrial Fibrillation with Heart Failure",
                phase="Phase 3",
                condition="Atrial Fibrillation with HF",
                min_age=50,
                max_age=85,
                required_icd10_codes=["I48.91", "I50.9"],
                excluded_icd10_codes=["I05.0"],
                min_egfr=30.0,
                max_bilirubin=2.5,
            )
        )

    def evaluate_patient(
        self,
        patient_age: int,
        patient_gender: str,
        active_icd10_codes: List[str],
        egfr: Optional[float] = None,
        platelets: Optional[float] = None,
        bilirubin: Optional[float] = None,
        genomic_mutations: Optional[List[str]] = None,
    ) -> List[TrialEligibilityResult]:
        results: List[TrialEligibilityResult] = []
        mutations = set(genomic_mutations or [])
        icd_set = set(active_icd10_codes)

        for trial in self.trials:
            passed = []
            failed = []
            pending = []

            # 1. Age check
            if trial.min_age <= patient_age <= trial.max_age:
                passed.append(f"Age {patient_age} within criteria [{trial.min_age}-{trial.max_age}]")
            else:
                failed.append(f"Age {patient_age} outside criteria [{trial.min_age}-{trial.max_age}]")

            # 2. Gender check
            if patient_gender.lower() in [g.lower() for g in trial.required_genders]:
                passed.append(f"Gender {patient_gender} matches")
            else:
                failed.append(f"Gender {patient_gender} not eligible")

            # 3. Required ICD-10
            if trial.required_icd10_codes:
                matched_req = [c for c in trial.required_icd10_codes if c in icd_set]
                if matched_req:
                    passed.append(f"Matching condition diagnosis: {', '.join(matched_req)}")
                else:
                    failed.append(f"Missing required ICD-10 diagnosis: {', '.join(trial.required_icd10_codes)}")

            # 4. Excluded ICD-10
            if trial.excluded_icd10_codes:
                matched_exc = [c for c in trial.excluded_icd10_codes if c in icd_set]
                if matched_exc:
                    failed.append(f"Has exclusion diagnosis: {', '.join(matched_exc)}")
                else:
                    passed.append("No exclusion ICD-10 codes present")

            # 5. eGFR
            if trial.min_egfr is not None:
                if egfr is not None:
                    if egfr >= trial.min_egfr:
                        passed.append(f"eGFR {egfr} >= {trial.min_egfr}")
                    else:
                        failed.append(f"eGFR {egfr} < required {trial.min_egfr}")
                else:
                    pending.append(f"Requires recent eGFR >= {trial.min_egfr}")

            # 6. Platelets
            if trial.min_platelets is not None:
                if platelets is not None:
                    if platelets >= trial.min_platelets:
                        passed.append(f"Platelet count {platelets} >= {trial.min_platelets}")
                    else:
                        failed.append(f"Platelet count {platelets} < {trial.min_platelets}")
                else:
                    pending.append(f"Requires platelet count >= {trial.min_platelets}")

            # 7. Genomic Mutations
            if trial.required_mutations:
                matched_mut = [m for m in trial.required_mutations if m in mutations]
                if matched_mut:
                    passed.append(f"Possesses target genomic variant: {', '.join(matched_mut)}")
                else:
                    failed.append(f"Missing required target variant: {', '.join(trial.required_mutations)}")

            total_evaluated = len(passed) + len(failed)
            score_pct = round((len(passed) / total_evaluated * 100.0) if total_evaluated > 0 else 0.0, 1)
            is_elig = len(failed) == 0 and len(passed) > 0

            results.append(
                TrialEligibilityResult(
                    trial_id=trial.trial_id,
                    title=trial.title,
                    is_eligible=is_elig,
                    match_score_percent=score_pct,
                    passed_criteria=passed,
                    failed_criteria=failed,
                    pending_criteria=pending,
                )
            )

        return results
