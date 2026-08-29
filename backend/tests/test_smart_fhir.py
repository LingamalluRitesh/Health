import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.fhir.smart_launch import SmartConfigurationProvider, FhirBatchExporter

client = TestClient(app)


def test_smart_configuration_discovery():
    provider = SmartConfigurationProvider(base_url="https://healthpulse.local")
    config = provider.get_well_known_configuration()
    assert config["issuer"] == "https://healthpulse.local"
    assert "launch/patient" in config["scopes_supported"]
    assert "S256" in config["code_challenge_methods_supported"]


def test_fhir_batch_exporter():
    resources = [
        {"resourceType": "Patient", "id": "p1", "name": [{"family": "Doe"}]},
        {"resourceType": "Observation", "id": "obs1", "status": "final"},
    ]
    bundle = FhirBatchExporter.create_transaction_bundle(resources)
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "transaction"
    assert bundle["total"] == 2
    assert len(bundle["entry"]) == 2


def test_smart_fhir_routes():
    res = client.get("/api/v1/smart/.well-known/smart-configuration")
    assert res.status_code == 200
    assert "authorization_endpoint" in res.json()

    bundle_res = client.post(
        "/api/v1/smart/fhir/r4/bundle",
        json={
            "bundle_type": "transaction",
            "resources": [{"resourceType": "Condition", "id": "cond-1"}],
        },
    )
    assert bundle_res.status_code == 200
    assert bundle_res.json()["resourceType"] == "Bundle"
