import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.core.observability import ClinicalMetricsRegistry

client = TestClient(app)


def test_metrics_registry():
    registry = ClinicalMetricsRegistry()
    registry.http_requests_total.inc(5)
    registry.cds_evaluations_total.inc(3)
    registry.critical_alarms_total.inc(1)
    registry.request_duration_seconds.observe(0.045)
    registry.request_duration_seconds.observe(0.055)

    prom_text = registry.export_prometheus_format()
    assert "healthpulse_http_requests_total 5.0" in prom_text
    assert "healthpulse_cds_evaluations_total 3.0" in prom_text
    assert "healthpulse_critical_alarms_total 1.0" in prom_text
    assert "healthpulse_request_duration_seconds_count 2" in prom_text


def test_metrics_endpoint():
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "healthpulse_http_requests_total" in res.text
