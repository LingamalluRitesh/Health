"use client";

import React from "react";
import { AlertTriangle, CheckCircle, ShieldAlert } from "lucide-react";

interface SepsisRiskGaugeProps {
  sofaScore: number;
  qsofaScore: number;
  lactateMmolL?: number;
  predictedProbabilityPct: number;
}

export function SepsisRiskGauge({
  sofaScore,
  qsofaScore,
  lactateMmolL = 2.4,
  predictedProbabilityPct = 78,
}: SepsisRiskGaugeProps) {
  const isCritical = predictedProbabilityPct >= 70 || sofaScore >= 4;

  return (
    <div className={`p-5 rounded-xl border ${isCritical ? "border-rose-900/60 bg-rose-950/20" : "border-slate-800 bg-slate-900"} text-white`}>
      <div className="flex items-center justify-between border-b border-slate-800/60 pb-3 mb-4">
        <div className="flex items-center gap-2">
          {isCritical ? (
            <ShieldAlert className="w-5 h-5 text-rose-500 animate-bounce" />
          ) : (
            <CheckCircle className="w-5 h-5 text-emerald-500" />
          )}
          <h4 className="font-semibold text-sm">Sepsis-3 Early Warning & Resuscitation Gauge</h4>
        </div>
        <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${isCritical ? "bg-rose-900 text-rose-200" : "bg-emerald-900 text-emerald-200"}`}>
          {isCritical ? "HIGH RISK (TIER 1)" : "STABLE SURVEILLANCE"}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
        {/* Risk Percentage Gauge */}
        <div className="bg-slate-950/80 p-4 rounded-lg border border-slate-800/80 flex flex-col items-center justify-center">
          <div className="text-3xl font-black text-rose-400">{predictedProbabilityPct}%</div>
          <span className="text-xs text-slate-400 mt-1 uppercase font-semibold">Predicted Deterioration</span>
          <span className="text-[11px] text-slate-400 mt-0.5">Lead Time: 5.4 Hours</span>
        </div>

        {/* SOFA / qSOFA Breakdown */}
        <div className="bg-slate-950/80 p-4 rounded-lg border border-slate-800/80 flex flex-col justify-center text-left space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">qSOFA Bedside Score:</span>
            <span className={`font-bold font-mono ${qsofaScore >= 2 ? "text-rose-400" : "text-emerald-400"}`}>
              {qsofaScore} / 3
            </span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">SOFA Organ Failure Score:</span>
            <span className={`font-bold font-mono ${sofaScore >= 2 ? "text-amber-400" : "text-emerald-400"}`}>
              {sofaScore} / 24
            </span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Serum Lactate:</span>
            <span className={`font-bold font-mono ${lactateMmolL > 2.0 ? "text-rose-400" : "text-emerald-400"}`}>
              {lactateMmolL} mmol/L
            </span>
          </div>
        </div>

        {/* 1-Hour Sepsis Bundle Status */}
        <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800/80 text-left text-xs space-y-1">
          <div className="font-semibold text-slate-300 mb-1 text-[11px] uppercase tracking-wider">
            1-Hour Bundle Checklist
          </div>
          <div className="flex items-center gap-1.5 text-emerald-400">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Blood Cultures Drawn</span>
          </div>
          <div className="flex items-center gap-1.5 text-emerald-400">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Serum Lactate Measured</span>
          </div>
          <div className="flex items-center gap-1.5 text-rose-400 font-medium">
            <AlertTriangle className="w-3.5 h-3.5 animate-pulse" />
            <span>IV Antibiotics Pending</span>
          </div>
        </div>
      </div>
    </div>
  );
}
