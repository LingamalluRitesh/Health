import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.security.emergency_access import BreakGlassSecurityManager

client = TestClient(app)


def test_break_glass_manager_lifecycle():
    mgr = BreakGlassSecurityManager()
    with pytest.raises(ValueError):
        mgr.request_emergency_access("DOC-1", "DOCTOR", "PAT-1", "Too short")

    session = mgr.request_emergency_access(
        user_id="DOC-1",
        user_role="CRITICAL_CARE_FELLOW",
        patient_id="PAT-991",
        clinical_justification="Patient undergoing emergency bedside thoracotomy.",
        duration_minutes=30,
    )
    assert session.session_id.startswith("BG-")
    assert session.is_active is True
    assert mgr.verify_emergency_access(session.session_id, session.cryptographic_token) is True
    assert mgr.verify_emergency_access(session.session_id, "invalid_token") is False

    mgr.revoke_emergency_access(session.session_id)
    assert mgr.verify_emergency_access(session.session_id, session.cryptographic_token) is False


def test_break_glass_api_flow():
    req_body = {
        "user_id": "PRACTITIONER-009",
        "user_role": "SURGEON",
        "patient_id": "PAT-4040",
        "clinical_justification": "Urgent neurosurgical consultation for acute subdural hematoma.",
        "duration_minutes": 45,
    }
    res = client.post("/api/v1/emergency-access/request", json=req_body)
    assert res.status_code == 200
    data = res.json()
    assert "session_id" in data
    assert "cryptographic_token" in data

    ver_res = client.post(
        "/api/v1/emergency-access/verify",
        json={"session_id": data["session_id"], "token": data["cryptographic_token"]},
    )
    assert ver_res.status_code == 200
    assert ver_res.json()["valid"] is True
