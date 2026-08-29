"""
HealthPulse AI — Secure Multi-Party Aggregation (SecAgg) Protocol.
Simulates pairwise random masking so the central server only observes the true sum of weights without inspecting individual hospital updates.
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import random


@dataclass
class MaskedClientUpdate:
    hospital_id: str
    masked_weights: List[float]


class SecureAggregator:
    """Simulates Bonawitz et al. Practical Secure Aggregation Protocol."""

    def __init__(self, dimension: int):
        self.dimension = dimension

    def generate_pairwise_masks(self, hospital_ids: List[str]) -> Dict[str, List[float]]:
        """Generates canceling symmetric noise masks between all participating hospital pairs."""
        masks = {hid: [0.0] * self.dimension for hid in hospital_ids}

        for i in range(len(hospital_ids)):
            for j in range(i + 1, len(hospital_ids)):
                h_a = hospital_ids[i]
                h_b = hospital_ids[j]

                # Generate shared random vector s_{u,v}
                shared_seed = [random.uniform(-1.0, 1.0) for _ in range(self.dimension)]
                
                # Add +s to h_a and -s to h_b
                for d in range(self.dimension):
                    masks[h_a][d] += shared_seed[d]
                    masks[h_b][d] -= shared_seed[d]

        return masks

    def aggregate_masked_updates(
        self,
        masked_updates: List[MaskedClientUpdate],
    ) -> List[float]:
        """Server aggregates masked weights: all pairwise noise terms algebraically sum to zero."""
        n = len(masked_updates)
        if n == 0:
            return [0.0] * self.dimension

        summed = [0.0] * self.dimension
        for up in masked_updates:
            for d in range(self.dimension):
                summed[d] += up.masked_weights[d]

        return [round(val / n, 6) for val in summed]
