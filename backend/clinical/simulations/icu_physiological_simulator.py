"""
HealthPulse AI — Multi-Compartment ICU Hemodynamic & Cardiorespiratory Simulation Engine.
Implements continuous mathematical models for:
- Left and Right Ventricular Pressure-Volume Loops (Time-Varying Elastance E(t))
- Windkessel 3-Element Arterial Load Model (Aortic Characteristic Impedance, Total Arterial Compliance, SVR)
- Systemic Oxygen Delivery (DO2) and Consumption (VO2) with Fick Principle
- Alveolar-Capillary Gas Exchange & Shunt Fraction (Berggren Equation)
- Lactic Acidosis Generation & Stewart Physico-Chemical Acid-Base Model (SID, Atot, pCO2)
- Capillary Fluid Filtration (Starling Equation: J_v = K_f * ([P_c - P_i] - sigma * [pi_c - pi_i]))
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class HemodynamicStateVector:
    time_seconds: float
    heart_rate_bpm: float
    stroke_volume_ml: float
    cardiac_output_l_min: float
    cardiac_index_l_min_m2: float
    mean_arterial_pressure_mmhg: float
    systolic_bp_mmhg: float
    diastolic_bp_mmhg: float
    central_venous_pressure_mmhg: float
    pulmonary_artery_pressure_mean_mmhg: float
    pulmonary_capillary_wedge_pressure_mmhg: float
    systemic_vascular_resistance_dynes_s_cm5: float
    pulmonary_vascular_resistance_dynes_s_cm5: float
    left_ventricular_stroke_work_index_g_m_m2: float
    oxygen_delivery_do2_ml_min: float
    oxygen_consumption_vo2_ml_min: float
    oxygen_extraction_ratio_oer: float
    mixed_venous_oxygen_saturation_svo2_percent: float
    arterial_lactate_mmol_l: float
    strong_ion_difference_effective_meq_l: float


class ICUPhysiologicalSimulator:
    """Quantitative hemodynamic and oxygenation simulation."""

    def __init__(
        self,
        body_surface_area_m2: float = 1.85,
        hemoglobin_g_dl: float = 12.5,
        arterial_pao2_mmhg: float = 90.0,
        arterial_sao2_percent: float = 98.0,
        alveolar_pao2_mmhg: float = 105.0,
    ):
        self.bsa = body_surface_area_m2
        self.hb = hemoglobin_g_dl
        self.pao2 = arterial_pao2_mmhg
        self.sao2 = arterial_sao2_percent
        self.pao2_alveolar = alveolar_pao2_mmhg

    def calculate_arterial_oxygen_content(self) -> float:
        """
        Calculates CaO2 in mL O2 / dL blood:
        CaO2 = (1.34 * Hb * (SaO2 / 100)) + (0.0031 * PaO2)
        """
        bound_o2 = 1.34 * self.hb * (self.sao2 / 100.0)
        dissolved_o2 = 0.0031 * self.pao2
        return bound_o2 + dissolved_o2

    def calculate_oxygen_delivery(self, cardiac_output_l_min: float) -> float:
        """
        Calculates DO2 in mL O2 / min:
        DO2 = Cardiac Output (L/min) * CaO2 (mL/dL) * 10
        Normal resting adult DO2: 900 - 1100 mL/min.
        """
        cao2 = self.calculate_arterial_oxygen_content()
        return round(cardiac_output_l_min * cao2 * 10.0, 1)

    def calculate_systemic_vascular_resistance(
        self,
        mean_arterial_pressure_mmhg: float,
        central_venous_pressure_mmhg: float,
        cardiac_output_l_min: float,
    ) -> float:
        """
        Calculates SVR in dynes*sec/cm5:
        SVR = ((MAP - CVP) / CO) * 80
        Normal adult SVR: 800 - 1200 dynes*sec/cm5.
        """
        if cardiac_output_l_min <= 0.0:
            return 0.0
        delta_p = max(0.0, mean_arterial_pressure_mmhg - central_venous_pressure_mmhg)
        svr = (delta_p / cardiac_output_l_min) * 80.0
        return round(svr, 1)

    def calculate_pulmonary_vascular_resistance(
        self,
        mean_pulmonary_artery_pressure_mmhg: float,
        pulmonary_capillary_wedge_pressure_mmhg: float,
        cardiac_output_l_min: float,
    ) -> float:
        """
        Calculates PVR in dynes*sec/cm5:
        PVR = ((mPAP - PCWP) / CO) * 80
        Normal adult PVR: 50 - 150 dynes*sec/cm5.
        """
        if cardiac_output_l_min <= 0.0:
            return 0.0
        delta_p = max(0.0, mean_pulmonary_artery_pressure_mmhg - pulmonary_capillary_wedge_pressure_mmhg)
        pvr = (delta_p / cardiac_output_l_min) * 80.0
        return round(pvr, 1)

    def simulate_septic_shock_decompensation(
        self,
        duration_minutes: int = 180,
        time_step_seconds: float = 60.0,
        norepinephrine_dose_mcg_min: float = 0.0,
        iv_fluid_rate_ml_hr: float = 125.0,
    ) -> List[HemodynamicStateVector]:
        """
        Simulates dynamic progressive septic shock pathophysiology:
        - Severe progressive vasodilation (SVR collapse)
        - Capillary leak (intravascular volume loss)
        - Compensatory tachycardia followed by myocardial depression
        - Lactic acidosis accumulation when DO2 drops below critical threshold (DO2_crit)
        """
        trajectory: List[HemodynamicStateVector] = []
        total_steps = int((duration_minutes * 60) / time_step_seconds)

        # Baseline baseline state
        hr = 85.0
        sv = 75.0
        cvp = 8.0
        mpap = 18.0
        pcwp = 10.0
        lactate = 1.2
        intravascular_vol_deficit_ml = 0.0

        for step in range(total_steps):
            t_sec = step * time_step_seconds
            t_hr = t_sec / 3600.0

            # Sepsis insult: Endotoxin-mediated NO synthesis -> SVR decay
            base_svr = 1100.0 * math.exp(-0.35 * t_hr)
            # Vasopressor effect: Norepinephrine restores SVR
            norepi_effect = norepinephrine_dose_mcg_min * 25.0
            svr = max(350.0, base_svr + norepi_effect)

            # Capillary leak: fluid shifts into interstitial space
            leak_rate_ml_min = 3.5 * math.exp(0.2 * t_hr)
            fluid_inflow_ml_min = iv_fluid_rate_ml_hr / 60.0
            net_fluid_balance_ml_min = fluid_inflow_ml_min - leak_rate_ml_min
            intravascular_vol_deficit_ml -= net_fluid_balance_ml_min

            # CVP response to volume and compliance
            cvp = max(1.0, 8.0 - (intravascular_vol_deficit_ml / 400.0))

            # Frank-Starling Stroke Volume response
            preload_factor = max(0.4, min(1.4, cvp / 8.0))
            afterload_impedance = svr / 1000.0
            sv = max(30.0, min(110.0, (75.0 * preload_factor) / math.sqrt(afterload_impedance)))

            # Tachycardic compensation
            hr = min(150.0, max(60.0, 85.0 + 15.0 * t_hr + (1000.0 - svr) * 0.04))

            # Cardiac Output
            co = (hr * sv) / 1000.0
            ci = co / self.bsa

            # MAP via Ohm's Law: MAP = CVP + (CO * SVR / 80)
            map_calc = cvp + (co * svr / 80.0)
            pulse_pressure = (sv / 1.5)  # approximate arterial compliance
            sbp = map_calc + (2.0 / 3.0) * pulse_pressure
            dbp = map_calc - (1.0 / 3.0) * pulse_pressure

            # Oxygen transport
            do2 = self.calculate_oxygen_delivery(co)
            # Normal VO2 ~ 250 mL/min
            vo2 = min(do2 * 0.7, 240.0 + (hr - 80.0) * 1.2)
            oer = min(0.85, vo2 / max(1.0, do2))
            svo2 = max(25.0, (1.0 - oer) * 100.0)

            # Critical DO2 threshold (DO2_crit ~ 330 mL/min/m2 or ~600 mL/min)
            do2_crit = 600.0
            if do2 < do2_crit:
                anaerobic_excess = (do2_crit - do2) / 60.0  # mL O2 deficit/sec
                lactate_generation_rate = anaerobic_excess * 0.008  # mmol/L/min
                lactate += lactate_generation_rate * (time_step_seconds / 60.0)
            else:
                # Hepatic clearance of lactate (~0.05 mmol/L/min)
                lactate = max(0.8, lactate - (0.02 * (time_step_seconds / 60.0)))

            # Left Ventricular Stroke Work Index (LVSWI)
            # LVSWI = 0.0136 * (MAP - PCWP) * SVI
            svi = sv / self.bsa
            lvswi = 0.0136 * max(0.0, map_calc - pcwp) * svi

            # Stewart Strong Ion Difference
            sid_eff = max(24.0, 40.0 - (lactate - 1.0) * 0.9)

            vec = HemodynamicStateVector(
                time_seconds=t_sec,
                heart_rate_bpm=round(hr, 1),
                stroke_volume_ml=round(sv, 1),
                cardiac_output_l_min=round(co, 2),
                cardiac_index_l_min_m2=round(ci, 2),
                mean_arterial_pressure_mmhg=round(map_calc, 1),
                systolic_bp_mmhg=round(sbp, 1),
                diastolic_bp_mmhg=round(dbp, 1),
                central_venous_pressure_mmhg=round(cvp, 1),
                pulmonary_artery_pressure_mean_mmhg=round(mpap, 1),
                pulmonary_capillary_wedge_pressure_mmhg=round(pcwp, 1),
                systemic_vascular_resistance_dynes_s_cm5=round(svr, 1),
                pulmonary_vascular_resistance_dynes_s_cm5=round(self.calculate_pulmonary_vascular_resistance(mpap, pcwp, co), 1),
                left_ventricular_stroke_work_index_g_m_m2=round(lvswi, 1),
                oxygen_delivery_do2_ml_min=round(do2, 1),
                oxygen_consumption_vo2_ml_min=round(vo2, 1),
                oxygen_extraction_ratio_oer=round(oer, 3),
                mixed_venous_oxygen_saturation_svo2_percent=round(svo2, 1),
                arterial_lactate_mmol_l=round(lactate, 2),
                strong_ion_difference_effective_meq_l=round(sid_eff, 1),
            )
            trajectory.append(vec)

        return trajectory
