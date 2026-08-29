"""
HealthPulse AI — Real-Time Sepsis Alert & Clinical Deterioration Dispatcher Worker.
Subscribes to telemetry events, runs qSOFA & SOFA inference, and generates critical alerts.
"""

import asyncio
from datetime import datetime
from backend.core.logging import get_logger
from backend.core.events import event_bus, ClinicalEvent
from backend.core.types import ClinicalAlert, AlertType, ClinicalSeverity
from backend.core.database import db_store
from backend.clinical.sepsis_sofa import calculate_qsofa

logger = get_logger("healthpulse.worker.sepsis_alert")


class SepsisAlertDispatcherWorker:
    """Asynchronous worker that evaluates vitals for sepsis threshold breaches."""

    def __init__(self):
        self.is_running = False

    async def _handle_vitals_event(self, event: ClinicalEvent):
        payload = event.payload
        pid = payload.get("patient_id")
        rr = payload.get("respiratory_rate", 16.0)
        sbp = payload.get("systolic_bp", 120.0)
        
        # Calculate qSOFA
        q_res = calculate_qsofa(respiratory_rate=rr, gcs_score=15.0, systolic_bp=sbp)

        if q_res.score >= 2:
            alert = ClinicalAlert(
                alert_id=f"alert-{int(datetime.utcnow().timestamp() * 1000)}",
                patient_id=pid,
                alert_type=AlertType.SEPSIS_WARNING,
                severity=ClinicalSeverity.CRITICAL,
                message=f"CRITICAL: Bedside qSOFA score {q_res.score} >= 2 (RR: {rr}, SBP: {sbp}).",
                score=float(q_res.score),
                threshold=2.0,
                timestamp=datetime.utcnow(),
                evidence={"respiratory_rate": rr, "systolic_bp": sbp},
            )
            await db_store.add_alert(alert)
            logger.warning(f"Sepsis alert dispatched for patient {pid}: qSOFA={q_res.score}")

    async def start(self):
        self.is_running = True
        await event_bus.subscribe("vitals.received", self._handle_vitals_event)
        logger.info("SepsisAlertDispatcherWorker active and subscribed to telemetry events.")
        while self.is_running:
            await asyncio.sleep(60)

    def stop(self):
        self.is_running = False
