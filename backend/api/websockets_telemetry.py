"""
HealthPulse AI — Real-Time WebSocket Telemetry Gateway.
Streams high-frequency physiological vital signs, waveforms, and instant alarms to bedside clinical monitors.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
import random
from datetime import datetime
from typing import List


router = APIRouter()


class ConnectionManager:
    """Manages active bedside client WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass


manager = ConnectionManager()


@router.websocket("/telemetry/{patient_id}")
async def websocket_patient_telemetry(websocket: WebSocket, patient_id: str):
    await manager.connect(websocket)
    try:
        hr = 78.0
        sbp = 120.0
        dbp = 75.0
        spo2 = 98.0
        rr = 16.0

        while True:
            # Simulate real-time continuous physiological drift
            hr += random.uniform(-1.5, 1.5)
            sbp += random.uniform(-2.0, 2.0)
            dbp += random.uniform(-1.0, 1.0)
            spo2 += random.uniform(-0.2, 0.2)
            rr += random.uniform(-0.5, 0.5)

            hr = max(50.0, min(140.0, hr))
            sbp = max(80.0, min(180.0, sbp))
            dbp = max(50.0, min(110.0, dbp))
            spo2 = max(88.0, min(100.0, spo2))
            rr = max(10.0, min(35.0, rr))

            packet = {
                "patient_id": patient_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "heart_rate": round(hr, 1),
                "systolic_bp": round(sbp, 1),
                "diastolic_bp": round(dbp, 1),
                "mean_arterial_pressure": round((2 * dbp + sbp) / 3.0, 1),
                "oxygen_saturation": round(spo2, 1),
                "respiratory_rate": round(rr, 1),
                "is_alarm_triggered": hr > 110.0 or spo2 < 92.0 or sbp < 90.0,
            }

            await websocket.send_text(json.dumps(packet))
            await asyncio.sleep(1.0)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
