"""
HealthPulse AI — Quantitative Radiology Feature Extraction & Morphology Analysis.
Extracts volumetric pulmonary nodule metrics, ground-glass opacity density, and cardiothoracic ratios.
"""

import math
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PulmonaryNoduleMetrics:
    volume_mm3: float
    max_diameter_mm: float
    mean_attenuation_hu: float
    calcification_pattern: str
    malignancy_risk_tier: str
    fleischner_society_recommendation: str


def estimate_nodule_volume_mm3(
    diameter_axial_max_mm: float,
    diameter_axial_min_mm: float,
    diameter_vertical_mm: float,
) -> float:
    """
    Estimates nodule volume using ellipsoid formula:
    V = (pi / 6) * d1 * d2 * d3
    """
    return round((math.pi / 6.0) * diameter_axial_max_mm * diameter_axial_min_mm * diameter_vertical_mm, 2)


def evaluate_pulmonary_nodule(
    diameter_max_mm: float,
    mean_hu: float,
    is_solid: bool,
    patient_high_risk: bool = False,
) -> PulmonaryNoduleMetrics:
    """
    Fleischner Society 2017 Guidelines for Management of Incidental Pulmonary Nodules.
    """
    vol = estimate_nodule_volume_mm3(diameter_max_mm, diameter_max_mm * 0.85, diameter_max_mm * 0.85)

    if mean_hu > 200:
        calc_pattern = "Benign Calcification (Central/Popcorn/Concentric)"
        risk = "Very Low / Benign"
        rec = "No routine CT follow-up required."
    elif diameter_max_mm < 6.0:
        calc_pattern = "Non-calcified"
        risk = "Low (<1%)"
        rec = "Optional CT at 12 months in high-risk patients; no follow-up needed for low risk." if is_solid else "No routine follow-up."
    elif 6.0 <= diameter_max_mm <= 8.0:
        calc_pattern = "Non-calcified"
        risk = "Intermediate (1-5%)"
        rec = "CT at 6-12 months, then at 18-24 months if stable."
    else:
        calc_pattern = "Non-calcified / Subsolid"
        risk = "High (>15%)"
        rec = "Consider chest CT at 3 months, PET/CT scan, or tissue biopsy."

    return PulmonaryNoduleMetrics(
        volume_mm3=vol,
        max_diameter_mm=round(diameter_max_mm, 1),
        mean_attenuation_hu=round(mean_hu, 1),
        calcification_pattern=calc_pattern,
        malignancy_risk_tier=risk,
        fleischner_society_recommendation=rec,
    )


def calculate_cardiothoracic_ratio(
    cardiac_transverse_diameter_mm: float,
    thoracic_internal_diameter_mm: float,
) -> Dict[str, Any]:
    """
    Calculates Cardiothoracic Ratio (CTR) on PA Chest Radiographs.
    Normal CTR <= 0.50. CTR > 0.50 indicates cardiomegaly.
    """
    if thoracic_internal_diameter_mm <= 0.0:
        return {"error": "Invalid thoracic diameter"}

    ctr = round(cardiac_transverse_diameter_mm / thoracic_internal_diameter_mm, 3)
    is_cardiomegaly = ctr > 0.50

    if ctr <= 0.50:
        sev = "Normal cardiac silhouette"
    elif 0.51 <= ctr <= 0.55:
        sev = "Mild cardiomegaly"
    elif 0.56 <= ctr <= 0.60:
        sev = "Moderate cardiomegaly"
    else:
        sev = "Severe cardiomegaly / Massive enlargement"

    return {
        "cardiothoracic_ratio": ctr,
        "is_cardiomegaly": is_cardiomegaly,
        "classification": sev,
        "cardiac_width_mm": cardiac_transverse_diameter_mm,
        "thoracic_width_mm": thoracic_internal_diameter_mm,
    }


def detect_ground_glass_attenuation(
    hu_pixels: List[float],
    total_lung_voxels: int,
) -> Dict[str, Any]:
    """
    Detects ground-glass opacity (GGO) characteristic of viral pneumonia (e.g. COVID-19/ARDS).
    GGO attenuation typically ranges from -700 HU to -300 HU without obscuring underlying bronchial/vascular margins.
    """
    ggo_count = sum(1 for val in hu_pixels if -700.0 <= val <= -300.0)
    consolidation_count = sum(1 for val in hu_pixels if -300.0 < val <= 50.0)
    
    total = max(1, total_lung_voxels)
    ggo_pct = round((ggo_count / total) * 100.0, 2)
    consol_pct = round((consolidation_count / total) * 100.0, 2)

    return {
        "ggo_voxel_count": ggo_count,
        "consolidation_voxel_count": consolidation_count,
        "ggo_involvement_percent": ggo_pct,
        "consolidation_involvement_percent": consol_pct,
        "severity_grade": (
            "Severe (>50% parenchymal involvement)"
            if (ggo_pct + consol_pct) > 50.0
            else (
                "Moderate (25-50% parenchymal involvement)"
                if (ggo_pct + consol_pct) >= 25.0
                else "Mild (<25% parenchymal involvement)"
            )
        ),
    }
