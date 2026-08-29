"""
HealthPulse AI — Python SDK Patient EHR Client.
"""

from typing import Dict, List, Any, Optional
import urllib.request
import json


class EHRClient:
    """Client for Patient records and longitudinal EHR data."""

    def __init__(self, root_client):
        self._root = root_client

    def list_patients(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/patients?limit={limit}&offset={offset}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HealthPulse-Python-SDK/1.0"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return {"total": 0, "patients": []}

    def get_patient(self, patient_id: str) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/patients/{patient_id}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HealthPulse-Python-SDK/1.0"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception:
            return {"error": "Failed to connect to HealthPulse API"}
