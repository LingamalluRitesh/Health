"""
HealthPulse AI — Enterprise Configuration Management.
Centralized environment and security settings loader.
"""

import os
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class DatabaseSettings:
    url: str = "sqlite+aiosqlite:///./healthpulse.db"
    pool_size: int = 20
    max_overflow: int = 10
    echo_sql: bool = False


@dataclass
class RedisSettings:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    ssl: bool = False


@dataclass
class SecuritySettings:
    jwt_secret_key: str = "enterprise-clinical-ai-secure-token-2026"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    enable_hipaa_audit_trail: bool = True
    enable_break_glass_mode: bool = True
    diff_privacy_epsilon: float = 0.5
    diff_privacy_delta: float = 1e-5


@dataclass
class DICOMSettings:
    pacs_wado_rs_url: str = "http://localhost:8042/dicom-web"
    storage_root: str = "./data_storage/dicom"
    max_slice_buffer_mb: int = 512
    enable_gpu_acceleration: bool = False


@dataclass
class Settings:
    environment: str = "development"
    app_name: str = "HealthPulse AI Enterprise"
    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    allowed_origins: List[str] = field(default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"])
    
    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    redis: RedisSettings = field(default_factory=RedisSettings)
    security: SecuritySettings = field(default_factory=SecuritySettings)
    dicom: DICOMSettings = field(default_factory=DICOMSettings)

    @classmethod
    def load_from_env(cls) -> "Settings":
        env = os.getenv("HEALTHPULSE_ENV", "development")
        debug = os.getenv("HEALTHPULSE_DEBUG", "false").lower() in ("true", "1", "yes")
        port = int(os.getenv("PORT", "8000"))
        host = os.getenv("HOST", "0.0.0.0")

        return cls(
            environment=env,
            debug=debug,
            port=port,
            host=host,
        )


_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings.load_from_env()
    return _settings_instance
