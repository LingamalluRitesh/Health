"""
HealthPulse AI — Asynchronous Clinical Event Bus.
Decouples real-time ICU telemetry ingestion from clinical alert triggers and audit loggers.
"""

import asyncio
from typing import Dict, List, Callable, Any, Coroutine
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ClinicalEvent:
    event_id: str
    topic: str
    payload: Dict[str, Any]
    timestamp: datetime
    source: str


EventListener = Callable[[ClinicalEvent], Coroutine[Any, Any, None]]


class ClinicalEventBus:
    """Asynchronous Pub-Sub Event Bus for Medical Alerts and Telemetry Streams."""

    def __init__(self):
        self._subscribers: Dict[str, List[EventListener]] = {}
        self._lock = asyncio.Lock()

    async def subscribe(self, topic: str, listener: EventListener) -> None:
        async with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(listener)

    async def publish(self, topic: str, payload: Dict[str, Any], source: str = "system") -> None:
        event = ClinicalEvent(
            event_id=f"evt_{int(datetime.utcnow().timestamp() * 1000)}",
            topic=topic,
            payload=payload,
            timestamp=datetime.utcnow(),
            source=source,
        )

        listeners = self._subscribers.get(topic, []).copy()
        wildcard_listeners = self._subscribers.get("*", []).copy()
        all_listeners = listeners + wildcard_listeners

        if all_listeners:
            tasks = [asyncio.create_task(listener(event)) for listener in all_listeners]
            await asyncio.gather(*tasks, return_exceptions=True)


event_bus = ClinicalEventBus()
