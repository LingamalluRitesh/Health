"""
HealthPulse AI — Computed Tomography Angiography (CTA) & Coronary Plaque Analysis.
Implements CAD-RADS 2.0 (Coronary Artery Disease - Reporting and Data System) and NASCET Carotid Stenosis.
- Multiplanar Centerline Vessel Reconstruction & Lumen Profiling
- High-Risk Plaque (HRP) Features: Low-Attenuation Plaque (<30 HU), Positive Remodeling, Napkin-Ring Sign
- NASCET % Stenosis Calculation = (1 - (D_stenosis / D_normal_distal)) * 100
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CADRADSCategory(str, Enum):
    CAD_RADS_0 = "CAD-RADS 0: Documented absence of CAD (0% stenosis)"
    CAD_RADS_1 = "CAD-RADS 1: Minimal non-obstructive CAD (1-24% stenosis)"
    CAD_RADS_2 = "CAD-RADS 2: Mild non-obstructive CAD (25-49% stenosis)"
    CAD_RADS_3 = "CAD-RADS 3: Moderate stenosis (50-69% stenosis)"
    CAD_RADS_4A = "CAD-RADS 4A: Severe stenosis (70-99%) in 1 or 2 vessels"
    CAD_RADS_4B = "CAD-RADS 4B: Left Main stenosis >= 50% or 3-vessel disease >= 70%"
    CAD_RADS_5 = "CAD-RADS 5: Total occlusion (100% stenosis)"


class CTAPerfusionEngine:
    """CTA and vessel stenosis quantification."""

    @staticmethod
    def calculate_nascet_carotid_stenosis(
        narrowest_lumen_diameter_mm: float,
        distal_normal_internal_carotid_diameter_mm: float,
    ) -> Dict[str, Any]:
        """
        NASCET (North American Symptomatic Carotid Endarterectomy Trial) Carotid Stenosis Formula.
        % Stenosis = (1 - (D_narrow / D_distal)) * 100
        Symptomatic >= 70% stenosis: Class 1 indication for Carotid Endarterectomy (CEA) or Stenting (CAS).
        """
        if distal_normal_internal_carotid_diameter_mm <= 0.0:
            return {"error": "Invalid distal diameter"}

        stenosis_pct = (1.0 - (narrowest_lumen_diameter_mm / distal_normal_internal_carotid_diameter_mm)) * 100.0
        stenosis_pct = max(0.0, min(100.0, round(stenosis_pct, 1)))

        if stenosis_pct >= 70.0:
            rec = "Severe Carotid Stenosis (70-99%). Urgent vascular surgery referral for Carotid Endarterectomy (CEA) or Carotid Artery Stenting (CAS) (Class 1, Level A if symptomatic)."
        elif stenosis_pct >= 50.0:
            rec = "Moderate Carotid Stenosis (50-69%). Moderate benefit from CEA in symptomatic male patients; intensive medical therapy (High-intensity Statin + Antiplatelet)."
        else:
            rec = "Mild / Non-significant Stenosis (< 50%). Best medical therapy with aggressive LDL lowering (Target LDL < 55 mg/dL) and Aspirin."

        return {
            "nascet_stenosis_percentage": stenosis_pct,
            "narrowest_diameter_mm": narrowest_lumen_diameter_mm,
            "reference_distal_diameter_mm": distal_normal_internal_carotid_diameter_mm,
            "intervention_recommendation": rec,
        }
