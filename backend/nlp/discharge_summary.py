"""
HealthPulse AI — Structured Hospital Discharge Summary Generator.
Synthesizes hospital inpatient stay, active discharge medications, and follow-up care instructions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DischargeSummaryData:
    patient_id: str
    patient_name: str
    admission_date: str
    discharge_date: str
    admission_diagnosis: str
    discharge_diagnosis: str
    hospital_course_summary: str
    discharge_medications: List[str]
    pending_lab_results: List[str]
    follow_up_appointments: List[str]
    discharge_condition: str = "Stable"


class DischargeSummaryGenerator:
    """Generates structured, standards-compliant discharge summary documents."""

    def generate_document(self, data: DischargeSummaryData) -> str:
        """Renders formal narrative discharge summary."""
        meds_formatted = "\n".join(f"  - {m}" for m in data.discharge_medications) or "  - None"
        followup_formatted = "\n".join(f"  - {f}" for f in data.follow_up_appointments) or "  - Follow up with Primary Care in 1-2 weeks"
        pending_formatted = "\n".join(f"  - {p}" for p in data.pending_lab_results) or "  - None"

        doc = f"""================================================================================
                    HEALTHPULSE AI HOSPITAL NETWORK
                       HOSPITAL DISCHARGE SUMMARY
================================================================================
PATIENT NAME       : {data.patient_name}
PATIENT ID (MRN)   : {data.patient_id}
ADMISSION DATE     : {data.admission_date}
DISCHARGE DATE     : {data.discharge_date}
DISCHARGE STATUS   : {data.discharge_condition}

1. PRIMARY DIAGNOSES AT DISCHARGE:
   {data.discharge_diagnosis}

2. INITIAL REASON FOR ADMISSION:
   {data.admission_diagnosis}

3. HOSPITAL COURSE & CLINICAL NARRATIVE:
   {data.hospital_course_summary}

4. DISCHARGE MEDICATIONS:
{meds_formatted}

5. PENDING LABS & STUDIES:
{pending_formatted}

6. FOLLOW-UP INSTRUCTIONS & APPOINTMENTS:
{followup_formatted}

================================================================================
Electronically Signed by: HealthPulse Attending Physician Staff
Document Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
================================================================================
"""
        return doc.strip()
