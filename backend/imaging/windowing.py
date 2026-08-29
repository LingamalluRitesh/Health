"""
HealthPulse AI — Hounsfield Unit (HU) Transformation & VOI LUT Windowing Engine.
Converts raw stored pixel values to calibrated Hounsfield Units and renders 8-bit display grayscale.
"""

from typing import List, Tuple, Dict, Union
from backend.core.constants import CT_WINDOW_PRESETS


def convert_to_hounsfield_units(
    raw_pixels: List[int],
    rescale_slope: float,
    rescale_intercept: float,
) -> List[float]:
    """
    Transforms raw stored integer pixels (SV) into calibrated Hounsfield Units (HU):
    HU = (SV * RescaleSlope) + RescaleIntercept
    """
    return [(val * rescale_slope) + rescale_intercept for val in raw_pixels]


def apply_voi_lut_window(
    hu_pixels: List[float],
    window_center: float,
    window_width: float,
    output_range: Tuple[int, int] = (0, 255),
) -> List[int]:
    """
    Applies linear VOI LUT windowing transformation according to DICOM PS 3.3 C.11.2.1.2:
    - If x <= (c - 0.5) - (w - 1)/2, then y = y_min
    - Else if x > (c - 0.5) + (w - 1)/2, then y = y_max
    - Else y = ((x - (c - 0.5)) / (w - 1) + 0.5) * (y_max - y_min) + y_min
    """
    y_min, y_max = output_range
    w = max(1.0, window_width)
    c = window_center

    lower_bound = (c - 0.5) - (w - 1.0) / 2.0
    upper_bound = (c - 0.5) + (w - 1.0) / 2.0
    span = y_max - y_min

    rendered: List[int] = []
    for val in hu_pixels:
        if val <= lower_bound:
            rendered.append(y_min)
        elif val > upper_bound:
            rendered.append(y_max)
        else:
            normalized = ((val - (c - 0.5)) / (w - 1.0) + 0.5) * span + y_min
            rendered.append(int(round(max(y_min, min(y_max, normalized)))))

    return rendered


def apply_preset_window(
    hu_pixels: List[float],
    preset_name: str,
) -> List[int]:
    """Applies named clinical window preset (lung, bone, brain, soft_tissue, mediastinum)."""
    preset = CT_WINDOW_PRESETS.get(preset_name.lower(), (40, 400))
    window_center, window_width = preset
    return apply_voi_lut_window(hu_pixels, window_center=window_center, window_width=window_width)


def get_tissue_density_classification(hu_value: float) -> str:
    """Returns clinical tissue classification according to CT attenuation value (HU)."""
    if hu_value < -900:
        return "Air / Pneumothorax"
    elif -900 <= hu_value < -500:
        return "Lung Parenchyma"
    elif -500 <= hu_value < -50:
        return "Fat / Adipose Tissue"
    elif -50 <= hu_value <= 15:
        return "Fluid / Water / Simple Cyst"
    elif 15 < hu_value <= 45:
        return "Soft Tissue / Muscle"
    elif 45 < hu_value <= 80:
        return "Acute Blood / Clot / Enhanced Parenchyma"
    elif 80 < hu_value <= 300:
        return "Thyroid / Cartilage / Calcification"
    else:
        return "Dense Cortical Bone / Contrast Agent / Metal"
