"""
HealthPulse AI — Prometheus Metrics & System Observability Engine.
Collects and exposes clinical throughput, latency, CDS Hook evaluations, and worker telemetry.
"""

from typing import Dict, Any, List
import time
from dataclasses import dataclass, field


@dataclass
class MetricCounter:
    name: str
    description: str
    value: float = 0.0

    def inc(self, amount: float = 1.0) -> None:
        self.value += amount


@dataclass
class MetricHistogram:
    name: str
    description: str
    observations: List[float] = field(default_factory=list)

    def observe(self, value: float) -> None:
        self.observations.append(value)

    @property
    def count(self) -> int:
        return len(self.observations)

    @property
    def sum(self) -> float:
        return sum(self.observations)

    @property
    def avg(self) -> float:
        return self.sum / self.count if self.count > 0 else 0.0


class ClinicalMetricsRegistry:
    """In-memory Prometheus-compatible clinical metrics collector."""

    def __init__(self):
        self.http_requests_total = MetricCounter(
            "healthpulse_http_requests_total",
            "Total count of HTTP requests served by clinical gateway",
        )
        self.cds_evaluations_total = MetricCounter(
            "healthpulse_cds_evaluations_total",
            "Total count of CDS Hooks clinical decision support evaluations",
        )
        self.critical_alarms_total = MetricCounter(
            "healthpulse_critical_alarms_total",
            "Total count of critical hemodynamic / sepsis alerts dispatched",
        )
        self.request_duration_seconds = MetricHistogram(
            "healthpulse_request_duration_seconds",
            "Histogram of clinical API request latency in seconds",
        )

    def export_prometheus_format(self) -> str:
        lines = [
            f"# HELP {self.http_requests_total.name} {self.http_requests_total.description}",
            f"# TYPE {self.http_requests_total.name} counter",
            f"{self.http_requests_total.name} {self.http_requests_total.value}",
            f"# HELP {self.cds_evaluations_total.name} {self.cds_evaluations_total.description}",
            f"# TYPE {self.cds_evaluations_total.name} counter",
            f"{self.cds_evaluations_total.name} {self.cds_evaluations_total.value}",
            f"# HELP {self.critical_alarms_total.name} {self.critical_alarms_total.description}",
            f"# TYPE {self.critical_alarms_total.name} counter",
            f"{self.critical_alarms_total.name} {self.critical_alarms_total.value}",
            f"# HELP {self.request_duration_seconds.name} {self.request_duration_seconds.description}",
            f"# TYPE {self.request_duration_seconds.name} summary",
            f"{self.request_duration_seconds.name}_count {self.request_duration_seconds.count}",
            f"{self.request_duration_seconds.name}_sum {self.request_duration_seconds.sum:.4f}",
        ]
        return "\n".join(lines) + "\n"
