"""
HealthPulse AI — NLP & HIPAA Security Unit Tests.
"""

from backend.nlp.negex import NegExClassifier, is_negated
from backend.nlp.concept_extractor import ClinicalConceptExtractor
from backend.nlp.icd_coding import AutomatedICD10Coder
from backend.nlp.soap_parser import SOAPNoteParser
from backend.security.hipaa_scrubber import HIPAAScrubber, deidentify_clinical_text
from backend.security.merkle_audit import MerkleAuditTrail
from backend.security.differential_privacy import add_laplace_noise, add_gaussian_noise, DifferentialPrivacyEngine


def test_negex_negation():
    classifier = NegExClassifier()
    # Negated mention
    res1 = classifier.evaluate_sentence("Patient denies chest pain and fever.", "chest pain")
    assert res1.is_negated is True

    # Affirmed mention
    res2 = classifier.evaluate_sentence("Patient has severe acute chest pain radiating to back.", "chest pain")
    assert res2.is_negated is False


def test_concept_extraction():
    extractor = ClinicalConceptExtractor()
    text = "Patient was diagnosed with type 2 diabetes and hypertension. Started on metformin 500mg."
    entities = extractor.extract_entities(text)
    assert len(entities) >= 2
    matched_names = [e.text.lower() for e in entities]
    assert "type 2 diabetes" in matched_names
    assert "metformin" in matched_names


def test_icd10_coding():
    coder = AutomatedICD10Coder()
    matches = coder.code_diagnosis_text("Assessment: Essential hypertension and systolic heart failure")
    assert len(matches) >= 2
    codes = [m.code for m in matches]
    assert "I10" in codes
    assert "I50.20" in codes


def test_hipaa_18_identifiers_scrubbing():
    scrubber = HIPAAScrubber()
    note = "Patient Jane Doe (SSN: 000-11-2222, Phone: 617-555-0199) visited Boston on 04/15/2025."
    sanitized = scrubber.scrub_text(note).sanitized_text

    assert "000-11-2222" not in sanitized
    assert "617-555-0199" not in sanitized
    assert "[SOCIAL_SECURITY_NUMBER]" in sanitized
    assert "[TELEPHONE_NUMBER]" in sanitized


def test_merkle_audit_integrity():
    ledger = MerkleAuditTrail()
    b1 = ledger.log_event(
        actor_id="DR_SMITH",
        role="clinician",
        action="VIEW_EHR",
        resource_type="Patient",
        resource_id="P-101",
        patient_id="P-101",
    )
    b2 = ledger.log_event(
        actor_id="DR_SMITH",
        role="clinician",
        action="ORDER_MEDICATION",
        resource_type="MedicationRequest",
        resource_id="MED-505",
        patient_id="P-101",
    )

    assert len(ledger.chain) == 3
    is_valid, msg = ledger.verify_integrity()
    assert is_valid is True


def test_differential_privacy():
    engine = DifferentialPrivacyEngine(total_epsilon=5.0)
    true_count = 100
    noisy_count = engine.execute_private_count(true_count, epsilon=0.5)
    assert isinstance(noisy_count, int)
    assert engine.spent_epsilon == 0.5
