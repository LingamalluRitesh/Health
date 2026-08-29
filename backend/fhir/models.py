"""
HealthPulse AI — FHIR R4 (Fast Healthcare Interoperability Resources) Data Models.
Implements the HL7 FHIR Release 4.0.1 specification for clinical resources.
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class FHIRCoding:
    system: Optional[str] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    userSelected: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.system is not None:
            res["system"] = self.system
        if self.version is not None:
            res["version"] = self.version
        if self.code is not None:
            res["code"] = self.code
        if self.display is not None:
            res["display"] = self.display
        if self.userSelected is not None:
            res["userSelected"] = self.userSelected
        return res


@dataclass
class FHIRCodeableConcept:
    coding: List[FHIRCoding] = field(default_factory=list)
    text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.coding:
            res["coding"] = [c.to_dict() for c in self.coding]
        if self.text is not None:
            res["text"] = self.text
        return res


@dataclass
class FHIRIdentifier:
    use: Optional[str] = None
    system: Optional[str] = None
    value: Optional[str] = None
    type: Optional[FHIRCodeableConcept] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.use:
            res["use"] = self.use
        if self.system:
            res["system"] = self.system
        if self.value:
            res["value"] = self.value
        if self.type:
            res["type"] = self.type.to_dict()
        return res


@dataclass
class FHIRReference:
    reference: Optional[str] = None
    type: Optional[str] = None
    display: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.reference:
            res["reference"] = self.reference
        if self.type:
            res["type"] = self.type
        if self.display:
            res["display"] = self.display
        return res


@dataclass
class FHIRPeriod:
    start: Optional[str] = None
    end: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.start:
            res["start"] = self.start
        if self.end:
            res["end"] = self.end
        return res


@dataclass
class FHIRQuantity:
    value: Optional[float] = None
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = "http://unitsofmeasure.org"
    code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.value is not None:
            res["value"] = self.value
        if self.comparator:
            res["comparator"] = self.comparator
        if self.unit:
            res["unit"] = self.unit
        if self.system:
            res["system"] = self.system
        if self.code:
            res["code"] = self.code
        return res


@dataclass
class FHIRHumanName:
    use: Optional[str] = "official"
    text: Optional[str] = None
    family: Optional[str] = None
    given: List[str] = field(default_factory=list)
    prefix: List[str] = field(default_factory=list)
    suffix: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.use:
            res["use"] = self.use
        if self.text:
            res["text"] = self.text
        if self.family:
            res["family"] = self.family
        if self.given:
            res["given"] = self.given
        return res


@dataclass
class FHIRAddress:
    use: Optional[str] = "home"
    line: List[str] = field(default_factory=list)
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = "USA"

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.use:
            res["use"] = self.use
        if self.line:
            res["line"] = self.line
        if self.city:
            res["city"] = self.city
        if self.state:
            res["state"] = self.state
        if self.postalCode:
            res["postalCode"] = self.postalCode
        if self.country:
            res["country"] = self.country
        return res


@dataclass
class FHIRResource:
    resourceType: str
    id: str

    def to_dict(self) -> Dict[str, Any]:
        return {"resourceType": self.resourceType, "id": self.id}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class FHIRPatient(FHIRResource):
    resourceType: str = "Patient"
    id: str = ""
    identifier: List[FHIRIdentifier] = field(default_factory=list)
    active: bool = True
    name: List[FHIRHumanName] = field(default_factory=list)
    gender: str = "unknown"
    birthDate: Optional[str] = None
    deceasedBoolean: Optional[bool] = False
    address: List[FHIRAddress] = field(default_factory=list)
    maritalStatus: Optional[FHIRCodeableConcept] = None
    telecom: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "identifier": [i.to_dict() for i in self.identifier],
            "active": self.active,
            "name": [n.to_dict() for n in self.name],
            "gender": self.gender,
            "birthDate": self.birthDate,
            "deceasedBoolean": self.deceasedBoolean,
            "address": [a.to_dict() for a in self.address],
        })
        if self.maritalStatus:
            base["maritalStatus"] = self.maritalStatus.to_dict()
        if self.telecom:
            base["telecom"] = self.telecom
        return base


@dataclass
class FHIRObservation(FHIRResource):
    resourceType: str = "Observation"
    id: str = ""
    status: str = "final"
    category: List[FHIRCodeableConcept] = field(default_factory=list)
    code: FHIRCodeableConcept = field(default_factory=FHIRCodeableConcept)
    subject: Optional[FHIRReference] = None
    encounter: Optional[FHIRReference] = None
    effectiveDateTime: Optional[str] = None
    valueQuantity: Optional[FHIRQuantity] = None
    valueString: Optional[str] = None
    valueCodeableConcept: Optional[FHIRCodeableConcept] = None
    interpretation: List[FHIRCodeableConcept] = field(default_factory=list)
    referenceRange: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "status": self.status,
            "category": [c.to_dict() for c in self.category],
            "code": self.code.to_dict(),
        })
        if self.subject:
            base["subject"] = self.subject.to_dict()
        if self.encounter:
            base["encounter"] = self.encounter.to_dict()
        if self.effectiveDateTime:
            base["effectiveDateTime"] = self.effectiveDateTime
        if self.valueQuantity:
            base["valueQuantity"] = self.valueQuantity.to_dict()
        elif self.valueString:
            base["valueString"] = self.valueString
        elif self.valueCodeableConcept:
            base["valueCodeableConcept"] = self.valueCodeableConcept.to_dict()
        if self.interpretation:
            base["interpretation"] = [i.to_dict() for i in self.interpretation]
        if self.referenceRange:
            base["referenceRange"] = self.referenceRange
        return base


@dataclass
class FHIRCondition(FHIRResource):
    resourceType: str = "Condition"
    id: str = ""
    clinicalStatus: Optional[FHIRCodeableConcept] = None
    verificationStatus: Optional[FHIRCodeableConcept] = None
    category: List[FHIRCodeableConcept] = field(default_factory=list)
    severity: Optional[FHIRCodeableConcept] = None
    code: FHIRCodeableConcept = field(default_factory=FHIRCodeableConcept)
    subject: Optional[FHIRReference] = None
    encounter: Optional[FHIRReference] = None
    onsetDateTime: Optional[str] = None
    recordedDate: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["code"] = self.code.to_dict()
        if self.clinicalStatus:
            base["clinicalStatus"] = self.clinicalStatus.to_dict()
        if self.verificationStatus:
            base["verificationStatus"] = self.verificationStatus.to_dict()
        if self.category:
            base["category"] = [c.to_dict() for c in self.category]
        if self.severity:
            base["severity"] = self.severity.to_dict()
        if self.subject:
            base["subject"] = self.subject.to_dict()
        if self.onsetDateTime:
            base["onsetDateTime"] = self.onsetDateTime
        if self.recordedDate:
            base["recordedDate"] = self.recordedDate
        return base


@dataclass
class FHIREncounter(FHIRResource):
    resourceType: str = "Encounter"
    id: str = ""
    status: str = "in-progress"
    class_code: Optional[FHIRCoding] = None
    type: List[FHIRCodeableConcept] = field(default_factory=list)
    subject: Optional[FHIRReference] = None
    period: Optional[FHIRPeriod] = None
    reasonCode: List[FHIRCodeableConcept] = field(default_factory=list)
    hospitalization: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["status"] = self.status
        if self.class_code:
            base["class"] = self.class_code.to_dict()
        if self.type:
            base["type"] = [t.to_dict() for t in self.type]
        if self.subject:
            base["subject"] = self.subject.to_dict()
        if self.period:
            base["period"] = self.period.to_dict()
        if self.reasonCode:
            base["reasonCode"] = [r.to_dict() for r in self.reasonCode]
        return base


@dataclass
class FHIRDiagnosticReport(FHIRResource):
    resourceType: str = "DiagnosticReport"
    id: str = ""
    status: str = "final"
    category: List[FHIRCodeableConcept] = field(default_factory=list)
    code: FHIRCodeableConcept = field(default_factory=FHIRCodeableConcept)
    subject: Optional[FHIRReference] = None
    effectiveDateTime: Optional[str] = None
    issued: Optional[str] = None
    result: List[FHIRReference] = field(default_factory=list)
    conclusion: Optional[str] = None
    conclusionCode: List[FHIRCodeableConcept] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "status": self.status,
            "code": self.code.to_dict(),
            "category": [c.to_dict() for c in self.category],
            "result": [r.to_dict() for r in self.result],
        })
        if self.subject:
            base["subject"] = self.subject.to_dict()
        if self.effectiveDateTime:
            base["effectiveDateTime"] = self.effectiveDateTime
        if self.issued:
            base["issued"] = self.issued
        if self.conclusion:
            base["conclusion"] = self.conclusion
        return base


@dataclass
class FHIRMedicationRequest(FHIRResource):
    resourceType: str = "MedicationRequest"
    id: str = ""
    status: str = "active"
    intent: str = "order"
    medicationCodeableConcept: Optional[FHIRCodeableConcept] = None
    subject: Optional[FHIRReference] = None
    authoredOn: Optional[str] = None
    requester: Optional[FHIRReference] = None
    dosageInstruction: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "status": self.status,
            "intent": self.intent,
        })
        if self.medicationCodeableConcept:
            base["medicationCodeableConcept"] = self.medicationCodeableConcept.to_dict()
        if self.subject:
            base["subject"] = self.subject.to_dict()
        if self.authoredOn:
            base["authoredOn"] = self.authoredOn
        if self.dosageInstruction:
            base["dosageInstruction"] = self.dosageInstruction
        return base


@dataclass
class FHIRCarePlan(FHIRResource):
    resourceType: str = "CarePlan"
    id: str = ""
    status: str = "active"
    intent: str = "plan"
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[FHIRReference] = None
    period: Optional[FHIRPeriod] = None
    activity: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({"status": self.status, "intent": self.intent})
        if self.title:
            base["title"] = self.title
        if self.description:
            base["description"] = self.description
        if self.subject:
            base["subject"] = self.subject.to_dict()
        if self.period:
            base["period"] = self.period.to_dict()
        if self.activity:
            base["activity"] = self.activity
        return base


@dataclass
class FHIRBundleEntry:
    fullUrl: Optional[str] = None
    resource: Optional[FHIRResource] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {}
        if self.fullUrl:
            res["fullUrl"] = self.fullUrl
        if self.resource:
            res["resource"] = self.resource.to_dict()
        return res


@dataclass
class FHIRBundle(FHIRResource):
    resourceType: str = "Bundle"
    id: str = ""
    type: str = "collection"
    timestamp: Optional[str] = None
    total: int = 0
    entry: List[FHIRBundleEntry] = field(default_factory=list)

    def add_entry(self, resource: FHIRResource, full_url: Optional[str] = None) -> None:
        url = full_url or f"urn:uuid:{resource.id}"
        self.entry.append(FHIRBundleEntry(fullUrl=url, resource=resource))
        self.total = len(self.entry)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "type": self.type,
            "total": self.total,
            "entry": [e.to_dict() for e in self.entry],
        })
        if self.timestamp:
            base["timestamp"] = self.timestamp
        return base
