"""
HealthPulse AI — Medical Imaging & DICOM Processing API Endpoints.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from backend.imaging.windowing import apply_voi_lut_window, convert_to_hounsfield_units, get_tissue_density_classification
from backend.imaging.radiology_features import calculate_cardiothoracic_ratio, evaluate_pulmonary_nodule, detect_ground_glass_attenuation


router = APIRouter()


class NoduleEvalSchema(BaseModel):
    max_diameter_mm: float = Field(..., example=8.5)
    mean_hu: float = Field(..., example=-120.0)
    is_solid: bool = Field(True, example=True)
    patient_high_risk: bool = Field(True, example=True)


class CTRSchema(BaseModel):
    cardiac_diameter_mm: float = Field(..., example=165.0)
    thoracic_diameter_mm: float = Field(..., example=300.0)


class WindowingSchema(BaseModel):
    raw_pixels: List[int] = Field(..., example=[100, 200, 300, 400, 500])
    rescale_slope: float = Field(1.0, example=1.0)
    rescale_intercept: float = Field(-1024.0, example=-1024.0)
    window_center: float = Field(40.0, example=40.0)
    window_width: float = Field(400.0, example=400.0)


@router.post("/nodule-evaluate")
def evaluate_nodule(payload: NoduleEvalSchema):
    res = evaluate_pulmonary_nodule(
        diameter_max_mm=payload.max_diameter_mm,
        mean_hu=payload.mean_hu,
        is_solid=payload.is_solid,
        patient_high_risk=payload.patient_high_risk,
    )
    return res.__dict__


@router.post("/cardiothoracic-ratio")
def compute_ctr(payload: CTRSchema):
    return calculate_cardiothoracic_ratio(payload.cardiac_diameter_mm, payload.thoracic_diameter_mm)


@router.post("/window-transform")
def window_transform(payload: WindowingSchema):
    hu_pixels = convert_to_hounsfield_units(payload.raw_pixels, payload.rescale_slope, payload.rescale_intercept)
    rendered = apply_voi_lut_window(hu_pixels, payload.window_center, payload.window_width)
    return {
        "hu_pixels": hu_pixels,
        "grayscale_8bit": rendered,
        "sample_tissue_type": get_tissue_density_classification(hu_pixels[0] if hu_pixels else 0.0),
    }
