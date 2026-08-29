"""
HealthPulse AI — Python SDK Precision Genomics Client.
"""

from typing import Dict, List, Any
import urllib.request
import json


class GenomicsClient:
    """Client for precision oncology and pharmacogenomic recommendations."""

    def __init__(self, root_client):
        self._root = root_client

    def evaluate_pgx_guideline(self, gene: str, diplotype: str, drug: str) -> Dict[str, Any]:
        url = f"{self._root.base_url}/api/v1/genomics/pgx-guideline"
        payload = json.dumps({"gene": gene, "diplotype": diplotype, "target_drug": drug}).encode()
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=self._root.timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e)}
