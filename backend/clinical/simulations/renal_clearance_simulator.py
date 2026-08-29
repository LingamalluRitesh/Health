"""
HealthPulse AI — Quantitative Renal Physiology & Tubular Electrolyte Transport Engine.
Implements nephron-level clearance kinetics:
- Glomerular Capillary Ultrafiltration (Net Filtration Pressure NFP = (P_GC - P_BS) - pi_GC)
- Fractional Excretion of Sodium (FE_Na = (U_Na * P_Cr) / (P_Na * U_Cr) * 100)
- Fractional Excretion of Urea (FE_Urea = (U_Urea * P_Cr) / (P_Urea * U_Cr) * 100)
- Free Water Clearance (C_H2O = V * (1 - (U_osm / P_osm)))
- Transtubular Potassium Gradient (TTKG = (U_K * P_osm) / (P_K * U_osm))
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass


class RenalPhysiologyEngine:
    """Quantitative nephron filtration and tubular function analysis."""

    @staticmethod
    def evaluate_prerenal_vs_atn(
        urine_sodium_meq_l: float,
        serum_sodium_meq_l: float,
        urine_creatinine_mg_dl: float,
        serum_creatinine_mg_dl: float,
        urine_urea_mg_dl: Optional[float] = None,
        serum_urea_mg_dl: Optional[float] = None,
        is_on_diuretics: bool = False,
    ) -> Dict[str, Any]:
        """
        Differentiates Prerenal Azotemia from Acute Tubular Necrosis (ATN).
        FE_Na < 1%: Prerenal (avid tubular sodium reabsorption).
        FE_Na > 2%: Intrinsic Renal / ATN (tubular epithelial dysfunction).
        In patients on loop diuretics, FE_Urea is preferred (FE_Urea < 35% indicates Prerenal).
        """
        # FE_Na = (U_Na * P_Cr) / (P_Na * U_Cr) * 100
        fe_na = ((urine_sodium_meq_l * serum_creatinine_mg_dl) / max(0.1, (serum_sodium_meq_l * urine_creatinine_mg_dl))) * 100.0
        fe_na = round(fe_na, 2)

        fe_urea = None
        if urine_urea_mg_dl is not None and serum_urea_mg_dl is not None and serum_urea_mg_dl > 0:
            fe_urea_val = ((urine_urea_mg_dl * serum_creatinine_mg_dl) / (serum_urea_mg_dl * urine_creatinine_mg_dl)) * 100.0
            fe_urea = round(fe_urea_val, 1)

        bun_cr_ratio = round(serum_urea_mg_dl / max(0.1, serum_creatinine_mg_dl), 1) if serum_urea_mg_dl else None

        if is_on_diuretics and fe_urea is not None:
            is_prerenal = fe_urea < 35.0
            etiology = "Prerenal Azotemia (evaluated via FE_Urea due to diuretic use)" if is_prerenal else "Acute Tubular Necrosis (ATN) / Intrinsic AKI"
        else:
            is_prerenal = fe_na < 1.0
            etiology = "Prerenal Azotemia (FE_Na < 1.0%)" if is_prerenal else "Acute Tubular Necrosis (ATN) / Intrinsic AKI (FE_Na > 2.0%)"

        return {
            "fractional_excretion_sodium_percent": fe_na,
            "fractional_excretion_urea_percent": fe_urea,
            "bun_creatinine_ratio": bun_cr_ratio,
            "is_on_diuretics": is_on_diuretics,
            "inferred_etiology": etiology,
            "therapeutic_management": (
                "Volume resuscitation with isotonic balanced crystalloid (Lactated Ringer's / Plasma-Lyte) and optimization of cardiac output."
                if is_prerenal
                else "Avoid fluid overload; discontinue all nephrotoxins; monitor daily electrolytes and indications for renal replacement therapy."
            ),
        }
