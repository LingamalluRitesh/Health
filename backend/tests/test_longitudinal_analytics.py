import pytest
from backend.analytics.longitudinal_record import (
    LongitudinalRecordAggregator,
    VitalReading,
)
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)


def test_longitudinal_record_metrics_calculation():
    aggregator = LongitudinalRecordAggregator(patient_id="PAT-001")
    aggregator.add_reading(
        VitalReading(
            timestamp="2026-08-29T08:00:00Z",
            systolic_bp=120.0,
            diastolic_bp=80.0,
            heart_rate=70.0,
            spo2=98.0,
            temperature_c=36.8,
        )
    )
    aggregator.add_reading(
        VitalReading(
            timestamp="2026-08-29T12:00:00Z",
            systolic_bp=85.0,
            diastolic_bp=55.0,
            heart_rate=115.0,
            spo2=90.0,
            temperature_c=38.6,
        )
    )

    summary = aggregator.analyze()
    assert summary.patient_id == "PAT-001"
    assert summary.total_readings == 2
    assert summary.mean_arterial_pressure_latest == 65.0
    assert summary.shock_index_latest == round(115.0 / 85.0, 3)
    assert summary.pulse_pressure_latest == 30.0
    assert "ELEVATED_SHOCK_INDEX_HEMODYNAMIC_INSTABILITY" in summary.clinical_flags
    assert "HYPOXIA_SPO2_SUBOPTIMAL" in summary.clinical_flags
    assert "FEBRILE_EPISODE" in summary.clinical_flags


def test_longitudinal_api_endpoint():
    payload = {
        "patient_id": "PAT-002",
        "readings": [
            {
                "timestamp": "2026-08-29T06:00:00Z",
                "systolic_bp": 130.0,
                "diastolic_bp": 85.0,
                "heart_rate": 75.0,
                "spo2": 99.0,
                "temperature_c": 37.0,
            },
            {
                "timestamp": "2026-08-29T10:00:00Z",
                "systolic_bp": 125.0,
                "diastolic_bp": 82.0,
                "heart_rate": 78.0,
                "spo2": 98.0,
                "temperature_c": 37.1,
            },
        ],
    }
    response = client.post("/api/v1/analytics/longitudinal-summary", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "PAT-002"
    assert data["total_readings"] == 2
    assert "vital_trajectories" in data
