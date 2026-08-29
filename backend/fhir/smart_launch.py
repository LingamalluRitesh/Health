"""
SMART-on-FHIR App Launch Protocol & FHIR R4 Batch Exporter.
Implements HL7 FHIR SMART App Launch standard configuration and batch export mechanisms.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class SmartConfigurationProvider:
    """Provides SMART-on-FHIR discovery configuration endpoints."""

    def __init__(self, base_url: str = "https://healthpulse.ai"):
        self.base_url = base_url

    def get_well_known_configuration(self) -> Dict[str, Any]:
        return {
            "issuer": self.base_url,
            "authorization_endpoint": f"{self.base_url}/oauth/authorize",
            "token_endpoint": f"{self.base_url}/oauth/token",
            "token_endpoint_auth_methods_supported": ["client_secret_basic", "private_key_jwt"],
            "grant_types_supported": ["authorization_code", "refresh_token", "client_credentials"],
            "registration_endpoint": f"{self.base_url}/oauth/register",
            "scopes_supported": [
                "openid",
                "profile",
                "launch",
                "launch/patient",
                "patient/*.read",
                "user/*.read",
                "offline_access",
            ],
            "response_types_supported": ["code"],
            "management_endpoint": f"{self.base_url}/oauth/manage",
            "introspection_endpoint": f"{self.base_url}/oauth/introspect",
            "revocation_endpoint": f"{self.base_url}/oauth/revoke",
            "code_challenge_methods_supported": ["S256"],
            "capabilities": [
                "launch-ehr",
                "launch-standalone",
                "client-public",
                "client-confidential-symmetric",
                "context-ehr-patient",
                "permission-patient",
                "permission-user",
            ],
        }


class FhirBatchExporter:
    """Packages multiple FHIR resources into a FHIR R4 Bundle for interoperability export."""

    @staticmethod
    def create_transaction_bundle(resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        entries = []
        for res in resources:
            res_type = res.get("resourceType", "Resource")
            res_id = res.get("id", "temp-id")
            entries.append({
                "fullUrl": f"urn:uuid:{res_id}",
                "resource": res,
                "request": {
                    "method": "POST",
                    "url": res_type,
                },
            })

        return {
            "resourceType": "Bundle",
            "type": "transaction",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total": len(entries),
            "entry": entries,
        }

    @staticmethod
    def create_searchset_bundle(resources: List[Dict[str, Any]], search_url: str) -> Dict[str, Any]:
        entries = []
        for res in resources:
            res_id = res.get("id", "res-id")
            res_type = res.get("resourceType", "Resource")
            entries.append({
                "fullUrl": f"{search_url}/{res_type}/{res_id}",
                "resource": res,
                "search": {"mode": "match"},
            })

        return {
            "resourceType": "Bundle",
            "type": "searchset",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total": len(entries),
            "link": [{"relation": "self", "url": search_url}],
            "entry": entries,
        }
