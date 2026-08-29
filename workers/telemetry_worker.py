"""
HealthPulse AI — Real-Time Telemetry Ingestion Worker.
Continuously ingests multi-bed physiological vital streams and publishes to the clinical event bus.
"""

import asyncio
import random
from typing import List, Optional
from datetime import datetime
from backend.core.logging import get_logger
from backend.core.events import event_bus
from backend.core.types import PatientVitalSigns
from backend.core.database import db_store

logger = get_logger("healthpulse.worker.telemetry")


class TelemetryIngestionWorker:
    """Simulates multi-patient ICU monitor streaming and event ingestion."""

    def __init__(self, monitored_patients: Optional[list] = None):
        self.monitored_patients = monitored_patients or ["P-100234", "P-100235", "P-100236"]
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info(f"TelemetryIngestionWorker started for {len(self.monitored_patients)} ICU beds.")

        while self.is_running:
            for pid in self.monitored_patients:
                # Generate physiological reading
                vitals = PatientVitalSigns(
                    patient_id=pid,
                    timestamp=datetime.utcnow(),
                    heart_rate=round(random.uniform(65.0, 115.0), 1),
                    respiratory_rate=round(random.uniform(14.0, 26.0), 1),
                    systolic_bp=round(random.uniform(90.0, 145.0), 1),
                    diastolic_bp=round(random.uniform(55.0, 90.0), 1),
                    oxygen_saturation=round(random.uniform(92.0, 99.0), 1),
                    temperature_celsius=round(random.uniform(36.6, 38.9), 1),
                )
                await db_store.add_vitals(vitals)

                # Publish event
                await event_bus.publish(
                    topic="vitals.received",
                    payload={
                        "patient_id": pid,
                        "heart_rate": vitals.heart_rate,
                        "respiratory_rate": vitals.respiratory_rate,
                        "systolic_bp": vitals.systolic_bp,
                        "spo2": vitals.oxygen_saturation,
                        "temp_c": vitals.temperature_celsius,
                    },
                    source="TelemetryWorker",
                )

            await asyncio.sleep(2.0)

    def stop(self):
        self.is_running = False
        logger.info("TelemetryIngestionWorker stopped.")
