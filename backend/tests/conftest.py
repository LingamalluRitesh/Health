"""
HealthPulse AI — Pytest Fixtures and Environment Configuration.
"""

import pytest
from datetime import datetime
from backend.core.types import PatientVitalSigns


@pytest.fixture
def sample_icu_vitals():
    return PatientVitalSigns(
        patient_id="P-TEST-001",
        timestamp=datetime.utcnow(),
        heart_rate=112.0,
        respiratory_rate=26.0,
        systolic_bp=88.0,
        diastolic_bp=55.0,
        oxygen_saturation=93.0,
        temperature_celsius=38.9,
        gcs_score=13.0,
        fio2=0.40,
        pao2=75.0,
        platelets=95.0,
        bilirubin=2.2,
        creatinine=2.1,
        urine_output_24h=400.0,
        on_vasopressors=True,
    )
