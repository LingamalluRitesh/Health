"use client";

import React from "react";
import { ShieldCheck, FileCheck, Layers, AlertCircle } from "lucide-react";

export function ModelCardViewer() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-white space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-950 border border-purple-800 text-purple-300">
              EU AI Act Annex IV Compliant
            </span>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-950 border border-blue-800 text-blue-300">
              FDA SaMD Class II (510k)
            </span>
          </div>
          <h3 className="text-lg font-bold text-white mt-2">HealthPulse Sepsis-Net Neural Surveillance Engine</h3>
          <p className="text-xs text-slate-400">Model Version: v1.2.0 | Release: 2026-01-15 | Verification: 100% Certified</p>
        </div>
        <div className="p-3 bg-emerald-950/60 border border-emerald-800/60 rounded-xl text-center">
          <div className="text-xs text-emerald-400 font-semibold uppercase">AUROC Score</div>
          <div className="text-2xl font-black text-emerald-300">0.912</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
        {/* Intended Use & Indications */}
        <div className="bg-slate-950/70 p-4 rounded-lg border border-slate-800 space-y-2">
          <h4 className="font-semibold text-slate-200 text-sm flex items-center gap-1.5">
            <FileCheck className="w-4 h-4 text-emerald-400" />
            <span>Intended Clinical Use & Patient Population</span>
          </h4>
          <p className="text-slate-400 leading-relaxed">
            Continuous real-time automated surveillance of adult ICU and telemetry-monitored beds to detect acute sepsis onset 4 to 6 hours prior to overt decompensation.
          </p>
          <div className="pt-2 border-t border-slate-800/80">
            <span className="font-semibold text-slate-300">Target Population:</span> Adults aged 18+ admitted to ICU/CCU.
          </div>
        </div>

        {/* Contraindications */}
        <div className="bg-slate-950/70 p-4 rounded-lg border border-slate-800 space-y-2">
          <h4 className="font-semibold text-slate-200 text-sm flex items-center gap-1.5">
            <AlertCircle className="w-4 h-4 text-rose-400" />
            <span>Clinical Contraindications & Limitations</span>
          </h4>
          <ul className="text-slate-400 space-y-1 list-disc list-inside">
            <li>Contraindicated in pediatric populations (&lt;18 years).</li>
            <li>Autonomous drug titration prohibited; clinician sign-off mandatory.</li>
            <li>Decreased sensitivity during active targeted temperature management.</li>
          </ul>
        </div>
      </div>

      {/* Benchmarks & Performance Metrics */}
      <div className="bg-slate-950/80 p-4 rounded-lg border border-slate-800 space-y-3">
        <h4 className="font-semibold text-slate-200 text-sm flex items-center gap-1.5">
          <Layers className="w-4 h-4 text-blue-400" />
          <span>Independent Multi-Center Validation Benchmarks</span>
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div className="bg-slate-900 p-2.5 rounded border border-slate-800">
            <div className="text-[11px] text-slate-400 uppercase">AUPRC</div>
            <div className="text-lg font-bold text-white mt-0.5">0.684</div>
          </div>
          <div className="bg-slate-900 p-2.5 rounded border border-slate-800">
            <div className="text-[11px] text-slate-400 uppercase">Sensitivity (at 80% Spec)</div>
            <div className="text-lg font-bold text-emerald-400 mt-0.5">84.2%</div>
          </div>
          <div className="bg-slate-900 p-2.5 rounded border border-slate-800">
            <div className="text-[11px] text-slate-400 uppercase">Mean Lead Time</div>
            <div className="text-lg font-bold text-blue-400 mt-0.5">5.4 Hours</div>
          </div>
          <div className="bg-slate-900 p-2.5 rounded border border-slate-800">
            <div className="text-[11px] text-slate-400 uppercase">Brier Calibration Score</div>
            <div className="text-lg font-bold text-purple-400 mt-0.5">0.052</div>
          </div>
        </div>
      </div>
    </div>
  );
}
