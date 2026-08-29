"""
HealthPulse AI — DICOM (Digital Imaging and Communications in Medicine) Binary & Metadata Parser.
Implements DICOM Part 5 (Data Structures and Encoding) and Part 10 (Media Storage).
"""

import struct
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from backend.core.exceptions import DICOMProcessingException


@dataclass
class DICOMTag:
    group: int
    element: int
    vr: str
    length: int
    value: Any

    @property
    def hex_tag(self) -> str:
        return f"({self.group:04X},{self.element:04X})"


@dataclass
class DICOMDataset:
    sop_instance_uid: str
    study_instance_uid: str
    series_instance_uid: str
    patient_id: str
    patient_name: str
    modality: str
    study_date: str
    rows: int
    columns: int
    bits_allocated: int
    bits_stored: int
    high_bit: int
    pixel_representation: int  # 0 = unsigned, 1 = 2's complement signed
    rescale_intercept: float = 0.0
    rescale_slope: float = 1.0
    window_center: float = 40.0
    window_width: float = 400.0
    pixel_spacing: Tuple[float, float] = (1.0, 1.0)  # (row_spacing, col_spacing) in mm
    slice_thickness: float = 1.0                     # mm
    slice_location: float = 0.0
    tags: Dict[str, DICOMTag] = field(default_factory=dict)
    pixel_data: Optional[List[int]] = None           # 1D flattened raw pixel integers

    def get_pixel(self, row: int, col: int) -> int:
        if self.pixel_data is None:
            return 0
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return self.pixel_data[row * self.columns + col]
        return 0


# Common DICOM Tag Hex mappings
TAG_PATIENT_NAME = (0x0010, 0x0010)
TAG_PATIENT_ID = (0x0010, 0x0020)
TAG_STUDY_DATE = (0x0008, 0x0020)
TAG_MODALITY = (0x0008, 0x0060)
TAG_STUDY_INSTANCE_UID = (0x0020, 0x000D)
TAG_SERIES_INSTANCE_UID = (0x0020, 0x000E)
TAG_SOP_INSTANCE_UID = (0x0008, 0x0018)
TAG_ROWS = (0x0028, 0x0010)
TAG_COLUMNS = (0x0028, 0x0011)
TAG_BITS_ALLOCATED = (0x0028, 0x0100)
TAG_BITS_STORED = (0x0028, 0x0101)
TAG_HIGH_BIT = (0x0028, 0x0102)
TAG_PIXEL_REPRESENTATION = (0x0028, 0x0103)
TAG_RESCALE_INTERCEPT = (0x0028, 0x1052)
TAG_RESCALE_SLOPE = (0x0028, 0x1053)
TAG_WINDOW_CENTER = (0x0028, 0x1050)
TAG_WINDOW_WIDTH = (0x0028, 0x1051)
TAG_PIXEL_SPACING = (0x0028, 0x0030)
TAG_SLICE_THICKNESS = (0x0018, 0x0050)
TAG_SLICE_LOCATION = (0x0020, 0x1041)
TAG_PIXEL_DATA = (0x7FE0, 0x0010)


def parse_dicom_bytes(raw_bytes: bytes) -> DICOMDataset:
    """
    Parses a raw DICOM byte stream (with 128-byte preamble + DICM magic prefix).
    """
    if len(raw_bytes) < 132:
        raise DICOMProcessingException("Payload too small to be a valid DICOM Part 10 file")

    magic = raw_bytes[128:132]
    if magic != b"DICM":
        raise DICOMProcessingException(f"Invalid DICOM magic header, expected b'DICM' got {magic}")

    offset = 132
    tags: Dict[str, DICOMTag] = {}

    rows = 512
    cols = 512
    bits_alloc = 16
    bits_stored = 12
    high_bit = 11
    pixel_rep = 0
    rescale_intercept = 0.0
    rescale_slope = 1.0
    window_center = 40.0
    window_width = 400.0
    pixel_spacing = (1.0, 1.0)
    slice_thickness = 1.0
    slice_location = 0.0
    patient_id = "UNKNOWN"
    patient_name = "ANONYMOUS"
    modality = "CT"
    study_uid = f"1.2.840.10008.1.{int(offset)}"
    series_uid = f"1.2.840.10008.2.{int(offset)}"
    sop_uid = f"1.2.840.10008.3.{int(offset)}"
    study_date = "20260101"
    pixel_array: Optional[List[int]] = None

    # Sequential tag scanner
    while offset + 8 <= len(raw_bytes):
        group, element = struct.unpack("<HH", raw_bytes[offset : offset + 4])
        vr_raw = raw_bytes[offset + 4 : offset + 6]
        
        # Check standard 2-char VR (Explicit VR Little Endian)
        try:
            vr_str = vr_raw.decode("ascii")
        except UnicodeDecodeError:
            vr_str = "UN"

        if vr_str in ("OB", "OW", "OF", "SQ", "UC", "UR", "UT", "UN"):
            if offset + 12 > len(raw_bytes):
                break
            length = struct.unpack("<I", raw_bytes[offset + 8 : offset + 12])[0]
            val_offset = offset + 12
            offset = val_offset + length
        else:
            if offset + 8 > len(raw_bytes):
                break
            length = struct.unpack("<H", raw_bytes[offset + 6 : offset + 8])[0]
            val_offset = offset + 8
            offset = val_offset + length

        if val_offset + length > len(raw_bytes):
            length = max(0, len(raw_bytes) - val_offset)

        val_bytes = raw_bytes[val_offset : val_offset + length]
        tag_key = f"({group:04X},{element:04X})"

        if (group, element) == TAG_PATIENT_ID:
            patient_id = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_PATIENT_NAME:
            patient_name = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_MODALITY:
            modality = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_STUDY_INSTANCE_UID:
            study_uid = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_SERIES_INSTANCE_UID:
            series_uid = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_SOP_INSTANCE_UID:
            sop_uid = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_STUDY_DATE:
            study_date = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00")
        elif (group, element) == TAG_ROWS and len(val_bytes) >= 2:
            rows = struct.unpack("<H", val_bytes[:2])[0]
        elif (group, element) == TAG_COLUMNS and len(val_bytes) >= 2:
            cols = struct.unpack("<H", val_bytes[:2])[0]
        elif (group, element) == TAG_BITS_ALLOCATED and len(val_bytes) >= 2:
            bits_alloc = struct.unpack("<H", val_bytes[:2])[0]
        elif (group, element) == TAG_BITS_STORED and len(val_bytes) >= 2:
            bits_stored = struct.unpack("<H", val_bytes[:2])[0]
        elif (group, element) == TAG_HIGH_BIT and len(val_bytes) >= 2:
            high_bit = struct.unpack("<H", val_bytes[:2])[0]
        elif (group, element) == TAG_PIXEL_REPRESENTATION and len(val_bytes) >= 2:
            pixel_rep = struct.unpack("<H", val_bytes[:2])[0]
        elif (group, element) == TAG_RESCALE_INTERCEPT:
            try:
                rescale_intercept = float(val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00"))
            except ValueError:
                pass
        elif (group, element) == TAG_RESCALE_SLOPE:
            try:
                rescale_slope = float(val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00"))
            except ValueError:
                pass
        elif (group, element) == TAG_WINDOW_CENTER:
            try:
                raw_wc = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00").split("\\")[0]
                window_center = float(raw_wc)
            except (ValueError, IndexError):
                pass
        elif (group, element) == TAG_WINDOW_WIDTH:
            try:
                raw_ww = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00").split("\\")[0]
                window_width = float(raw_ww)
            except (ValueError, IndexError):
                pass
        elif (group, element) == TAG_PIXEL_SPACING:
            try:
                parts = val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00").split("\\")
                if len(parts) >= 2:
                    pixel_spacing = (float(parts[0]), float(parts[1]))
            except ValueError:
                pass
        elif (group, element) == TAG_SLICE_THICKNESS:
            try:
                slice_thickness = float(val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00"))
            except ValueError:
                pass
        elif (group, element) == TAG_SLICE_LOCATION:
            try:
                slice_location = float(val_bytes.decode("ascii", errors="ignore").strip().rstrip("\x00"))
            except ValueError:
                pass
        elif (group, element) == TAG_PIXEL_DATA:
            # Decode pixel array
            num_pixels = rows * cols
            if bits_alloc == 16:
                fmt = f"<{num_pixels}h" if pixel_rep == 1 else f"<{num_pixels}H"
                expected_bytes = num_pixels * 2
                if len(val_bytes) >= expected_bytes:
                    pixel_array = list(struct.unpack(fmt, val_bytes[:expected_bytes]))
            elif bits_alloc == 8:
                fmt = f"<{num_pixels}b" if pixel_rep == 1 else f"<{num_pixels}B"
                if len(val_bytes) >= num_pixels:
                    pixel_array = list(struct.unpack(fmt, val_bytes[:num_pixels]))

        tag_obj = DICOMTag(
            group=group,
            element=element,
            vr=vr_str,
            length=length,
            value=val_bytes,
        )
        tags[tag_key] = tag_obj

    if pixel_array is None:
        pixel_array = [0] * (rows * cols)

    return DICOMDataset(
        sop_instance_uid=sop_uid,
        study_instance_uid=study_uid,
        series_instance_uid=series_uid,
        patient_id=patient_id,
        patient_name=patient_name,
        modality=modality,
        study_date=study_date,
        rows=rows,
        columns=cols,
        bits_allocated=bits_alloc,
        bits_stored=bits_stored,
        high_bit=high_bit,
        pixel_representation=pixel_rep,
        rescale_intercept=rescale_intercept,
        rescale_slope=rescale_slope,
        window_center=window_center,
        window_width=window_width,
        pixel_spacing=pixel_spacing,
        slice_thickness=slice_thickness,
        slice_location=slice_location,
        tags=tags,
        pixel_data=pixel_array,
    )


def parse_dicom_file(filepath: str) -> DICOMDataset:
    """Reads and parses DICOM file from filesystem."""
    with open(filepath, "rb") as f:
        content = f.read()
    return parse_dicom_bytes(content)
