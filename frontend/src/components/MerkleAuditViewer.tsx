"use client";

import React from "react";
import { Link2, ShieldCheck, Lock, AlertOctagon } from "lucide-react";

export function MerkleAuditViewer() {
  const blocks = [
    {
      index: 3,
      timestamp: "2026-08-29T10:42:15Z",
      actor: "Dr. Jenkins (CLINICIAN)",
      action: "EHR_ORDER_MEDICATION",
      resource: "MedicationRequest/MED-8891",
      patient: "P-100234",
      hash: "a4f8e9102c77d4b1a80c98e11a2f4401bb8d9902...",
      prevHash: "7b19a002fe4412c98a0021bdfa338901cc9901aa...",
      isBreakGlass: false,
    },
    {
      index: 2,
      timestamp: "2026-08-29T10:15:00Z",
      actor: "Emergency Team (EMERGENCY_OVERRIDE)",
      action: "BREAK_GLASS_ACCESS",
      resource: "Patient/P-100234",
      patient: "P-100234",
      hash: "7b19a002fe4412c98a0021bdfa338901cc9901aa...",
      prevHash: "0034a11fec8891002acb77881109ffbb887711aa...",
      isBreakGlass: true,
    },
    {
      index: 1,
      timestamp: "2026-08-29T09:30:12Z",
      actor: "TelemetryIngestionWorker (SYSTEM)",
      action: "INGEST_ICU_TELEMETRY",
      resource: "Observation/OBS-44012",
      patient: "P-100234",
      hash: "0034a11fec8891002acb77881109ffbb887711aa...",
      prevHash: "0000000000000000000000000000000000000000...",
      isBreakGlass: false,
    },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Lock className="w-5 h-5 text-emerald-400" />
          <h3 className="font-semibold text-sm">Cryptographically Verifiable Merkle Audit Ledger</h3>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 font-medium flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Chain Integrity 100% Intact</span>
        </span>
      </div>

      <div className="space-y-3">
        {blocks.map((b) => (
          <div
            key={b.index}
            className={`p-3.5 rounded-lg border text-xs transition-all ${
              b.isBreakGlass
                ? "bg-rose-950/20 border-rose-800/80"
                : "bg-slate-950/80 border-slate-800/80 hover:border-slate-700"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-bold text-slate-300 font-mono">Block #{b.index}</span>
                {b.isBreakGlass ? (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-rose-900 text-rose-200 text-[10px] font-bold">
                    <AlertOctagon className="w-3 h-3" />
                    <span>EMERGENCY BREAK-GLASS</span>
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">
                    {b.action}
                  </span>
                )}
              </div>
              <span className="text-slate-400 font-mono text-[11px]">{b.timestamp}</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2 pt-2 border-t border-slate-800/60 text-[11px]">
              <div>
                <span className="text-slate-400">Actor:</span> <strong className="text-slate-200">{b.actor}</strong>
              </div>
              <div>
                <span className="text-slate-400">Resource:</span> <strong className="text-slate-200">{b.resource}</strong>
              </div>
            </div>

            <div className="mt-2 text-[10px] font-mono text-slate-400 space-y-0.5">
              <div className="flex items-center gap-1 truncate">
                <Link2 className="w-3 h-3 text-emerald-400 flex-shrink-0" />
                <span>Current Hash: <strong className="text-emerald-300">{b.hash}</strong></span>
              </div>
              <div className="truncate text-slate-400">
                <span>Prev Hash: {b.prevHash}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
