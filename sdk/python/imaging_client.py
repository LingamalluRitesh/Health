"""
HealthPulse AI — Python SDK Medical Imaging Client.
"""

from typing import Dict, List, Any, Optional
import urllib.request
import json


class ImagingClient:
    """Client for DICOM processing and quantitative radiology analytics."""

    def __init__(self, root_client):
        self._root = root_client

    def evaluate_nodule(
        self,
        max_diameter_mm: float,
        mean_hu: float,
        is_solid: bool = True,
        patient_high_risk: bool = True,
    ) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/imaging/nodule-evaluate"
        payload = json.dumps({
            "max_diameter_mm": max_diameter_mm,
            "mean_hu": mean_hu,
            "is_solid": is_solid,
            "patient_high_risk": patient_high_risk,
        }).encode()
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}
