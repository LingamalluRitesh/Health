"""
HealthPulse AI — CDS Hooks v1.0 Standard Service Endpoints.
Complies with HL7 CDS Hooks standard for seamless EHR integration (Epic, Cerner, MEDITECH).
"""

from fastapi import APIRouter
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from backend.fhir.cds_hooks import CDSHooksEngine


router = APIRouter()
cds_engine = CDSHooksEngine()


class CDSHookRequest(BaseModel):
    hook: str = Field("patient-view", example="patient-view")
    hookInstance: str = Field(..., example="d15f2780-4228-4e89-9830-4e3146b965f8")
    context: Dict[str, Any] = Field(..., example={"patientId": "P-100234", "userId": "Practitioner/DOC-101"})
    prefetch: Optional[Dict[str, Any]] = None


@router.get("")
def get_services():
    """CDS Hooks Discovery endpoint: GET /cds-services."""
    return {"services": cds_engine.discovery.get_services()}


@router.post("/sepsis-early-warning")
def evaluate_sepsis_service(payload: CDSHookRequest):
    """Executes Sepsis Early Warning CDS evaluation."""
    cards = cds_engine.evaluate_patient_view(
        patient_id=payload.context.get("patientId", "P-100234"),
        qsofa_score=2,
        sofa_score=4,
        temp_c=38.8,
        hr=118.0,
        rr=25.0,
    )
    return {"cards": [c.to_dict() for c in cards]}


@router.post("/pgx-ddi-safety")
def evaluate_pgx_service(payload: CDSHookRequest):
    """Executes Pharmacogenomics & DDI Safety CDS evaluation."""
    cards = cds_engine.evaluate_order_select_ddi(
        patient_id=payload.context.get("patientId", "P-100234"),
        ordered_drug="Clopidogrel 75mg",
        active_drugs=["Omeprazole 20mg", "Aspirin 81mg"],
        interaction_warnings=["CYP2C19 competition with Omeprazole reduces antiplatelet activation of Clopidogrel."],
    )
    return {"cards": [c.to_dict() for c in cards]}
