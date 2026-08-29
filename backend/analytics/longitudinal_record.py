"""
Longitudinal Patient Record Aggregator & Vital Signs Analytics.
Analyzes multi-encounter clinical timelines, calculating vital trends,
physiological indices (MAP, Shock Index, Pulse Pressure), and trajectory anomalies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import math


@dataclass
class VitalReading:
    timestamp: str
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    heart_rate: Optional[float] = None
    respiratory_rate: Optional[float] = None
    temperature_c: Optional[float] = None
    spo2: Optional[float] = None
    glucose_mg_dl: Optional[float] = None


@dataclass
class LongitudinalSummary:
    patient_id: str
    total_readings: int
    first_recorded: Optional[str]
    last_recorded: Optional[str]
    mean_arterial_pressure_latest: Optional[float]
    shock_index_latest: Optional[float]
    pulse_pressure_latest: Optional[float]
    vital_trajectories: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    clinical_flags: List[str] = field(default_factory=list)


class LongitudinalRecordAggregator:
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.readings: List[VitalReading] = []

    def add_reading(self, reading: VitalReading) -> None:
        self.readings.append(reading)
        self.readings.sort(key=lambda r: r.timestamp)

    @staticmethod
    def calculate_map(systolic: float, diastolic: float) -> float:
        """Calculate Mean Arterial Pressure: DP + 1/3(SP - DP)"""
        return round(diastolic + (systolic - diastolic) / 3.0, 2)

    @staticmethod
    def calculate_shock_index(heart_rate: float, systolic: float) -> Optional[float]:
        """Calculate Shock Index: HR / Systolic BP"""
        if systolic <= 0:
            return None
        return round(heart_rate / systolic, 3)

    @staticmethod
    def calculate_pulse_pressure(systolic: float, diastolic: float) -> float:
        """Calculate Pulse Pressure: SP - DP"""
        return round(systolic - diastolic, 2)

    def _compute_trajectory(self, values: List[float]) -> Dict[str, Any]:
        if not values:
            return {"count": 0, "min": None, "max": None, "mean": None, "trend": "unknown"}
        n = len(values)
        mean_val = round(sum(values) / n, 2)
        min_val = min(values)
        max_val = max(values)

        if n < 2:
            trend = "stable"
        else:
            delta = values[-1] - values[0]
            if delta > 0.05 * mean_val:
                trend = "increasing"
            elif delta < -0.05 * mean_val:
                trend = "decreasing"
            else:
                trend = "stable"

        return {
            "count": n,
            "min": min_val,
            "max": max_val,
            "mean": mean_val,
            "latest": values[-1],
            "trend": trend,
        }

    def analyze(self) -> LongitudinalSummary:
        if not self.readings:
            return LongitudinalSummary(
                patient_id=self.patient_id,
                total_readings=0,
                first_recorded=None,
                last_recorded=None,
                mean_arterial_pressure_latest=None,
                shock_index_latest=None,
                pulse_pressure_latest=None,
            )

        sbp_list = [r.systolic_bp for r in self.readings if r.systolic_bp is not None]
        dbp_list = [r.diastolic_bp for r in self.readings if r.diastolic_bp is not None]
        hr_list = [r.heart_rate for r in self.readings if r.heart_rate is not None]
        spo2_list = [r.spo2 for r in self.readings if r.spo2 is not None]
        temp_list = [r.temperature_c for r in self.readings if r.temperature_c is not None]

        trajectories = {
            "systolic_bp": self._compute_trajectory(sbp_list),
            "diastolic_bp": self._compute_trajectory(dbp_list),
            "heart_rate": self._compute_trajectory(hr_list),
            "spo2": self._compute_trajectory(spo2_list),
            "temperature_c": self._compute_trajectory(temp_list),
        }

        latest = self.readings[-1]
        latest_map = None
        latest_si = None
        latest_pp = None

        if latest.systolic_bp is not None and latest.diastolic_bp is not None:
            latest_map = self.calculate_map(latest.systolic_bp, latest.diastolic_bp)
            latest_pp = self.calculate_pulse_pressure(latest.systolic_bp, latest.diastolic_bp)

        if latest.heart_rate is not None and latest.systolic_bp is not None:
            latest_si = self.calculate_shock_index(latest.heart_rate, latest.systolic_bp)

        flags = []
        if latest_si and latest_si >= 0.9:
            flags.append("ELEVATED_SHOCK_INDEX_HEMODYNAMIC_INSTABILITY")
        if latest_map and latest_map < 65.0:
            flags.append("HYPOTENSION_MAP_CRITICAL")
        if latest.spo2 and latest.spo2 < 92.0:
            flags.append("HYPOXIA_SPO2_SUBOPTIMAL")
        if latest.temperature_c and latest.temperature_c >= 38.3:
            flags.append("FEBRILE_EPISODE")

        return LongitudinalSummary(
            patient_id=self.patient_id,
            total_readings=len(self.readings),
            first_recorded=self.readings[0].timestamp,
            last_recorded=self.readings[-1].timestamp,
            mean_arterial_pressure_latest=latest_map,
            shock_index_latest=latest_si,
            pulse_pressure_latest=latest_pp,
            vital_trajectories=trajectories,
            clinical_flags=flags,
        )
