"use client";

import React, { useState } from "react";
import { Header } from "../../components/Header";
import { CDSHooksCard } from "../../components/CDSHooksCard";
import { Bell, Play, Code, Check } from "lucide-react";

export default function CDSHooksPage() {
  const [hookType, setHookType] = useState("patient-view");
  const [executed, setExecuted] = useState(true);

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Clinical Decision Support (CDS Hooks v1.0) Integration Sandbox"
        subtitle="Test EHR hook triggers, prefetch FHIR bundles, and inspect advisory action cards"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Hook Trigger Simulator */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Code className="w-5 h-5 text-emerald-400" />
              <h3 className="font-semibold text-sm">CDS Hook Trigger Request Builder</h3>
            </div>
            <button
              onClick={() => setExecuted(true)}
              className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold rounded-lg text-xs flex items-center gap-1.5"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Fire Hook Evaluation</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="text-slate-400 font-semibold block mb-1 uppercase">Hook Name</label>
              <select
                value={hookType}
                onChange={(e) => setHookType(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"
              >
                <option value="patient-view">patient-view (Sepsis & Vital Surveillance)</option>
                <option value="order-select">order-select (Pharmacogenomics & DDI Safety)</option>
                <option value="order-sign">order-sign (Renal Dosing & eGFR Advisor)</option>
              </select>
            </div>

            <div>
              <label className="text-slate-400 font-semibold block mb-1 uppercase">Context Patient ID</label>
              <input
                type="text"
                defaultValue="P-100234 (Eleanor Vance - ICU East)"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white font-mono"
              />
            </div>
          </div>
        </div>

        {/* Advisory Cards Rendered */}
        {executed && (
          <div className="space-y-4">
            <h4 className="font-semibold text-sm text-slate-300">Generated CDS Advisory Response Cards</h4>
            <CDSHooksCard
              summary="CRITICAL: Sepsis Early Warning Alert for Bed 04 (SOFA: 4, qSOFA: 2)"
              indicator="critical"
              source={{
                label: "Surviving Sepsis Campaign 2024 Guideline Engine",
                url: "https://healthpulse.ai/guidelines/sepsis-3",
              }}
              detail="Patient demonstrates acute organ dysfunction markers (RR: 26 bpm, MAP: 62 mmHg, Lactate: 2.8 mmol/L). Initiate 1-Hour Sepsis Bundle immediately."
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
          </div>
        )}
      </div>
    </main>
  );
}
