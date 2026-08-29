"""
HealthPulse AI — FHIR R4 & HL7 v2 Unit Tests.
"""

from backend.fhir.models import FHIRPatient, FHIRObservation, FHIRCodeableConcept, FHIRCoding, FHIRQuantity
from backend.fhir.serializer import parse_fhir_resource, create_observation
from backend.fhir.hl7_parser import parse_hl7_v2
from backend.fhir.hl7_serializer import build_adt_a01, build_oru_r01
from backend.fhir.omop_cdm import OMOPTransformer


def test_fhir_patient_serialization():
    patient = FHIRPatient(
        id="pt-101",
        active=True,
        gender="male",
        birthDate="1980-05-15",
    )
    d = patient.to_dict()
    assert d["resourceType"] == "Patient"
    assert d["id"] == "pt-101"
    assert d["gender"] == "male"


def test_fhir_observation_builder():
    obs = create_observation(
        patient_id="pt-101",
        code="8867-4",
        display="Heart rate",
        value=78.0,
        unit="bpm",
    )
    d = obs.to_dict()
    assert d["resourceType"] == "Observation"
    assert d["valueQuantity"]["value"] == 78.0


def test_hl7_v2_generation_and_parsing():
    raw_msg = build_adt_a01(
        patient_id="P12345",
        first_name="Jane",
        last_name="Doe",
        dob="19750820",
        gender="female",
    )
    assert raw_msg.startswith("MSH")
    assert "P12345" in raw_msg

    parsed = parse_hl7_v2(raw_msg)
    assert parsed.message_type == "ADT"
    assert parsed.trigger_event == "A01"
    
    pid_seg = parsed.get_first_segment("PID")
    assert pid_seg is not None
    assert pid_seg.get_component(3, 1) == "P12345"


def test_omop_cdm_transformation():
    transformer = OMOPTransformer()
    patient = FHIRPatient(id="P-OMOP-01", gender="female", birthDate="1992-04-10")
    person = transformer.transform_patient(patient)

    assert person.gender_concept_id == 8532  # Female OMOP ID
    assert person.year_of_birth == 1992
    assert person.person_source_value == "P-OMOP-01"
