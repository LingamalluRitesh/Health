"use client";

import React, { useState } from "react";
import { Header } from "../../../components/Header";
import { EHRTimeline, TimelineEvent } from "../../../components/EHRTimeline";
import { CDSHooksCard } from "../../../components/CDSHooksCard";
import { VitalWaveformChart } from "../../../components/VitalWaveformChart";
import { SepsisRiskGauge } from "../../../components/SepsisRiskGauge";
import { CLINICAL_PHARMACOPEIA } from "../../../lib/pharmacopeia";
import {
  User,
  Heart,
  Pill,
  FileText,
  Dna,
  ShieldCheck,
  AlertTriangle,
} from "lucide-react";

export function generateStaticParams() {
  return [
    { id: "P-100234" },
    { id: "P-100235" },
    { id: "P-100236" },
    { id: "P-100237" },
  ];
}

export default function PatientDetailPage({ params }: { params: { id: string } }) {
  const [activeTab, setActiveTab] = useState<"overview" | "timeline" | "medications" | "genomics">("overview");

  const timelineEvents: TimelineEvent[] = [
    {
      id: "evt-1",
      timestamp: "2026-08-29 10:30 UTC",
      category: "alert",
      title: "Sepsis Early Warning Triggered",
      description: "qSOFA score increased to 2 (RR 26 bpm, SBP 88 mmHg). Lactate elevated at 2.8 mmol/L.",
      provider: "HealthPulse Automated AI Engine",
      badgeText: "STAT REVIEW",
      badgeVariant: "danger",
    },
    {
      id: "evt-2",
      timestamp: "2026-08-29 08:00 UTC",
      category: "medication",
      title: "Medication Administered",
      description: "Piperacillin / Tazobactam 4.5g IV piggyback extended infusion over 4 hours.",
      provider: "Nurse J. Martinez, RN",
    },
    {
      id: "evt-3",
      timestamp: "2026-08-28 22:15 UTC",
      category: "encounter",
      title: "Admitted to Intensive Care Unit",
      description: "Admitted from Emergency Department with acute septic state and fever.",
      provider: "Dr. Sarah Jenkins, MD",
    },
  ];

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title={`Patient 360 EHR: Eleanor Vance (${params.id || "P-100234"})`}
        subtitle="Longitudinal clinical chart, real-time vitals, pharmacopeia, and genomic profile"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Patient Demographic Banner */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-emerald-950 border border-emerald-700 flex items-center justify-center text-emerald-400 font-bold text-lg">
              EV
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-bold">Eleanor Vance</h3>
                <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-950 border border-rose-800 text-rose-300">
                  Critical ICU Bed-04
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                MRN: <strong>MRN-882319</strong> | DOB: 1968-04-12 (58y) | Female | Blood Type: A+
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("overview")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                activeTab === "overview" ? "bg-emerald-600 text-slate-950 font-bold" : "bg-slate-800 text-slate-300"
              }`}
            >
              Surveillance
            </button>
            <button
              onClick={() => setActiveTab("timeline")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                activeTab === "timeline" ? "bg-emerald-600 text-slate-950 font-bold" : "bg-slate-800 text-slate-300"
              }`}
            >
              Timeline (FHIR)
            </button>
            <button
              onClick={() => setActiveTab("medications")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium ${
                activeTab === "medications" ? "bg-emerald-600 text-slate-950 font-bold" : "bg-slate-800 text-slate-300"
              }`}
            >
              Medications & DDI
            </button>
          </div>
        </div>

        {/* Tab content */}
        {activeTab === "overview" && (
          <div className="space-y-6">
            <CDSHooksCard
              summary="CRITICAL: Sepsis Organ Dysfunction Advisory"
              indicator="critical"
              source={{ label: "HealthPulse Surviving Sepsis Engine" }}
              detail="Patient meets Sepsis-3 criteria (Delta-SOFA +3, Lactate 2.8 mmol/L). 1-Hour bundle completion required."
              suggestions={[
                {
                  label: "Initiate Blood Cultures & Repeat Lactate",
                  actions: [{ type: "create", description: "Order STAT Lactate q2h" }],
                },
              ]}
            />
            <VitalWaveformChart />
            <SepsisRiskGauge sofaScore={4} qsofaScore={2} lactateMmolL={2.8} predictedProbabilityPct={84} />
          </div>
        )}

        {activeTab === "timeline" && <EHRTimeline events={timelineEvents} />}

        {activeTab === "medications" && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
            <h4 className="font-semibold text-sm">Active Inpatient Medication Regimen</h4>
            <div className="space-y-3">
              {Object.entries(CLINICAL_PHARMACOPEIA).slice(0, 3).map(([key, med]) => (
                <div key={key} className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-emerald-400">{med.genericName}</span>
                    <span className="text-[10px] text-slate-400 font-mono">RxNorm: {med.rxNormCode}</span>
                  </div>
                  <p className="text-slate-300">{med.therapeuticClass}</p>
                  <div className="text-slate-400">
                    <strong>Standard Dosage:</strong> {med.standardDosing[0]?.dose} via {med.standardDosing[0]?.route} ({med.standardDosing[0]?.frequency})
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
