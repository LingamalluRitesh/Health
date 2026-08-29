"""
SMART-on-FHIR & Interoperability API Gateway.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from backend.fhir.smart_launch import SmartConfigurationProvider, FhirBatchExporter

router = APIRouter()
smart_provider = SmartConfigurationProvider()


class BatchExportRequest(BaseModel):
    resources: List[Dict[str, Any]]
    bundle_type: str = Field("transaction", example="transaction")
    search_url: Optional[str] = Field("https://api.healthpulse.ai/fhir/r4", example="https://api.healthpulse.ai/fhir/r4")


@router.get("/.well-known/smart-configuration", summary="SMART Configuration Discovery")
async def get_smart_configuration():
    return smart_provider.get_well_known_configuration()


@router.post("/fhir/r4/bundle", summary="Generate FHIR R4 Bundle")
async def generate_fhir_bundle(request: BatchExportRequest):
    if not request.resources:
        raise HTTPException(status_code=400, detail="Resource list cannot be empty.")

    if request.bundle_type == "searchset":
        return FhirBatchExporter.create_searchset_bundle(request.resources, request.search_url or "")
    return FhirBatchExporter.create_transaction_bundle(request.resources)
