"""
HealthPulse AI — Main Python Client SDK Interface.
"""

from typing import Optional
from sdk.python.ehr_client import EHRClient
from sdk.python.clinical_client import ClinicalClient
from sdk.python.imaging_client import ImagingClient
from sdk.python.genomics_client import GenomicsClient
from sdk.python.governance_client import GovernanceClient


class HealthPulseClient:
    """Enterprise client for connecting to HealthPulse AI platform."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: Optional[str] = None,
        timeout_seconds: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout_seconds

        self.ehr = EHRClient(self)
        self.clinical = ClinicalClient(self)
        self.imaging = ImagingClient(self)
        self.genomics = GenomicsClient(self)
        self.governance = GovernanceClient(self)
