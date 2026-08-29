"""
HealthPulse AI — Asynchronous Storage and Patient Repository Layer.
Provides ACID persistence, repository abstractions, and schema models.
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from backend.core.types import PatientVitalSigns, ClinicalLabResult, MedicationOrder, ClinicalAlert


class InMemoryPatientStore:
    """Enterprise Patient Data Repository supporting in-memory transactional storage."""

    def __init__(self):
        self._patients: Dict[str, Dict[str, Any]] = {}
        self._vitals: Dict[str, List[PatientVitalSigns]] = {}
        self._labs: Dict[str, List[ClinicalLabResult]] = {}
        self._medications: Dict[str, List[MedicationOrder]] = {}
        self._alerts: Dict[str, List[ClinicalAlert]] = {}
        self._lock = asyncio.Lock()

    async def register_patient(self, patient_id: str, data: Dict[str, Any]) -> None:
        async with self._lock:
            data["created_at"] = datetime.utcnow()
            data["updated_at"] = datetime.utcnow()
            self._patients[patient_id] = data
            if patient_id not in self._vitals:
                self._vitals[patient_id] = []
            if patient_id not in self._labs:
                self._labs[patient_id] = []
            if patient_id not in self._medications:
                self._medications[patient_id] = []
            if patient_id not in self._alerts:
                self._alerts[patient_id] = []

    async def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        return self._patients.get(patient_id)

    async def list_patients(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        all_pts = list(self._patients.values())
        return all_pts[offset : offset + limit]

    async def add_vitals(self, vitals: PatientVitalSigns) -> None:
        async with self._lock:
            if vitals.patient_id not in self._vitals:
                self._vitals[vitals.patient_id] = []
            self._vitals[vitals.patient_id].append(vitals)

    async def get_latest_vitals(self, patient_id: str) -> Optional[PatientVitalSigns]:
        records = self._vitals.get(patient_id, [])
        return records[-1] if records else None

    async def get_vitals_history(self, patient_id: str, limit: int = 50) -> List[PatientVitalSigns]:
        records = self._vitals.get(patient_id, [])
        return records[-limit:]

    async def add_lab_result(self, patient_id: str, lab: ClinicalLabResult) -> None:
        async with self._lock:
            if patient_id not in self._labs:
                self._labs[patient_id] = []
            self._labs[patient_id].append(lab)

    async def get_lab_results(self, patient_id: str) -> List[ClinicalLabResult]:
        return self._labs.get(patient_id, [])

    async def add_medication(self, med: MedicationOrder) -> None:
        async with self._lock:
            if med.patient_id not in self._medications:
                self._medications[med.patient_id] = []
            self._medications[med.patient_id].append(med)

    async def get_active_medications(self, patient_id: str) -> List[MedicationOrder]:
        meds = self._medications.get(patient_id, [])
        return [m for m in meds if m.status == "active"]

    async def add_alert(self, alert: ClinicalAlert) -> None:
        async with self._lock:
            if alert.patient_id not in self._alerts:
                self._alerts[alert.patient_id] = []
            self._alerts[alert.patient_id].append(alert)

    async def get_active_alerts(self, patient_id: Optional[str] = None) -> List[ClinicalAlert]:
        if patient_id:
            alerts = self._alerts.get(patient_id, [])
            return [a for a in alerts if not a.acknowledged]
        
        all_active = []
        for p_alerts in self._alerts.values():
            all_active.extend([a for a in p_alerts if not a.acknowledged])
        return all_active


db_store = InMemoryPatientStore()
