"""
HealthPulse AI — Differential Privacy Noise Injection & Budget Accounting.
Implements Laplace and Gaussian mechanisms to enable privacy-preserving clinical population analytics.
"""

import math
import random
from typing import List, Dict, Any, Tuple


def add_laplace_noise(value: float, sensitivity: float, epsilon: float) -> float:
    """
    Laplace Mechanism: Adds noise drawn from Lap(0, sensitivity / epsilon).
    Guarantees pure epsilon-differential privacy.
    """
    scale = sensitivity / max(1e-6, epsilon)
    # Inverse CDF sampling for Laplace distribution
    u = random.uniform(-0.5, 0.5)
    sign = 1 if u >= 0 else -1
    noise = -scale * sign * math.log(1.0 - 2.0 * abs(u) + 1e-12)
    return round(value + noise, 4)


def add_gaussian_noise(value: float, sensitivity: float, epsilon: float, delta: float) -> float:
    """
    Gaussian Mechanism: Adds noise drawn from N(0, sigma^2) where:
    sigma = (sensitivity * sqrt(2 * ln(1.25 / delta))) / epsilon
    Guarantees (epsilon, delta)-differential privacy.
    """
    sigma = (sensitivity * math.sqrt(2.0 * math.log(1.25 / max(1e-9, delta)))) / max(1e-6, epsilon)
    # Box-Muller transform for standard normal sampling
    u1 = max(1e-12, random.random())
    u2 = random.random()
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    noise = sigma * z0
    return round(value + noise, 4)


class DifferentialPrivacyEngine:
    """Tracks privacy budgets across clinical research cohort queries."""

    def __init__(self, total_epsilon: float = 10.0, total_delta: float = 1e-4):
        self.total_epsilon = total_epsilon
        self.total_delta = total_delta
        self.spent_epsilon = 0.0
        self.spent_delta = 0.0
        self.query_history: List[Dict[str, Any]] = []

    def can_execute_query(self, query_epsilon: float, query_delta: float = 0.0) -> bool:
        return (self.spent_epsilon + query_epsilon) <= self.total_epsilon

    def execute_private_count(self, true_count: int, epsilon: float = 0.5) -> int:
        """Executes differentially private count query (sensitivity = 1)."""
        if not self.can_execute_query(epsilon):
            raise ValueError("Differential privacy budget exhausted for this research session")

        noisy_count = add_laplace_noise(float(true_count), sensitivity=1.0, epsilon=epsilon)
        self.spent_epsilon += epsilon
        self.query_history.append({"type": "count", "eps": epsilon, "true": true_count, "noisy": max(0, int(round(noisy_count)))})

        return max(0, int(round(noisy_count)))

    def execute_private_mean(
        self,
        values: List[float],
        lower_bound: float,
        upper_bound: float,
        epsilon: float = 0.5,
    ) -> float:
        """Differentially private bounded mean query."""
        if not self.can_execute_query(epsilon):
            raise ValueError("Differential privacy budget exhausted")

        # Clip values to [lower_bound, upper_bound]
        n = max(1, len(values))
        clipped = [max(lower_bound, min(upper_bound, v)) for v in values]
        true_sum = sum(clipped)
        
        # Sensitivity of sum is (upper - lower)
        sensitivity = upper_bound - lower_bound
        noisy_sum = add_laplace_noise(true_sum, sensitivity=sensitivity, epsilon=epsilon)
        
        self.spent_epsilon += epsilon
        return round(noisy_sum / n, 2)
