"""
HealthPulse AI — Multi-Hospital Federated Learning API Endpoints.
"""

from fastapi import APIRouter
from typing import Dict, List, Any
from pydantic import BaseModel, Field

from backend.federated.orchestrator import FederatedOrchestrator
from backend.federated.privacy_accountant import RenyiDPAccountant


router = APIRouter()
orchestrator = FederatedOrchestrator(model_dimension=8)
accountant = RenyiDPAccountant()

# Register sample hospital sites
orchestrator.register_hospital("HOSP-MAYO", "Mayo Clinic Central", patient_count=14500)
orchestrator.register_hospital("HOSP-JHU", "Johns Hopkins Hospital", patient_count=12200)
orchestrator.register_hospital("HOSP-MGH", "Mass General Brigham", patient_count=16800)


class RegisterHospitalSchema(BaseModel):
    hospital_id: str = Field(..., example="HOSP-STANFORD")
    hospital_name: str = Field(..., example="Stanford Health Care")
    patient_count: int = Field(..., example=9800)


class ExecuteRoundSchema(BaseModel):
    round_number: int = Field(..., example=1)
    client_updates: Dict[str, List[float]] = Field(
        ...,
        example={
            "HOSP-MAYO": [0.12, 0.45, -0.22, 0.81, 0.05, -0.33, 0.19, 0.44],
            "HOSP-JHU": [0.10, 0.48, -0.20, 0.79, 0.07, -0.30, 0.22, 0.41],
            "HOSP-MGH": [0.14, 0.42, -0.25, 0.83, 0.04, -0.35, 0.18, 0.46],
        }
    )


@router.post("/register-hospital")
def register_hospital(payload: RegisterHospitalSchema):
    orchestrator.register_hospital(payload.hospital_id, payload.hospital_name, payload.patient_count)
    return {"status": "registered", "hospital_id": payload.hospital_id}


@router.get("/status")
def get_federated_status():
    summary = accountant.get_privacy_spent()
    return {
        "registered_hospitals": len(orchestrator.clients),
        "hospitals": [c.__dict__ for c in orchestrator.clients.values()],
        "global_weights": orchestrator.global_weights,
        "completed_rounds": len(orchestrator.rounds_history),
        "privacy_budget": summary.__dict__,
    }


@router.post("/execute-round")
def execute_round(payload: ExecuteRoundSchema):
    res = orchestrator.execute_fedavg_round(payload.round_number, payload.client_updates)
    accountant.step(noise_multiplier=1.1, subsampling_ratio=0.05)
    return res.__dict__
