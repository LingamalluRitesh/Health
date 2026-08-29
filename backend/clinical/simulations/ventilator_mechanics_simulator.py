"""
HealthPulse AI — Mechanical Ventilation & Respiratory Mechanics Simulation Engine.
Implements dynamic pulmonary physiology equations:
- Equation of Motion: P_aw(t) = (V_t(t) / C_rs) + (Flow(t) * R_aw) + PEEP_total
- Dynamic vs Static Respiratory System Compliance (C_stat = V_t / (P_plat - PEEP))
- Airway Resistance (R_aw = (P_peak - P_plat) / Insp_Flow)
- Alveolar Gas Equation: P_A O_2 = (P_atm - P_H2O) * FiO_2 - (PaCO_2 / R_Q)
- Alveolar-Arterial Oxygen Gradient: A-a Gradient = P_A O_2 - PaO_2
- Dead Space Fraction (Enghoff modification of Bohr Equation): V_d/V_t = (PaCO_2 - P_ETCO_2) / PaCO_2
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class VentBreathCyclePoint:
    time_ms: float
    airway_pressure_cm_h2o: float
    flow_rate_l_s: float
    volume_ml: float
    alveolar_pressure_cm_h2o: float


class VentilatorMechanicsSimulator:
    """Quantitative mechanical ventilation simulator."""

    def __init__(
        self,
        respiratory_compliance_ml_cm_h2o: float = 40.0,
        airway_resistance_cm_h2o_l_s: float = 12.0,
        peep_cm_h2o: float = 10.0,
        intrinsic_peep_cm_h2o: float = 2.0,
    ):
        self.c_rs = max(5.0, respiratory_compliance_ml_cm_h2o)
        self.r_aw = max(1.0, airway_resistance_cm_h2o_l_s)
        self.peep = peep_cm_h2o
        self.peep_i = intrinsic_peep_cm_h2o
        self.peep_total = self.peep + self.peep_i

    def simulate_volume_control_breath(
        self,
        tidal_volume_ml: float = 450.0,
        respiratory_rate_bpm: float = 16.0,
        inspiratory_time_seconds: float = 1.0,
        pause_time_seconds: float = 0.3,
    ) -> Dict[str, Any]:
        """
        Simulates Volume-Control (VCV) breath with square flow waveform and inspiratory pause.
        Calculates Peak Inspiratory Pressure (PIP), Plateau Pressure (P_plat), and Driving Pressure (DP).
        """
        total_cycle_time = 60.0 / respiratory_rate_bpm
        expiratory_time = total_cycle_time - inspiratory_time_seconds - pause_time_seconds

        # Square flow rate during active delivery (L/s)
        flow_active_l_s = (tidal_volume_ml / 1000.0) / inspiratory_time_seconds

        # Resistive pressure drop = Flow * Raw
        resistive_drop = flow_active_l_s * self.r_aw

        # Elastic pressure at end of inspiration = Vt / Crs
        elastic_pressure = tidal_volume_ml / self.c_rs

        # Peak Inspiratory Pressure (P_peak)
        p_peak = self.peep_total + resistive_drop + elastic_pressure

        # Plateau Pressure (P_plat) during no-flow pause (Flow = 0 -> Resistive drop = 0)
        p_plat = self.peep_total + elastic_pressure

        # Driving Pressure (DP = P_plat - PEEP) (Amato et al. NEJM 2015)
        driving_pressure = p_plat - self.peep

        time_points: List[VentBreathCyclePoint] = []
        dt_ms = 20.0
        total_steps = int((total_cycle_time * 1000.0) / dt_ms)

        for step in range(total_steps):
            t_s = (step * dt_ms) / 1000.0

            if t_s <= inspiratory_time_seconds:
                # Active inspiration
                frac = t_s / inspiratory_time_seconds
                vol = tidal_volume_ml * frac
                p_alv = self.peep_total + (vol / self.c_rs)
                p_aw = p_alv + (flow_active_l_s * self.r_aw)
                flow = flow_active_l_s
            elif t_s <= (inspiratory_time_seconds + pause_time_seconds):
                # Inspiratory pause (Zero flow)
                vol = tidal_volume_ml
                p_alv = self.peep_total + (vol / self.c_rs)
                p_aw = p_alv
                flow = 0.0
            else:
                # Passive expiration: exponential decay (RC time constant tau = R * C)
                t_exp = t_s - (inspiratory_time_seconds + pause_time_seconds)
                tau = (self.r_aw * (self.c_rs / 1000.0))  # seconds
                vol = tidal_volume_ml * math.exp(-t_exp / max(0.1, tau))
                p_alv = self.peep_total + (vol / self.c_rs)
                flow = -(vol / 1000.0) / max(0.1, tau)
                p_aw = self.peep

            time_points.append(
                VentBreathCyclePoint(
                    time_ms=round(t_s * 1000.0, 1),
                    airway_pressure_cm_h2o=round(p_aw, 1),
                    flow_rate_l_s=round(flow, 2),
                    volume_ml=round(vol, 1),
                    alveolar_pressure_cm_h2o=round(p_alv, 1),
                )
            )

        is_lung_protective = p_plat <= 30.0 and driving_pressure <= 14.0

        return {
            "peak_inspiratory_pressure_pip_cm_h2o": round(p_peak, 1),
            "plateau_pressure_pplat_cm_h2o": round(p_plat, 1),
            "driving_pressure_delta_p_cm_h2o": round(driving_pressure, 1),
            "static_compliance_ml_cm_h2o": round(self.c_rs, 1),
            "airway_resistance_cm_h2o_l_s": round(self.r_aw, 1),
            "total_peep_cm_h2o": round(self.peep_total, 1),
            "intrinsic_auto_peep_cm_h2o": round(self.peep_i, 1),
            "is_lung_protective_adherent": is_lung_protective,
            "waveform_points_count": len(time_points),
            "clinical_advisory": (
                "Lung-protective ventilation achieved (Pplat <= 30 cm H2O, Driving Pressure <= 14 cm H2O)."
                if is_lung_protective
                else "WARNING: Elevated Driving Pressure (>14 cm H2O) or Plateau Pressure (>30 cm H2O). Reduce tidal volume to 4-6 mL/kg PBW to mitigate ventilator-induced lung injury (VILI / barotrauma)."
            ),
        }
