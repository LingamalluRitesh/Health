"""
HealthPulse AI — Python SDK Governance and Explainability Client.
"""

from typing import Dict, List, Any
import urllib.request
import json


class GovernanceClient:
    """Client for EU AI Act Model Cards and Feature Explainability."""

    def __init__(self, root_client):
        self._root = root_client

    def get_sepsis_model_card(self) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/governance/model-card/sepsis"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HealthPulse-Python-SDK/1.0"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}

    def explain_features(self, features: Dict[str, float], predicted_risk: float = 0.8) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/governance/explain-features"
        payload = json.dumps({"features": features, "predicted_risk": predicted_risk}).encode()
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}
