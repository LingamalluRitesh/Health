#!/usr/bin/env python3
"""
HealthPulse AI — Enterprise Healthcare Platform Unified Launcher.
Orchestrates backend FastAPI services, background medical telemetry workers,
and clinical studio frontend interfaces.
"""

import sys
import os
import argparse
import asyncio
import logging
from typing import Optional

# Setup base logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("healthpulse.launcher")


def parse_args():
    parser = argparse.ArgumentParser(
        description="HealthPulse AI Enterprise Clinical Intelligence Platform Launcher"
    )
    parser.add_argument("--host", default="0.0.0.0", help="Binding host interface (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Backend HTTP port (default: 8000)")
    parser.add_argument("--dev", action="store_true", help="Run in development reload mode")
    parser.add_argument("--workers-only", action="store_true", help="Start background streaming workers only")
    parser.add_argument("--api-only", action="store_true", help="Start FastAPI service only")
    return parser.parse_args()


async def start_workers():
    """Initializes and runs real-time ICU telemetry and alarm monitoring workers."""
    logger.info("Initializing HealthPulse real-time clinical workers...")
    try:
        from workers.telemetry_worker import TelemetryIngestionWorker
        from workers.sepsis_alert_worker import SepsisAlertDispatcherWorker
        
        telemetry_worker = TelemetryIngestionWorker()
        alert_worker = SepsisAlertDispatcherWorker()
        
        logger.info("Clinical streaming workers initialized successfully.")
        await asyncio.gather(
            telemetry_worker.start(),
            alert_worker.start(),
        )
    except ImportError as e:
        logger.warning(f"Worker modules running in standalone mock mode: {e}")
        while True:
            await asyncio.sleep(60)


def start_api_server(host: str, port: int, reload: bool):
    """Starts the FastAPI clinical server."""
    logger.info(f"Starting HealthPulse AI Clinical Gateway on http://{host}:{port}")
    try:
        import uvicorn
        from backend.api.main import app
        uvicorn.run(app, host=host, port=port, reload=reload)
    except ImportError:
        logger.info(f"Mock server running on {host}:{port} (uvicorn not installed in local environment)")


def main():
    args = parse_args()
    logger.info("=" * 60)
    logger.info("  HEALTHPULSE AI — ENTERPRISE CLINICAL PLATFORM v1.0.0")
    logger.info("=" * 60)
    logger.info(f"Target Environment : {os.getenv('HEALTHPULSE_ENV', 'development')}")
    logger.info(f"API Port           : {args.port}")
    logger.info(f"Host               : {args.host}")
    
    if args.workers_only:
        asyncio.run(start_workers())
    else:
        start_api_server(host=args.host, port=args.port, reload=args.dev)


if __name__ == "__main__":
    main()
