"""
HealthPulse AI — Python SDK Clinical Risk Calculators Client.
"""

from typing import Dict, List, Any, Optional
import urllib.request
import json


class ClinicalClient:
    """Client for evaluating evidence-based risk algorithms."""

    def __init__(self, root_client):
        self._root = root_client

    def calculate_qsofa(self, respiratory_rate: float, gcs_score: float, systolic_bp: float) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/clinical/qsofa"
        payload = json.dumps({"respiratory_rate": respiratory_rate, "gcs_score": gcs_score, "systolic_bp": systolic_bp}).encode()
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}

    def check_drug_interactions(self, medications: List[str]) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/clinical/ddi-check"
        payload = json.dumps({"medications": medications}).encode()
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}
