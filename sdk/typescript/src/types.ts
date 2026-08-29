/**
 * HealthPulse AI — TypeScript SDK Type Definitions.
 */

export interface PatientVitalSigns {
  patient_id: string;
  timestamp: string;
  heart_rate: number;
  respiratory_rate: number;
  systolic_bp: number;
  diastolic_bp: number;
  mean_arterial_pressure: number;
  oxygen_saturation: number;
  temperature_celsius: number;
  is_alarm_triggered?: boolean;
}

export interface QSOFAResult {
  score: number;
  respiratory_rate_flag: boolean;
  altered_mentation_flag: boolean;
  systolic_bp_flag: boolean;
  is_high_risk: boolean;
  clinical_interpretation: string;
}

export interface DrugInteraction {
  drug_a: string;
  drug_b: string;
  severity: "contraindicated" | "major" | "moderate" | "minor" | "no_interaction";
  mechanism: string;
  clinical_effect: string;
  management_advice: string;
}

export interface CDSCard {
  summary: string;
  indicator: "info" | "warning" | "critical";
  source: {
    label: string;
    url?: string;
  };
  detail?: string;
  suggestions?: Array<{
    label: string;
    uuid?: string;
    actions: Array<{
      type: string;
      description: string;
    }>;
  }>;
}

export interface MerkleAuditBlock {
  index: number;
  timestamp: string;
  actor_id: string;
  role: string;
  action: string;
  resource_type: string;
  resource_id: string;
  patient_id?: string;
  is_break_glass: boolean;
  payload_hash: string;
  previous_hash: string;
  current_hash: string;
}
