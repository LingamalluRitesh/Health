"""
HealthPulse AI — OMOP Common Data Model (CDM) v6.0 ETL Pipeline.
Transforms FHIR resources and hospital EHR records into standardized OMOP analytics tables.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from backend.fhir.models import FHIRPatient, FHIRObservation, FHIRCondition


@dataclass
class OMOPPerson:
    person_id: int
    gender_concept_id: int
    year_of_birth: int
    month_of_birth: Optional[int]
    day_of_birth: Optional[int]
    birth_datetime: Optional[str]
    race_concept_id: int
    ethnicity_concept_id: int
    location_id: Optional[int]
    provider_id: Optional[int]
    care_site_id: Optional[int]
    person_source_value: str
    gender_source_value: str


@dataclass
class OMOPMeasurement:
    measurement_id: int
    person_id: int
    measurement_concept_id: int
    measurement_date: str
    measurement_datetime: Optional[str]
    measurement_type_concept_id: int
    operator_concept_id: Optional[int]
    value_as_number: Optional[float]
    value_as_concept_id: Optional[int]
    unit_concept_id: Optional[int]
    range_low: Optional[float]
    range_high: Optional[float]
    measurement_source_value: str
    unit_source_value: Optional[str]


class OMOPTransformer:
    """Transforms FHIR R4 JSON into standardized OMOP CDM tables."""

    GENDER_CONCEPT_MAP: Dict[str, int] = {
        "male": 8507,
        "female": 8532,
        "other": 8521,
        "unknown": 8551,
    }

    LOINC_TO_CONCEPT_MAP: Dict[str, int] = {
        "8867-4": 3027018,    # Heart rate
        "9279-1": 3024171,    # Respiratory rate
        "8480-6": 3004249,    # Systolic blood pressure
        "8462-4": 3012888,    # Diastolic blood pressure
        "2708-6": 40762499,   # Oxygen saturation
        "8310-5": 3020891,    # Body temperature
        "2160-0": 3016723,    # Serum creatinine
        "1975-2": 3024561,    # Total Bilirubin
        "777-3": 3024929,     # Platelet count
        "6690-2": 3000905,    # White blood cells
        "2524-7": 3037165,    # Serum Lactate
    }

    def __init__(self):
        self._person_seq = 1000
        self._measurement_seq = 50000

    def transform_patient(self, patient: FHIRPatient) -> OMOPPerson:
        """Converts FHIR Patient to OMOP Person record."""
        self._person_seq += 1
        gender_code = patient.gender.lower() if patient.gender else "unknown"
        concept_id = self.GENDER_CONCEPT_MAP.get(gender_code, 8551)
        
        yob = 1980
        mob = None
        dob = None
        if patient.birthDate:
            parts = patient.birthDate.split("-")
            if len(parts) >= 1:
                yob = int(parts[0])
            if len(parts) >= 2:
                mob = int(parts[1])
            if len(parts) >= 3:
                dob = int(parts[2])

        return OMOPPerson(
            person_id=self._person_seq,
            gender_concept_id=concept_id,
            year_of_birth=yob,
            month_of_birth=mob,
            day_of_birth=dob,
            birth_datetime=f"{patient.birthDate}T00:00:00Z" if patient.birthDate else None,
            race_concept_id=0,
            ethnicity_concept_id=0,
            location_id=None,
            provider_id=None,
            care_site_id=None,
            person_source_value=patient.id,
            gender_source_value=gender_code,
        )

    def transform_observation(self, obs: FHIRObservation, person_id: int) -> OMOPMeasurement:
        """Converts FHIR Observation to OMOP Measurement record."""
        self._measurement_seq += 1
        loinc_code = ""
        display = ""
        for c in obs.code.coding:
            if c.system and "loinc" in c.system.lower() and c.code:
                loinc_code = c.code
                display = c.display or ""
                break

        concept_id = self.LOINC_TO_CONCEPT_MAP.get(loinc_code, 0)
        val = obs.valueQuantity.value if obs.valueQuantity else None
        unit = obs.valueQuantity.unit if obs.valueQuantity else None
        obs_date = obs.effectiveDateTime[:10] if obs.effectiveDateTime else datetime.utcnow().strftime("%Y-%m-%d")

        return OMOPMeasurement(
            measurement_id=self._measurement_seq,
            person_id=person_id,
            measurement_concept_id=concept_id,
            measurement_date=obs_date,
            measurement_datetime=obs.effectiveDateTime,
            measurement_type_concept_id=44818701,  # Lab result
            operator_concept_id=4172703,           # Equals
            value_as_number=val,
            value_as_concept_id=None,
            unit_concept_id=0,
            range_low=None,
            range_high=None,
            measurement_source_value=f"{loinc_code}:{display}",
            unit_source_value=unit,
        )
