"""
HealthPulse AI — SOAP (Subjective, Objective, Assessment, Plan) Note Sectionizer.
Parses unstructured clinical notes into structured medical sections.
"""

import re
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SOAPNoteStructure:
    subjective: str
    objective: str
    assessment: str
    plan: str
    chief_complaint: Optional[str] = None
    vital_signs_extracted: Optional[str] = None


class SOAPNoteParser:
    """Deconstructs free-text clinical encounters into standard SOAP blocks."""

    def __init__(self):
        self.header_patterns = {
            "subjective": re.compile(r"(?:^|\n)\s*(?:SUBJECTIVE|HISTORY OF PRESENT ILLNESS|HPI|CHIEF COMPLAINT|S:)\s*[:\-]?\s*", re.IGNORECASE),
            "objective": re.compile(r"(?:^|\n)\s*(?:OBJECTIVE|PHYSICAL EXAM|EXAMINATION|LABS|VITALS|O:)\s*[:\-]?\s*", re.IGNORECASE),
            "assessment": re.compile(r"(?:^|\n)\s*(?:ASSESSMENT|IMPRESSION|DIAGNOSIS|CLINICAL IMPRESSION|A:)\s*[:\-]?\s*", re.IGNORECASE),
            "plan": re.compile(r"(?:^|\n)\s*(?:PLAN|TREATMENT PLAN|RECOMMENDATIONS|P:)\s*[:\-]?\s*", re.IGNORECASE),
        }

    def parse(self, note_text: str) -> SOAPNoteStructure:
        """Extracts text for Subjective, Objective, Assessment, and Plan."""
        text = note_text.strip()

        # Find header positions
        positions = []
        for sec_name, pattern in self.header_patterns.items():
            match = pattern.search(text)
            if match:
                positions.append((match.start(), match.end(), sec_name))

        positions.sort(key=lambda p: p[0])

        sections: Dict[str, str] = {
            "subjective": "",
            "objective": "",
            "assessment": "",
            "plan": "",
        }

        for i, (start, content_start, sec_name) in enumerate(positions):
            end = positions[i + 1][0] if (i + 1) < len(positions) else len(text)
            sections[sec_name] = text[content_start:end].strip()

        # If no explicit sections detected, treat entire text as assessment/plan
        if not any(sections.values()):
            sections["assessment"] = text

        return SOAPNoteStructure(
            subjective=sections["subjective"],
            objective=sections["objective"],
            assessment=sections["assessment"],
            plan=sections["plan"],
        )
