"use client";

import React, { useState } from "react";
import { Header } from "../../components/Header";
import { GitPullRequest, Shield, Building2, Play, Check } from "lucide-react";

export default function FederatedLearningPage() {
  const [currentRound, setCurrentRound] = useState(4);
  const [isRunning, setIsRunning] = useState(false);

  const hospitals = [
    { id: "HOSP-MAYO", name: "Mayo Clinic Central", patients: 14500, alpha: 0.5, status: "Ready" },
    { id: "HOSP-JHU", name: "Johns Hopkins Hospital", patients: 12200, alpha: 0.4, status: "Ready" },
    { id: "HOSP-MGH", name: "Mass General Brigham", patients: 16800, alpha: 0.6, status: "Ready" },
    { id: "HOSP-STANFORD", name: "Stanford Health Care", patients: 9800, alpha: 0.5, status: "Ready" },
  ];

  const handleRunRound = () => {
    setIsRunning(true);
    setTimeout(() => {
      setCurrentRound((r) => r + 1);
      setIsRunning(false);
    }, 1500);
  };

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Cross-Hospital Federated Learning & Privacy Hub"
        subtitle="FedAvg / FedProx multi-institutional training with Renyi Differential Privacy accounting"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Federated Overview Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl text-white">
            <span className="text-[10px] uppercase font-semibold text-slate-400">Current Round</span>
            <div className="text-2xl font-bold text-emerald-400 mt-1 font-mono">Round #{currentRound}</div>
          </div>
          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl text-white">
            <span className="text-[10px] uppercase font-semibold text-slate-400">Total Cohort Trained</span>
            <div className="text-2xl font-bold text-blue-400 mt-1 font-mono">53,300 Patients</div>
          </div>
          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl text-white">
            <span className="text-[10px] uppercase font-semibold text-slate-400">Global Validation Loss</span>
            <div className="text-2xl font-bold text-purple-400 mt-1 font-mono">0.142</div>
          </div>
          <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl text-white">
            <span className="text-[10px] uppercase font-semibold text-slate-400">Privacy Loss (Epsilon)</span>
            <div className="text-2xl font-bold text-amber-400 mt-1 font-mono">ε = 1.00 (δ = 10⁻⁵)</div>
          </div>
        </div>

        {/* Participating Hospital Nodes */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Building2 className="w-5 h-5 text-emerald-400" />
              <h3 className="font-semibold text-sm">Participating Hospital Consortium Nodes</h3>
            </div>
            <button
              onClick={handleRunRound}
              disabled={isRunning}
              className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold rounded-lg text-xs flex items-center gap-1.5 transition-colors"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>{isRunning ? "Aggregating SecAgg Masks..." : "Trigger Federated Round"}</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {hospitals.map((h) => (
              <div key={h.id} className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-200 text-sm">{h.name}</span>
                  <span className="px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono text-[10px]">
                    {h.status}
                  </span>
                </div>
                <div className="text-slate-400">Node Identifier: <strong className="font-mono text-slate-300">{h.id}</strong></div>
                <div className="flex justify-between text-slate-400 pt-1 border-t border-slate-800/80">
                  <span>Local Patients: <strong className="text-white">{h.patients.toLocaleString()}</strong></span>
                  <span>Heterogeneity α: <strong className="text-white font-mono">{h.alpha}</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
