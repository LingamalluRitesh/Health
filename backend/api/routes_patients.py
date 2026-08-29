"""
HealthPulse AI — Patients & Longitudinal EHR API Endpoints.
Provides CRUD operations, vital sign tracking, lab histories, medication regimens, and alerts.
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from backend.core.database import db_store
from backend.core.types import PatientVitalSigns, ClinicalLabResult, MedicationOrder, ClinicalAlert, AlertType, ClinicalSeverity
from backend.security.merkle_audit import audit_ledger


router = APIRouter()


class PatientRegistrationSchema(BaseModel):
    patient_id: str = Field(..., example="P-100234")
    name: str = Field(..., example="Eleanor Vance")
    gender: str = Field(..., example="female")
    birth_date: str = Field(..., example="1968-04-12")
    mrn: str = Field(..., example="MRN-882319")
    department: str = Field("ICU-East", example="ICU-East")
    bed_number: str = Field("BED-04", example="BED-04")
    primary_diagnosis: Optional[str] = "Sepsis secondary to acute pyelonephritis"


class VitalSignInputSchema(BaseModel):
    heart_rate: float = Field(..., example=98.0)
    respiratory_rate: float = Field(..., example=24.0)
    systolic_bp: float = Field(..., example=95.0)
    diastolic_bp: float = Field(..., example=60.0)
    oxygen_saturation: float = Field(..., example=94.0)
    temperature_celsius: float = Field(..., example=38.6)
    gcs_score: Optional[float] = 14.0
    fio2: Optional[float] = 0.40
    pao2: Optional[float] = 85.0
    serum_creatinine: Optional[float] = 1.8
    serum_lactate: Optional[float] = 2.4
    platelets: Optional[float] = 110.0
    bilirubin: Optional[float] = 1.4
    on_vasopressors: Optional[bool] = False
    on_mechanical_ventilation: Optional[bool] = False


@router.post("/register")
async def register_patient(payload: PatientRegistrationSchema):
    data = payload.dict()
    await db_store.register_patient(payload.patient_id, data)
    
    audit_ledger.log_event(
        actor_id="CLINICIAN-01",
        role="clinician",
        action="PATIENT_REGISTER",
        resource_type="Patient",
        resource_id=payload.patient_id,
        patient_id=payload.patient_id,
        payload_data=data,
    )
    return {"status": "success", "patient_id": payload.patient_id, "message": "Patient registered successfully"}


@router.get("")
async def list_patients(limit: int = Query(50), offset: int = Query(0)):
    pts = await db_store.list_patients(limit=limit, offset=offset)
    if not pts:
        # Provide sample default cohort if empty
        default_pts = [
            {
                "patient_id": "P-100234",
                "name": "Eleanor Vance",
                "gender": "female",
                "birth_date": "1968-04-12",
                "mrn": "MRN-882319",
                "department": "ICU-East",
                "bed_number": "BED-04",
                "primary_diagnosis": "Sepsis secondary to acute pyelonephritis",
            },
            {
                "patient_id": "P-100235",
                "name": "Marcus Bennett",
                "gender": "male",
                "birth_date": "1954-11-23",
                "mrn": "MRN-773192",
                "department": "Cardiology Step-Down",
                "bed_number": "BED-12",
                "primary_diagnosis": "Acute decompensated heart failure with AFib",
            },
        ]
        for p in default_pts:
            await db_store.register_patient(p["patient_id"], p)
        pts = default_pts

    return {"total": len(pts), "patients": pts}


@router.get("/{patient_id}")
async def get_patient_profile(patient_id: str):
    pt = await db_store.get_patient(patient_id)
    if not pt:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    vitals = await db_store.get_latest_vitals(patient_id)
    labs = await db_store.get_lab_results(patient_id)
    meds = await db_store.get_active_medications(patient_id)
    alerts = await db_store.get_active_alerts(patient_id)

    return {
        "patient": pt,
        "latest_vitals": vitals,
        "active_medications": meds,
        "recent_labs": labs,
        "active_alerts": alerts,
    }


@router.post("/{patient_id}/vitals")
async def record_vitals(patient_id: str, payload: VitalSignInputSchema):
    vitals = PatientVitalSigns(
        patient_id=patient_id,
        timestamp=datetime.utcnow(),
        heart_rate=payload.heart_rate,
        respiratory_rate=payload.respiratory_rate,
        systolic_bp=payload.systolic_bp,
        diastolic_bp=payload.diastolic_bp,
        oxygen_saturation=payload.oxygen_saturation,
        temperature_celsius=payload.temperature_celsius,
        gcs_score=payload.gcs_score,
        fio2=payload.fio2,
        pao2=payload.pao2,
        platelets=payload.platelets,
        bilirubin=payload.bilirubin,
        creatinine=payload.serum_creatinine,
        on_vasopressors=payload.on_vasopressors or False,
        on_mechanical_ventilation=payload.on_mechanical_ventilation or False,
    )
    await db_store.add_vitals(vitals)
    return {"status": "success", "recorded_at": vitals.timestamp.isoformat()}


@router.get("/{patient_id}/vitals/history")
async def get_vitals_history(patient_id: str, limit: int = Query(50)):
    records = await db_store.get_vitals_history(patient_id, limit=limit)
    return {"patient_id": patient_id, "count": len(records), "history": records}
