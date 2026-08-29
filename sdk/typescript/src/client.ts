/**
 * HealthPulse AI — TypeScript API Client Implementation.
 */

import { PatientVitalSigns, QSOFAResult, DrugInteraction, CDSCard, MerkleAuditBlock } from "./types.js";

export interface HealthPulseClientConfig {
  baseUrl: string;
  apiKey?: string;
}

export class HealthPulseClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(config: HealthPulseClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, "");
    this.apiKey = config.apiKey;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };

    if (this.apiKey) {
      headers["Authorization"] = `Bearer ${this.apiKey}`;
    }

    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      throw new Error(`HealthPulse API error: ${res.status} ${res.statusText}`);
    }
    return (await res.json()) as T;
  }

  public async getPatients(limit = 50, offset = 0) {
    return this.request<{ total: number; patients: any[] }>(`/api/v1/patients?limit=${limit}&offset=${offset}`);
  }

  public async calculateQSOFA(vitals: { respiratory_rate: number; gcs_score: number; systolic_bp: number }) {
    return this.request<QSOFAResult>("/api/v1/clinical/qsofa", {
      method: "POST",
      body: JSON.stringify(vitals),
    });
  }

  public async checkDrugInteractions(medications: string[]) {
    return this.request<{ interaction_count: number; interactions: DrugInteraction[] }>("/api/v1/clinical/ddi-check", {
      method: "POST",
      body: JSON.stringify({ medications }),
    });
  }

  public async getAuditLedger(limit = 50) {
    return this.request<{ is_chain_valid: boolean; total_blocks: number; recent_blocks: MerkleAuditBlock[] }>(
      `/api/v1/security/audit-ledger?limit=${limit}`
    );
  }
}
