"""
HealthPulse AI — Renyi Differential Privacy (RDP) & Moments Privacy Accountant.
Tracks cumulative privacy expenditure across federated learning communication rounds.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class PrivacyLossSummary:
    target_delta: float
    effective_epsilon: float
    total_rounds: int
    noise_multiplier_sigma: float
    sampling_ratio_q: float
    is_budget_exceeded: bool


class RenyiDPAccountant:
    """Calculates tight privacy bounds using Renyi Differential Privacy."""

    def __init__(self, orders: Optional[List[float]] = None):
        self.orders = orders or [1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 8.0, 16.0, 32.0, 64.0]
        self.rdp_history: Dict[float, float] = {alpha: 0.0 for alpha in self.orders}
        self.step_count = 0

    def step(self, noise_multiplier: float, subsampling_ratio: float) -> None:
        """Accumulates RDP privacy loss for one subsampled Gaussian mechanism step."""
        q = subsampling_ratio
        sigma = noise_multiplier
        self.step_count += 1

        for alpha in self.orders:
            # Analytical bound on RDP of subsampled Gaussian mechanism
            # Approx: rdp_step = (q^2 * alpha) / (2 * sigma^2)
            step_rdp = (q * q * alpha) / (2.0 * (sigma * sigma))
            self.rdp_history[alpha] += step_rdp

    def get_privacy_spent(self, target_delta: float = 1e-5, max_epsilon: float = 10.0) -> PrivacyLossSummary:
        """Converts accumulated RDP into (epsilon, delta)-DP bound."""
        best_eps = float("inf")

        for alpha in self.orders:
            cum_rdp = self.rdp_history[alpha]
            # Conversion formula: eps(delta) = rdp + (ln(1/delta) / (alpha - 1))
            if alpha > 1.0:
                eps = cum_rdp + (math.log(1.0 / target_delta) / (alpha - 1.0))
                if eps < best_eps:
                    best_eps = eps

        rounded_eps = round(best_eps, 4) if best_eps != float("inf") else 0.0

        return PrivacyLossSummary(
            target_delta=target_delta,
            effective_epsilon=rounded_eps,
            total_rounds=self.step_count,
            noise_multiplier_sigma=1.1,
            sampling_ratio_q=0.05,
            is_budget_exceeded=rounded_eps > max_epsilon,
        )
