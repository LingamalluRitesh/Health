"""
HealthPulse AI — Clinical Telemetry and Metric Observability.
Maintains latency histograms, clinical alert counters, and throughput monitors.
"""

import time
from typing import Dict, Any, Optional
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MetricCounter:
    name: str
    value: int = 0
    labels: Dict[str, str] = field(default_factory=dict)

    def inc(self, amount: int = 1) -> None:
        self.value += amount


@dataclass
class LatencyHistogram:
    name: str
    counts: int = 0
    total_time_ms: float = 0.0
    min_time_ms: float = float("inf")
    max_time_ms: float = 0.0

    def observe(self, duration_ms: float) -> None:
        self.counts += 1
        self.total_time_ms += duration_ms
        if duration_ms < self.min_time_ms:
            self.min_time_ms = duration_ms
        if duration_ms > self.max_time_ms:
            self.max_time_ms = duration_ms

    @property
    def average_ms(self) -> float:
        return self.total_time_ms / self.counts if self.counts > 0 else 0.0


class ClinicalTelemetryRegistry:
    """Registry for clinical system metrics, latency timers, and alert counters."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClinicalTelemetryRegistry, cls).__new__(cls)
            cls._instance.counters = defaultdict(int)
            cls._instance.histograms = {}
        return cls._instance

    def increment_counter(self, name: str, amount: int = 1) -> None:
        self.counters[name] += amount

    def observe_latency(self, name: str, duration_ms: float) -> None:
        if name not in self.histograms:
            self.histograms[name] = LatencyHistogram(name=name)
        self.histograms[name].observe(duration_ms)

    def snapshot(self) -> Dict[str, Any]:
        """Returns JSON-serializable snapshot of all platform telemetry."""
        return {
            "counters": dict(self.counters),
            "histograms": {
                k: {
                    "count": v.counts,
                    "avg_ms": round(v.average_ms, 3),
                    "min_ms": round(v.min_time_ms, 3) if v.min_time_ms != float("inf") else 0.0,
                    "max_ms": round(v.max_time_ms, 3),
                }
                for k, v in self.histograms.items()
            },
        }


telemetry = ClinicalTelemetryRegistry()


class LatencyTimer:
    """Context manager for measuring execution time of clinical inference blocks."""

    def __init__(self, metric_name: str):
        self.metric_name = metric_name
        self.start_time: float = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.perf_counter() - self.start_time) * 1000.0
        telemetry.observe_latency(self.metric_name, duration_ms)
