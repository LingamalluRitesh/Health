"""
Clinical Analytics & Longitudinal Vital Signs Trends API Routes.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from backend.analytics.longitudinal_record import (
    LongitudinalRecordAggregator,
    VitalReading,
    LongitudinalSummary,
)

router = APIRouter()


class VitalReadingInput(BaseModel):
    timestamp: str = Field(..., example="2026-08-29T10:00:00Z")
    systolic_bp: Optional[float] = Field(None, example=120.0)
    diastolic_bp: Optional[float] = Field(None, example=80.0)
    heart_rate: Optional[float] = Field(None, example=72.0)
    respiratory_rate: Optional[float] = Field(None, example=16.0)
    temperature_c: Optional[float] = Field(None, example=37.0)
    spo2: Optional[float] = Field(None, example=98.5)
    glucose_mg_dl: Optional[float] = Field(None, example=105.0)


class LongitudinalAnalysisRequest(BaseModel):
    patient_id: str = Field(..., example="PAT-99201")
    readings: List[VitalReadingInput]


@router.post("/longitudinal-summary", summary="Analyze Longitudinal Vital Trends")
async def analyze_longitudinal_vitals(request: LongitudinalAnalysisRequest) -> Dict[str, Any]:
    if not request.readings:
        raise HTTPException(status_code=400, detail="At least one vital reading is required.")

    aggregator = LongitudinalRecordAggregator(patient_id=request.patient_id)
    for r in request.readings:
        aggregator.add_reading(
            VitalReading(
                timestamp=r.timestamp,
                systolic_bp=r.systolic_bp,
                diastolic_bp=r.diastolic_bp,
                heart_rate=r.heart_rate,
                respiratory_rate=r.respiratory_rate,
                temperature_c=r.temperature_c,
                spo2=r.spo2,
                glucose_mg_dl=r.glucose_mg_dl,
            )
        )

    summary = aggregator.analyze()
    return {
        "patient_id": summary.patient_id,
        "total_readings": summary.total_readings,
        "first_recorded": summary.first_recorded,
        "last_recorded": summary.last_recorded,
        "mean_arterial_pressure_latest": summary.mean_arterial_pressure_latest,
        "shock_index_latest": summary.shock_index_latest,
        "pulse_pressure_latest": summary.pulse_pressure_latest,
        "vital_trajectories": summary.vital_trajectories,
        "clinical_flags": summary.clinical_flags,
    }
