"""
HealthPulse AI — HL7 v2.x Message Parsing and Structural Decomposition.
Parses standard HL7 v2 pipes-and-hats messages (MSH, PID, PV1, OBR, OBX, DG1, AL1, RXE).
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from backend.core.exceptions import HL7MessageException


@dataclass
class HL7Field:
    value: str
    components: List[str] = field(default_factory=list)

    @classmethod
    def parse(cls, raw: str, component_sep: str = "^") -> "HL7Field":
        comps = raw.split(component_sep)
        return cls(value=raw, components=comps)

    def get_component(self, index: int, default: str = "") -> str:
        """Returns 1-indexed component."""
        if 1 <= index <= len(self.components):
            return self.components[index - 1]
        return default


@dataclass
class HL7Segment:
    name: str
    fields: List[HL7Field] = field(default_factory=list)

    def get_field(self, field_num: int, default: str = "") -> str:
        """Returns 1-indexed field value from segment."""
        # For MSH, MSH-1 is the field separator itself
        if self.name == "MSH":
            if field_num == 1:
                return "|"
            if 2 <= field_num <= len(self.fields) + 1:
                return self.fields[field_num - 2].value
            return default
        else:
            if 1 <= field_num <= len(self.fields):
                return self.fields[field_num - 1].value
            return default

    def get_component(self, field_num: int, comp_num: int, default: str = "") -> str:
        if self.name == "MSH":
            if field_num == 1:
                return "|"
            if 2 <= field_num <= len(self.fields) + 1:
                return self.fields[field_num - 2].get_component(comp_num, default)
            return default
        else:
            if 1 <= field_num <= len(self.fields):
                return self.fields[field_num - 1].get_component(comp_num, default)
            return default


@dataclass
class HL7Message:
    message_type: str
    trigger_event: str
    control_id: str
    sending_app: str
    sending_facility: str
    segments: List[HL7Segment] = field(default_factory=list)

    def get_segments(self, name: str) -> List[HL7Segment]:
        return [s for s in self.segments if s.name == name]

    def get_first_segment(self, name: str) -> Optional[HL7Segment]:
        for s in self.segments:
            if s.name == name:
                return s
        return None


def parse_hl7_v2(raw_text: str) -> HL7Message:
    """Parses raw HL7 v2.x string into structured HL7Message."""
    lines = [line.strip() for line in raw_text.replace("\r\n", "\r").replace("\n", "\r").split("\r") if line.strip()]
    if not lines:
        raise HL7MessageException("Empty HL7 message string")

    # Parse MSH
    msh_line = lines[0]
    if not msh_line.startswith("MSH"):
        raise HL7MessageException(f"First segment must be MSH, got: {msh_line[:3]}")

    field_sep = msh_line[3]
    encoding_chars = msh_line[4:8]
    comp_sep = encoding_chars[0] if len(encoding_chars) > 0 else "^"

    parsed_segments: List[HL7Segment] = []
    
    # Parse MSH fields
    msh_raw_fields = msh_line.split(field_sep)
    msh_fields = [HL7Field.parse(f, comp_sep) for f in msh_raw_fields[1:]]
    parsed_segments.append(HL7Segment(name="MSH", fields=msh_fields))

    # Header parameters
    sending_app = msh_fields[1].value if len(msh_fields) > 1 else ""
    sending_facility = msh_fields[2].value if len(msh_fields) > 2 else ""
    msg_type_field = msh_fields[7] if len(msh_fields) > 7 else HL7Field("")
    msg_type = msg_type_field.get_component(1, "UNKNOWN")
    trigger_evt = msg_type_field.get_component(2, "UNKNOWN")
    control_id = msh_fields[8].value if len(msh_fields) > 8 else ""

    # Parse remaining segments
    for line in lines[1:]:
        raw_fields = line.split(field_sep)
        seg_name = raw_fields[0]
        seg_fields = [HL7Field.parse(f, comp_sep) for f in raw_fields[1:]]
        parsed_segments.append(HL7Segment(name=seg_name, fields=seg_fields))

    return HL7Message(
        message_type=msg_type,
        trigger_event=trigger_evt,
        control_id=control_id,
        sending_app=sending_app,
        sending_facility=sending_facility,
        segments=parsed_segments,
    )
