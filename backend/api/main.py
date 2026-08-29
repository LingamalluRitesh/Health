"""
HealthPulse AI — FastAPI Application Factory.
Configures CORS, middleware, global error handlers, route registries, and OpenAPI documentation.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from backend.core.config import get_settings
from backend.core.exceptions import HealthPulseException
from backend.api.routes_patients import router as patients_router
from backend.api.routes_clinical import router as clinical_router
from backend.api.routes_imaging import router as imaging_router
from backend.api.routes_genomics import router as genomics_router
from backend.api.routes_nlp import router as nlp_router
from backend.api.routes_governance import router as governance_router
from backend.api.routes_security import router as security_router
from backend.api.routes_federated import router as federated_router
from backend.api.routes_cds_hooks import router as cds_hooks_router
from backend.api.websockets_telemetry import router as ws_router
from backend.api.routes_analytics import router as analytics_router
from backend.api.routes_smart_fhir import router as smart_fhir_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="HealthPulse AI Enterprise Clinical API",
        description="HIPAA-compliant REST, GraphQL, CDS Hooks, and WebSocket streaming platform.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    @app.exception_handler(HealthPulseException)
    async def healthpulse_exception_handler(request: Request, exc: HealthPulseException):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "error_type": exc.__class__.__name__,
                "message": exc.message,
                "error_code": exc.error_code,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        )

    # Health Check
    @app.get("/health", tags=["System"])
    async def health_check():
        return {
            "status": "healthy",
            "service": "HealthPulse AI Clinical Platform",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "compliance": "HIPAA / EU AI Act High-Risk SaMD",
        }

    # Register Routers
    app.include_router(patients_router, prefix="/api/v1/patients", tags=["Patients & EHR"])
    app.include_router(clinical_router, prefix="/api/v1/clinical", tags=["Clinical Risk Calculators"])
    app.include_router(imaging_router, prefix="/api/v1/imaging", tags=["Medical Imaging & DICOM"])
    app.include_router(genomics_router, prefix="/api/v1/genomics", tags=["Genomics & PGx"])
    app.include_router(nlp_router, prefix="/api/v1/nlp", tags=["Clinical NLP & Terminology"])
    app.include_router(governance_router, prefix="/api/v1/governance", tags=["AI Governance & Model Cards"])
    app.include_router(security_router, prefix="/api/v1/security", tags=["HIPAA Security & Audit"])
    app.include_router(federated_router, prefix="/api/v1/federated", tags=["Federated Learning"])
    app.include_router(cds_hooks_router, prefix="/cds-services", tags=["CDS Hooks v1.0"])
    app.include_router(ws_router, prefix="/ws", tags=["Real-time WebSockets"])
    app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Clinical Analytics"])
    app.include_router(smart_fhir_router, prefix="/api/v1/smart", tags=["SMART on FHIR"])

    return app


app = create_app()
