"""
HealthPulse AI — Enterprise Structured Logging and PHI-Safe Redaction.
Ensures that clinical logs never leak unmasked Protected Health Information.
"""

import logging
import json
import re
import sys
from typing import Any, Dict
from datetime import datetime


PHI_SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
PHI_PHONE_PATTERN = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
PHI_EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
PHI_MRN_PATTERN = re.compile(r"\bMRN-?[A-Z0-9]{6,10}\b", re.IGNORECASE)


class PHISafeFormatter(logging.Formatter):
    """Custom logging formatter that strips PHI from log messages."""

    def format(self, record: logging.LogRecord) -> str:
        orig_msg = record.getMessage()
        sanitized = self._sanitize_phi(orig_msg)
        
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": sanitized,
            "module": record.module,
            "line": record.lineno,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)

    def _sanitize_phi(self, text: str) -> str:
        text = PHI_SSN_PATTERN.sub("[REDACTED_SSN]", text)
        text = PHI_PHONE_PATTERN.sub("[REDACTED_PHONE]", text)
        text = PHI_EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
        text = PHI_MRN_PATTERN.sub("[REDACTED_MRN]", text)
        return text


def configure_logging(level: int = logging.INFO) -> None:
    """Configures root logger with PHI safe structured JSON formatting."""
    root = logging.getLogger()
    root.setLevel(level)

    # Clear existing handlers
    while root.handlers:
        root.handlers.pop()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(PHISafeFormatter())
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Returns a named logger."""
    return logging.getLogger(name)
