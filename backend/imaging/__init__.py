"""
HealthPulse AI — Medical Imaging Intelligence and DICOM Processing Module.
Provides DICOM parsing, Hounsfield Unit windowing, 3D volumetric MPR, and radiology feature extraction.
"""

from backend.imaging.dicom_parser import (
    DICOMDataset,
    DICOMTag,
    parse_dicom_file,
    parse_dicom_bytes,
)
from backend.imaging.windowing import (
    apply_voi_lut_window,
    convert_to_hounsfield_units,
    CT_WINDOW_PRESETS,
)
from backend.imaging.volumetric_mpr import (
    VolumetricSeries,
    MultiPlanarReconstructor,
    PlaneType,
)
from backend.imaging.radiology_features import (
    calculate_cardiothoracic_ratio,
    estimate_nodule_volume_mm3,
    detect_ground_glass_attenuation,
)
from backend.imaging.dicomweb_client import (
    DICOMWebClient,
    WADORSQuery,
)
from backend.imaging.segmentation_metrics import (
    calculate_dice_coefficient,
    calculate_jaccard_index,
    calculate_hausdorff_distance_approx,
)

__all__ = [
    "DICOMDataset",
    "DICOMTag",
    "parse_dicom_file",
    "parse_dicom_bytes",
    "apply_voi_lut_window",
    "convert_to_hounsfield_units",
    "CT_WINDOW_PRESETS",
    "VolumetricSeries",
    "MultiPlanarReconstructor",
    "PlaneType",
    "calculate_cardiothoracic_ratio",
    "estimate_nodule_volume_mm3",
    "detect_ground_glass_attenuation",
    "DICOMWebClient",
    "WADORSQuery",
    "calculate_dice_coefficient",
    "calculate_jaccard_index",
    "calculate_hausdorff_distance_approx",
]
