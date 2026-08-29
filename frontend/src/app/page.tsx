"use client";

import React from "react";
import { Header } from "../components/Header";
import { MetricCard } from "../components/MetricCard";
import { VitalWaveformChart } from "../components/VitalWaveformChart";
import { SepsisRiskGauge } from "../components/SepsisRiskGauge";
import { CDSHooksCard } from "../components/CDSHooksCard";
import {
  Users,
  Activity,
  HeartAlert,
  ShieldCheck,
  Zap,
  TrendingUp,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Hospital Network Clinical Intelligence Overview"
        subtitle="Real-time multi-unit clinical surveillance and predictive risk intelligence"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Metric Cards Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Active Inpatient Census"
            value="142"
            subtitle="Across 6 Clinical Units"
            change="+4 today"
            isPositive={true}
            icon={Users}
            variant="info"
          />
          <MetricCard
            title="ICU Sepsis Alerts"
            value="3"
            subtitle="1-Hour Resuscitation Active"
            change="Action Required"
            isPositive={false}
            icon={Activity}
            variant="danger"
          />
          <MetricCard
            title="AI Model AUROC"
            value="0.912"
            subtitle="FDA SaMD Class II Certified"
            change="Optimal"
            isPositive={true}
            icon={ShieldCheck}
            variant="success"
          />
          <MetricCard
            title="Telemetry Data Stream"
            value="1,240 /s"
            subtitle="Latency: 14ms (p99)"
            change="Real-time"
            isPositive={true}
            icon={Zap}
            variant="default"
          />
        </div>

        {/* Live ICU Sepsis Alert Banner (CDS Hooks) */}
        <CDSHooksCard
          summary="CRITICAL: Sepsis Early Warning Alert for Bed 04 (SOFA: 4, qSOFA: 2)"
          indicator="critical"
          source={{
            label: "Surviving Sepsis Campaign 2024 Guideline Engine",
            url: "https://healthpulse.ai/guidelines/sepsis-3",
          }}
          detail="Patient Eleanor Vance (P-100234) in ICU-East exhibits acute physiological decompensation: RR 26 bpm, MAP 62 mmHg, Serum Lactate 2.8 mmol/L. Initiate 1-Hour Sepsis Resuscitation Bundle immediately."
          suggestions={[
            {
              label: "Execute 1-Hour Sepsis Resuscitation Bundle",
              actions: [
                { type: "create", description: "Order Serum Lactate STAT" },
                { type: "create", description: "Order Blood Cultures x 2 STAT" },
                { type: "create", description: "Initiate IV Piperacillin/Tazobactam 4.5g q6h" },
              ],
            },
          ]}
        />

        {/* Real-time ICU ECG & Waveforms */}
        <VitalWaveformChart />

        {/* Sepsis Gauge & Resuscitation Checklist */}
        <SepsisRiskGauge
          sofaScore={4}
          qsofaScore={2}
          lactateMmolL={2.8}
          predictedProbabilityPct={84}
        />
      </div>
    </main>
  );
}
