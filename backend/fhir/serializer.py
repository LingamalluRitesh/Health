"""
HealthPulse AI — FHIR Resource Validation and JSON Deserialization.
Converts raw JSON payloads into strongly-typed FHIR models and bundles.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.fhir.models import (
    FHIRResource,
    FHIRPatient,
    FHIRObservation,
    FHIRCondition,
    FHIREncounter,
    FHIRDiagnosticReport,
    FHIRMedicationRequest,
    FHIRCarePlan,
    FHIRBundle,
    FHIRCodeableConcept,
    FHIRCoding,
    FHIRIdentifier,
    FHIRReference,
    FHIRQuantity,
    FHIRHumanName,
    FHIRAddress,
)
from backend.core.exceptions import FHIRParsingException


def parse_fhir_resource(payload: Dict[str, Any]) -> FHIRResource:
    """Parses a dictionary JSON payload into a typed FHIR Resource."""
    if not isinstance(payload, dict):
        raise FHIRParsingException("Resource payload must be a JSON object")

    resource_type = payload.get("resourceType")
    if not resource_type:
        raise FHIRParsingException("Missing mandatory 'resourceType' attribute")

    res_id = payload.get("id", "")

    if resource_type == "Patient":
        identifiers = []
        for ident in payload.get("identifier", []):
            identifiers.append(FHIRIdentifier(
                use=ident.get("use"),
                system=ident.get("system"),
                value=ident.get("value"),
            ))
        
        names = []
        for name_data in payload.get("name", []):
            names.append(FHIRHumanName(
                use=name_data.get("use", "official"),
                text=name_data.get("text"),
                family=name_data.get("family"),
                given=name_data.get("given", []),
            ))

        addresses = []
        for addr in payload.get("address", []):
            addresses.append(FHIRAddress(
                use=addr.get("use", "home"),
                line=addr.get("line", []),
                city=addr.get("city"),
                state=addr.get("state"),
                postalCode=addr.get("postalCode"),
                country=addr.get("country", "USA"),
            ))

        return FHIRPatient(
            id=res_id,
            identifier=identifiers,
            active=payload.get("active", True),
            name=names,
            gender=payload.get("gender", "unknown"),
            birthDate=payload.get("birthDate"),
            deceasedBoolean=payload.get("deceasedBoolean", False),
            address=addresses,
        )

    elif resource_type == "Observation":
        code_data = payload.get("code", {})
        codings = [
            FHIRCoding(
                system=c.get("system"),
                version=c.get("version"),
                code=c.get("code"),
                display=c.get("display"),
            )
            for c in code_data.get("coding", [])
        ]
        code_concept = FHIRCodeableConcept(coding=codings, text=code_data.get("text"))

        subject = None
        if "subject" in payload:
            subject = FHIRReference(
                reference=payload["subject"].get("reference"),
                type=payload["subject"].get("type"),
                display=payload["subject"].get("display"),
            )

        val_q = None
        if "valueQuantity" in payload:
            vq = payload["valueQuantity"]
            val_q = FHIRQuantity(
                value=float(vq.get("value", 0.0)) if vq.get("value") is not None else None,
                unit=vq.get("unit"),
                system=vq.get("system"),
                code=vq.get("code"),
            )

        return FHIRObservation(
            id=res_id,
            status=payload.get("status", "final"),
            code=code_concept,
            subject=subject,
            effectiveDateTime=payload.get("effectiveDateTime"),
            valueQuantity=val_q,
            valueString=payload.get("valueString"),
        )

    elif resource_type == "Condition":
        code_data = payload.get("code", {})
        codings = [
            FHIRCoding(system=c.get("system"), code=c.get("code"), display=c.get("display"))
            for c in code_data.get("coding", [])
        ]
        return FHIRCondition(
            id=res_id,
            code=FHIRCodeableConcept(coding=codings, text=code_data.get("text")),
            onsetDateTime=payload.get("onsetDateTime"),
            recordedDate=payload.get("recordedDate"),
        )

    elif resource_type == "Bundle":
        bundle = FHIRBundle(id=res_id, type=payload.get("type", "collection"))
        for item in payload.get("entry", []):
            if "resource" in item:
                child_res = parse_fhir_resource(item["resource"])
                bundle.add_entry(child_res, full_url=item.get("fullUrl"))
        return bundle

    # Generic fallback
    return FHIRResource(resourceType=resource_type, id=res_id)


def create_observation(
    patient_id: str,
    code: str,
    display: str,
    value: float,
    unit: str,
    system: str = "http://loinc.org",
) -> FHIRObservation:
    """Helper to construct standard clinical Observation resource."""
    obs_id = f"obs-{int(datetime.utcnow().timestamp() * 1000)}"
    coding = FHIRCoding(system=system, code=code, display=display)
    code_concept = FHIRCodeableConcept(coding=[coding], text=display)
    quantity = FHIRQuantity(value=value, unit=unit, system="http://unitsofmeasure.org", code=unit)
    subject = FHIRReference(reference=f"Patient/{patient_id}", type="Patient")
    
    return FHIRObservation(
        id=obs_id,
        status="final",
        code=code_concept,
        subject=subject,
        effectiveDateTime=datetime.utcnow().isoformat() + "Z",
        valueQuantity=quantity,
    )
