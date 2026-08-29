"""
HealthPulse AI — High-Throughput HL7 & DICOM Ingestion Queue Worker.
Processes asynchronous batches of clinical messages and images without blocking HTTP gateways.
"""

import asyncio
from typing import List, Dict, Any
from backend.core.logging import get_logger
from backend.fhir.hl7_parser import parse_hl7_v2
from backend.fhir.serializer import parse_fhir_resource

logger = get_logger("healthpulse.worker.ingestion")


class AsyncIngestionWorker:
    """Asynchronous pipeline queue worker for incoming HL7/FHIR payloads."""

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False

    async def enqueue_message(self, message_type: str, raw_payload: str):
        await self.queue.put({"type": message_type, "payload": raw_payload})

    async def _process_item(self, item: Dict[str, Any]):
        m_type = item.get("type")
        raw = item.get("payload", "")

        try:
            if m_type == "HL7_V2":
                parsed_hl7 = parse_hl7_v2(raw)
                logger.info(f"HL7 message processed: type={parsed_hl7.message_type}^{parsed_hl7.trigger_event}")
            elif m_type == "FHIR_JSON":
                # Process FHIR
                pass
        except Exception as e:
            logger.error(f"Error processing ingestion item: {e}")

    async def start(self):
        self.is_running = True
        logger.info("AsyncIngestionWorker started.")
        while self.is_running:
            item = await self.queue.get()
            await self._process_item(item)
            self.queue.task_done()

    def stop(self):
        self.is_running = False
