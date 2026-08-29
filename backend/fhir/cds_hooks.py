"""
HealthPulse AI — CDS Hooks (Clinical Decision Support) v1.0 Standard Service.
Implements clinical trigger hooks (patient-view, order-select, order-sign, medication-prescribe)
and generates evidence cards with suggestions and FHIR actions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from backend.core.types import ClinicalSeverity


@dataclass
class CDSSource:
    label: str
    url: Optional[str] = None
    icon: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {"label": self.label}
        if self.url:
            res["url"] = self.url
        if self.icon:
            res["icon"] = self.icon
        return res


@dataclass
class CDSSuggestionAction:
    type: str  # create, update, delete
    description: str
    resource: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        res = {"type": self.type, "description": self.description}
        if self.resource:
            res["resource"] = self.resource
        return res


@dataclass
class CDSSuggestion:
    label: str
    uuid: Optional[str] = None
    actions: List[CDSSuggestionAction] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res = {
            "label": self.label,
            "actions": [a.to_dict() for a in self.actions],
        }
        if self.uuid:
            res["uuid"] = self.uuid
        return res


@dataclass
class CDSCard:
    summary: str
    indicator: str  # info, warning, critical
    source: CDSSource
    detail: Optional[str] = None
    suggestions: List[CDSSuggestion] = field(default_factory=list)
    selectionBehavior: Optional[str] = "at-most-one"
    overrideReasons: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "summary": self.summary,
            "indicator": self.indicator,
            "source": self.source.to_dict(),
        }
        if self.detail:
            res["detail"] = self.detail
        if self.suggestions:
            res["suggestions"] = [s.to_dict() for s in self.suggestions]
        if self.selectionBehavior:
            res["selectionBehavior"] = self.selectionBehavior
        return res


@dataclass
class CDSServiceDescriptor:
    hook: str
    title: str
    description: str
    id: str
    prefetch: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hook": self.hook,
            "title": self.title,
            "description": self.description,
            "id": self.id,
            "prefetch": self.prefetch,
        }


class CDSServiceDiscovery:
    """Manages available CDS Hooks service endpoints."""

    def __init__(self):
        self.services: List[CDSServiceDescriptor] = [
            CDSServiceDescriptor(
                hook="patient-view",
                title="Sepsis Early Warning Advisor",
                description="Monitors real-time vitals and triggers qSOFA/SOFA alert cards with recommended bundle actions.",
                id="sepsis-early-warning",
                prefetch={
                    "patient": "Patient/{{context.patientId}}",
                    "observations": "Observation?subject=Patient/{{context.patientId}}&_sort=-date&_count=20",
                },
            ),
            CDSServiceDescriptor(
                hook="order-select",
                title="Pharmacogenomics & DDI Safety Checker",
                description="Checks prospective medication orders against patient genotype (CYP2D6, CYP2C19) and active drug lists.",
                id="pgx-ddi-safety",
                prefetch={
                    "patient": "Patient/{{context.patientId}}",
                    "medications": "MedicationRequest?subject=Patient/{{context.patientId}}&status=active",
                },
            ),
            CDSServiceDescriptor(
                hook="order-sign",
                title="Renal Drug Dosing & eGFR Advisor",
                description="Evaluates nephrotoxic drug dosages against real-time CKD-EPI eGFR estimates.",
                id="renal-dosing-advisor",
                prefetch={
                    "patient": "Patient/{{context.patientId}}",
                    "creatinine": "Observation?subject=Patient/{{context.patientId}}&code=2160-0&_sort=-date&_count=1",
                },
            ),
        ]

    def get_services(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.services]


class CDSHooksEngine:
    """Evaluates CDS Hook requests and renders advisory cards."""

    def __init__(self):
        self.discovery = CDSServiceDiscovery()

    def evaluate_patient_view(
        self,
        patient_id: str,
        qsofa_score: int,
        sofa_score: int,
        temp_c: float,
        hr: float,
        rr: float,
    ) -> List[CDSCard]:
        cards: List[CDSCard] = []

        if qsofa_score >= 2 or sofa_score >= 2:
            card = CDSCard(
                summary=f"CRITICAL: Elevated Sepsis Risk (SOFA: {sofa_score}, qSOFA: {qsofa_score})",
                indicator="critical",
                source=CDSSource(
                    label="HealthPulse Surviving Sepsis Guideline Engine",
                    url="https://healthpulse.ai/guidelines/sepsis-3",
                ),
                detail=(
                    f"Patient {patient_id} demonstrates organ dysfunction markers. "
                    f"Parameters: RR {rr} bpm, HR {hr} bpm, Temp {temp_c}°C. "
                    "Initiate 1-Hour Sepsis Bundle immediately: draw blood cultures, measure serum lactate, "
                    "administer broad-spectrum antibiotics, and initiate 30 mL/kg IV crystalloid fluid."
                ),
                suggestions=[
                    CDSSuggestion(
                        label="Order 1-Hour Sepsis Resuscitation Bundle",
                        actions=[
                            CDSSuggestionAction(
                                type="create",
                                description="Order Serum Lactate Lab STAT",
                            ),
                            CDSSuggestionAction(
                                type="create",
                                description="Order Blood Cultures x 2 STAT",
                            ),
                            CDSSuggestionAction(
                                type="create",
                                description="Initiate IV Piperacillin/Tazobactam 4.5g q6h",
                            ),
                        ],
                    )
                ],
            )
            cards.append(card)
        return cards

    def evaluate_order_select_ddi(
        self,
        patient_id: str,
        ordered_drug: str,
        active_drugs: List[str],
        interaction_warnings: List[str],
    ) -> List[CDSCard]:
        cards: List[CDSCard] = []
        if interaction_warnings:
            card = CDSCard(
                summary=f"WARNING: Major Drug-Drug Interaction for {ordered_drug}",
                indicator="warning",
                source=CDSSource(
                    label="HealthPulse Clinical Pharmacology Engine",
                    url="https://healthpulse.ai/pharmacology/ddi",
                ),
                detail="; ".join(interaction_warnings),
                suggestions=[
                    CDSSuggestion(
                        label=f"Consider Alternative Non-Interacting Agent for {ordered_drug}",
                        actions=[
                            CDSSuggestionAction(
                                type="delete",
                                description=f"Cancel order for {ordered_drug}",
                            )
                        ],
                    )
                ],
            )
            cards.append(card)
        return cards
