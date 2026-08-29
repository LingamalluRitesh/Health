"""
HealthPulse AI — Clinical Covariate Shift and Population Stability Drift Monitor.
Calculates Population Stability Index (PSI) and Wasserstein divergence over physiological vital sign streams.
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import math


@dataclass
class DriftReport:
    feature_name: str
    psi_score: float
    drift_status: str  # NO_DRIFT, MODERATE_DRIFT, SEVERE_DRIFT
    baseline_mean: float
    current_mean: float
    baseline_std: float
    current_std: float
    requires_retraining: bool


class ClinicalDataDriftMonitor:
    """Monitors incoming telemetry and EHR variables against baseline distribution."""

    @staticmethod
    def _mean_std(values: List[float]) -> Tuple[float, float]:
        if not values:
            return 0.0, 0.0
        n = len(values)
        m = sum(values) / n
        var = sum((x - m) ** 2 for x in values) / max(1, n - 1)
        return round(m, 3), round(math.sqrt(var), 3)

    def calculate_psi(
        self,
        baseline_values: List[float],
        current_values: List[float],
        num_buckets: int = 10,
    ) -> float:
        """
        Population Stability Index (PSI):
        PSI = sum((Actual% - Expected%) * ln(Actual% / Expected%))
        - PSI < 0.10: No significant distribution change
        - 0.10 <= PSI < 0.25: Moderate shift
        - PSI >= 0.25: Severe covariate shift / model drift
        """
        if not baseline_values or not current_values:
            return 0.0

        min_val = min(min(baseline_values), min(current_values))
        max_val = max(max(baseline_values), max(current_values))

        if min_val == max_val:
            return 0.0

        step = (max_val - min_val) / num_buckets
        eps = 1e-4

        psi_total = 0.0
        n_base = len(baseline_values)
        n_curr = len(current_values)

        for b in range(num_buckets):
            b_low = min_val + b * step
            b_high = min_val + (b + 1) * step if b < (num_buckets - 1) else max_val + 1e-6

            count_base = sum(1 for x in baseline_values if b_low <= x < b_high)
            count_curr = sum(1 for x in current_values if b_low <= x < b_high)

            pct_base = max(eps, count_base / n_base)
            pct_curr = max(eps, count_curr / n_curr)

            bucket_psi = (pct_curr - pct_base) * math.log(pct_curr / pct_base)
            psi_total += bucket_psi

        return round(psi_total, 4)

    def evaluate_feature_drift(
        self,
        feature_name: str,
        baseline_values: List[float],
        current_values: List[float],
    ) -> DriftReport:
        psi = self.calculate_psi(baseline_values, current_values)
        b_mean, b_std = self._mean_std(baseline_values)
        c_mean, c_std = self._mean_std(current_values)

        if psi < 0.10:
            status = "NO_DRIFT"
            retrain = False
        elif psi < 0.25:
            status = "MODERATE_DRIFT"
            retrain = False
        else:
            status = "SEVERE_DRIFT"
            retrain = True

        return DriftReport(
            feature_name=feature_name,
            psi_score=psi,
            drift_status=status,
            baseline_mean=b_mean,
            current_mean=c_mean,
            baseline_std=b_std,
            current_std=c_std,
            requires_retraining=retrain,
        )
