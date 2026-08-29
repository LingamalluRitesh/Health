"use client";

import React, { useState } from "react";
import { Header } from "../../components/Header";
import { VitalWaveformChart } from "../../components/VitalWaveformChart";
import { SepsisRiskGauge } from "../../components/SepsisRiskGauge";
import { HeartAlert, BellRing, Activity, ShieldAlert, Check } from "lucide-react";

export default function ICUPage() {
  const [activeBed, setActiveBed] = useState("BED-04");

  const beds = [
    { bed: "BED-01", patient: "John Doe", mrn: "MRN-11029", hr: 72, bp: "120/80", spo2: 99, status: "stable", sofa: 0 },
    { bed: "BED-02", patient: "James Robertson", mrn: "MRN-55410", hr: 98, bp: "105/68", spo2: 95, status: "warning", sofa: 3 },
    { bed: "BED-03", patient: "Maria Garcia", mrn: "MRN-66421", hr: 68, bp: "128/82", spo2: 98, status: "stable", sofa: 1 },
    { bed: "BED-04", patient: "Eleanor Vance", mrn: "MRN-88231", hr: 118, bp: "88/55", spo2: 93, status: "critical", sofa: 4 },
  ];

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Intensive Care Unit (ICU) Real-Time Central Telemetry Center"
        subtitle="Continuous multi-bed waveform surveillance and automated deterioration alerts"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Bed Grid Selector */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {beds.map((b) => (
            <button
              key={b.bed}
              onClick={() => setActiveBed(b.bed)}
              className={`p-4 rounded-xl border text-left transition-all ${
                activeBed === b.bed
                  ? "border-emerald-500 bg-emerald-950/40 ring-1 ring-emerald-500"
                  : b.status === "critical"
                  ? "border-rose-900/80 bg-rose-950/20"
                  : "border-slate-800 bg-slate-900 hover:border-slate-700"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-sm text-white font-mono">{b.bed}</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                    b.status === "critical"
                      ? "bg-rose-900 text-rose-200 animate-pulse"
                      : b.status === "warning"
                      ? "bg-amber-900 text-amber-200"
                      : "bg-emerald-900 text-emerald-200"
                  }`}
                >
                  {b.status}
                </span>
              </div>
              <div className="mt-2 text-xs font-semibold text-slate-200 truncate">{b.patient}</div>
              <div className="text-[11px] font-mono text-slate-400">{b.mrn}</div>

              <div className="mt-3 pt-2 border-t border-slate-800 flex justify-between text-xs font-mono">
                <span className="text-emerald-400">HR: {b.hr}</span>
                <span className="text-blue-400">SpO2: {b.spo2}%</span>
                <span className={b.sofa >= 2 ? "text-rose-400 font-bold" : "text-slate-400"}>
                  SOFA: {b.sofa}
                </span>
              </div>
            </button>
          ))}
        </div>

        {/* Selected Bed Active Waveform Stream */}
        <VitalWaveformChart />

        {/* Sepsis Surveillance & Resuscitation Gauge */}
        <SepsisRiskGauge sofaScore={4} qsofaScore={2} lactateMmolL={2.8} predictedProbabilityPct={84} />
      </div>
    </main>
  );
}
