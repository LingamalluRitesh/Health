"""
HealthPulse AI — Clinical NLP, Negation, and Medical Coding Endpoints.
"""

from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from backend.nlp.negex import NegExClassifier
from backend.nlp.concept_extractor import ClinicalConceptExtractor
from backend.nlp.icd_coding import AutomatedICD10Coder
from backend.nlp.soap_parser import SOAPNoteParser
from backend.nlp.discharge_summary import DischargeSummaryGenerator, DischargeSummaryData


router = APIRouter()
negex = NegExClassifier()
extractor = ClinicalConceptExtractor()
coder = AutomatedICD10Coder()
soap_parser = SOAPNoteParser()
discharge_gen = DischargeSummaryGenerator()


class NegExRequest(BaseModel):
    sentence: str = Field(..., example="Patient denies shortness of breath and chest pain.")
    concept: str = Field(..., example="chest pain")


class ClinicalTextRequest(BaseModel):
    text: str = Field(..., example="Assessment: Acute systolic heart failure with severe dyspnea and hypertension. Patient denies fever.")


class SOAPRequest(BaseModel):
    note_text: str = Field(..., example="SUBJECTIVE:\nPatient complains of progressive dyspnea.\nOBJECTIVE:\nBP 150/90, HR 98, SpO2 93%.\nASSESSMENT:\nAcute exacerbation of heart failure.\nPLAN:\nIV Furosemide 40mg STAT.")


@router.post("/negex-evaluate")
def evaluate_negex(payload: NegExRequest):
    res = negex.evaluate_sentence(payload.sentence, payload.concept)
    return res.__dict__


@router.post("/extract-concepts")
def extract_concepts(payload: ClinicalTextRequest):
    entities = extractor.extract_entities(payload.text)
    return {
        "text": payload.text,
        "entity_count": len(entities),
        "entities": [e.__dict__ for e in entities],
    }


@router.post("/icd10-code")
def code_icd10(payload: ClinicalTextRequest):
    matches = coder.code_diagnosis_text(payload.text)
    return {
        "text": payload.text,
        "matches": [m.__dict__ for m in matches],
    }


@router.post("/parse-soap")
def parse_soap(payload: SOAPRequest):
    res = soap_parser.parse(payload.note_text)
    return res.__dict__
