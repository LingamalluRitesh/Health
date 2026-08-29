"""
HealthPulse AI — Multi-Hospital Federated Learning and Privacy-Preserving AI Module.
Provides FedAvg, FedProx algorithms, Renyi differential privacy accounting, and secure multi-party aggregation.
"""

from backend.federated.orchestrator import (
    FederatedOrchestrator,
    HospitalClientNode,
    FederatedRoundResult,
)
from backend.federated.privacy_accountant import (
    RenyiDPAccountant,
    PrivacyLossSummary,
)
from backend.federated.secure_aggregation import (
    SecureAggregator,
    MaskedClientUpdate,
)

__all__ = [
    "FederatedOrchestrator",
    "HospitalClientNode",
    "FederatedRoundResult",
    "RenyiDPAccountant",
    "PrivacyLossSummary",
    "SecureAggregator",
    "MaskedClientUpdate",
]
