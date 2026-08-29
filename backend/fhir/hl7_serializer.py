"""
HealthPulse AI — HL7 v2 Message Construction and Serializer.
Generates compliant HL7 v2 messages (ADT^A01, ADT^A08, ORU^R01, MDM^T02).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


def _format_hl7_timestamp(dt: Optional[datetime] = None) -> str:
    t = dt or datetime.utcnow()
    return t.strftime("%Y%m%d%H%M%S")


def build_adt_a01(
    patient_id: str,
    first_name: str,
    last_name: str,
    dob: str,
    gender: str,
    admit_time: Optional[datetime] = None,
    attending_doctor: str = "DOC999^Smith^John",
    location: str = "ICU-BED-04",
) -> str:
    """Builds HL7 v2 ADT^A01 (Admit / Visit Notification) message."""
    ts = _format_hl7_timestamp(admit_time)
    ctrl_id = f"MSG{int(datetime.utcnow().timestamp() * 1000)}"

    msh = f"MSH|^~\\&|HEALTHPULSE_EHR|HOSPITAL_MAIN|CLINICAL_AI|CENTRAL_MONITOR|{ts}||ADT^A01|{ctrl_id}|P|2.5"
    evn = f"EVN|A01|{ts}"
    pid = f"PID|1||{patient_id}^^^MRN||{last_name}^{first_name}||{dob}|{gender[:1].upper()}|||123 Hospital Way^^Boston^MA^02115^USA"
    pv1 = f"PV1|1|I|{location}||||{attending_doctor}|||MED|||||||||V1001|||||||||||||||||||||||||{ts}"

    return f"{msh}\r{evn}\r{pid}\r{pv1}\r"


def build_oru_r01(
    patient_id: str,
    order_number: str,
    test_code: str,
    test_name: str,
    value: str,
    units: str,
    ref_range: str,
    is_abnormal: bool,
    observed_time: Optional[datetime] = None,
) -> str:
    """Builds HL7 v2 ORU^R01 (Unsolicited Observation / Lab Results) message."""
    ts = _format_hl7_timestamp(observed_time)
    ctrl_id = f"MSG{int(datetime.utcnow().timestamp() * 1000)}"
    flag = "A" if is_abnormal else "N"

    msh = f"MSH|^~\\&|LAB_SYSTEM|CORE_LAB|HEALTHPULSE_AI|CLINICAL_DB|{ts}||ORU^R01|{ctrl_id}|P|2.5"
    pid = f"PID|1||{patient_id}^^^MRN"
    obr = f"OBR|1|{order_number}|{order_number}|{test_code}^{test_name}^LN|||{ts}|||||||||||||||||F"
    obx = f"OBX|1|NM|{test_code}^{test_name}^LN||{value}|{units}|{ref_range}|{flag}|||F|||{ts}"

    return f"{msh}\r{pid}\r{obr}\r{obx}\r"


def build_mdm_t02(
    patient_id: str,
    doc_id: str,
    author: str,
    doc_title: str,
    note_content: str,
    created_time: Optional[datetime] = None,
) -> str:
    """Builds HL7 v2 MDM^T02 (Medical Document Management / Clinical Note) message."""
    ts = _format_hl7_timestamp(created_time)
    ctrl_id = f"MSG{int(datetime.utcnow().timestamp() * 1000)}"

    msh = f"MSH|^~\\&|HEALTHPULSE_NLP|CLINICAL_NLP|HEALTHPULSE_AI|EHR_ARCHIVE|{ts}||MDM^T02|{ctrl_id}|P|2.5"
    pid = f"PID|1||{patient_id}^^^MRN"
    txd = f"TXA|1|{doc_title}|TEXT|{ts}|||{ts}|||{author}||||||||||DOC_STATUS_FINAL"
    
    # Text lines in OBX
    obx_lines = []
    for idx, line in enumerate(note_content.split("\n"), start=1):
        obx_lines.append(f"OBX|{idx}|TX|NOTE^Clinical Note^LN||{line}||||||F")

    obx_str = "\r".join(obx_lines)
    return f"{msh}\r{pid}\r{txd}\r{obx_str}\r"
