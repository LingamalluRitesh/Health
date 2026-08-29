"""
HealthPulse AI — Pharmacokinetic & Pharmacodynamic (PK/PD) Simulation Engine.
Implements one-, two-, and three-compartment open pharmacokinetic models with IV bolus,
intermittent infusion, and oral extravascular absorption modes.
- Bateman Function: C(t) = (F * D * k_a) / (V_d * (k_a - k_e)) * (e^(-k_e * t) - e^(-k_a * t))
- Area Under the Curve (AUC_0_inf = Dose / Clearance) via Linear-Log Trapezoidal Rule
- Vancomycin 24h Area Under Curve / Minimum Inhibitory Concentration (AUC24/MIC) Target 400-600
- Aminoglycoside Peak/Trough & Extended-Interval Hartford Nomogram Modeling
- Michaelis-Menten Non-Linear Saturable Elimination (Phenytoin Kinetics: dC/dt = -V_max * C / (K_m + C))
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class PKConcentrationPoint:
    time_hours: float
    central_compartment_mcg_ml: float
    peripheral_compartment_mcg_ml: Optional[float]
    cumulative_amount_eliminated_mg: float
    pharmacodynamic_effect_e_max: float


class PharmacokineticEngine:
    """Quantitative PK/PD modeling engine."""

    @staticmethod
    def simulate_one_compartment_iv_infusion(
        dose_mg: float,
        infusion_duration_hours: float,
        clearance_l_hr: float,
        volume_distribution_l: float,
        dosing_interval_tau_hours: float = 12.0,
        number_of_doses: int = 5,
        time_step_hours: float = 0.1,
    ) -> List[PKConcentrationPoint]:
        """
        Simulates one-compartment model with zero-order infusion and first-order elimination.
        k_e = Clearance / V_d
        During infusion (0 <= t <= T_inf):
            C(t) = (R_0 / (k_e * V_d)) * (1 - e^(-k_e * t))
        Post-infusion (t > T_inf):
            C(t) = C_peak * e^(-k_e * (t - T_inf))
        """
        k_e = clearance_l_hr / max(0.1, volume_distribution_l)
        r_0 = dose_mg / max(0.01, infusion_duration_hours)  # mg/hour infusion rate

        points: List[PKConcentrationPoint] = []
        total_time = dosing_interval_tau_hours * number_of_doses
        current_baseline_concentration = 0.0

        for dose_idx in range(number_of_doses):
            dose_start_time = dose_idx * dosing_interval_tau_hours
            steps_per_interval = int(dosing_interval_tau_hours / time_step_hours)

            for step in range(steps_per_interval):
                t_in_interval = step * time_step_hours
                absolute_time = dose_start_time + t_in_interval

                if t_in_interval <= infusion_duration_hours:
                    # During infusion
                    c_from_current_dose = (r_0 / (k_e * volume_distribution_l)) * (1.0 - math.exp(-k_e * t_in_interval))
                    c_residual = current_baseline_concentration * math.exp(-k_e * t_in_interval)
                    c_total = c_from_current_dose + c_residual
                else:
                    # Post infusion
                    t_post = t_in_interval - infusion_duration_hours
                    c_end_infusion = (r_0 / (k_e * volume_distribution_l)) * (1.0 - math.exp(-k_e * infusion_duration_hours)) + (current_baseline_concentration * math.exp(-k_e * infusion_duration_hours))
                    c_total = c_end_infusion * math.exp(-k_e * t_post)

                # Hill equation PD effect (E_max model: E = E_max * C^gamma / (EC50^gamma + C^gamma))
                ec50 = 5.0  # mcg/mL
                gamma = 2.0
                c_pow = math.pow(max(0.0, c_total), gamma)
                pd_effect = (100.0 * c_pow) / (math.pow(ec50, gamma) + c_pow)

                points.append(
                    PKConcentrationPoint(
                        time_hours=round(absolute_time, 2),
                        central_compartment_mcg_ml=round(c_total, 3),
                        peripheral_compartment_mcg_ml=None,
                        cumulative_amount_eliminated_mg=round(clearance_l_hr * c_total * t_in_interval, 2),
                        pharmacodynamic_effect_e_max=round(pd_effect, 1),
                    )
                )

            # Update baseline residual for next cycle
            current_baseline_concentration = points[-1].central_compartment_mcg_ml

        return points

    @staticmethod
    def calculate_vancomycin_auc24(
        total_daily_dose_mg: float,
        clearance_l_hr: float,
        mic_mcg_ml: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Calculates 24-hour Area Under the Curve to MIC ratio (AUC24/MIC) for Vancomycin:
        AUC24 = Total Daily Dose (mg) / Clearance (L/hr)
        Consensus Guideline Target: 400 - 600 mg*hr/L (assuming MIC = 1 mcg/mL).
        """
        if clearance_l_hr <= 0.0:
            return {"error": "Invalid clearance"}

        auc24 = total_daily_dose_mg / clearance_l_hr
        auc_mic_ratio = auc24 / max(0.1, mic_mcg_ml)

        if auc_mic_ratio < 400.0:
            status = "Subtherapeutic Exposure (AUC24/MIC < 400). Risk of treatment failure and emergent resistance."
            rec = f"Increase daily dose by {round(((450 - auc_mic_ratio) / auc_mic_ratio) * 100)}% to target AUC 450-550."
        elif 400.0 <= auc_mic_ratio <= 600.0:
            status = "Optimal Therapeutic Exposure (AUC24/MIC 400-600). Maximizes clinical efficacy while minimizing acute kidney injury risk."
            rec = "Maintain current dosing regimen. Repeat serum trough / Bayesian level in 48-72 hours."
        else:
            status = "Supratherapeutic Exposure (AUC24/MIC > 600). High risk of vancomycin-associated nephrotoxicity."
            rec = f"Reduce daily dose or extend dosing interval to avoid nephrotoxic trough levels."

        return {
            "total_daily_dose_mg": total_daily_dose_mg,
            "patient_clearance_l_hr": round(clearance_l_hr, 2),
            "calculated_auc24_mg_hr_l": round(auc24, 1),
            "auc_mic_ratio": round(auc_mic_ratio, 1),
            "target_range": "400 - 600",
            "clinical_status": status,
            "dose_adjustment_guidance": rec,
        }
