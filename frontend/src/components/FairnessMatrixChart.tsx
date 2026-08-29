"use client";

import React from "react";
import { CheckCircle2, ShieldCheck, HelpCircle } from "lucide-react";

export function FairnessMatrixChart() {
  const demographics = [
    { group: "Male", sampleSize: "34,280", tpr: "84.8%", fpr: "11.2%", disparateImpact: "1.00 (Ref)", status: "PASS" },
    { group: "Female", sampleSize: "29,920", tpr: "83.6%", fpr: "11.5%", disparateImpact: "0.96", status: "PASS" },
    { group: "Age 18-49", sampleSize: "18,400", tpr: "85.1%", fpr: "9.8%", disparateImpact: "0.94", status: "PASS" },
    { group: "Age 50-74", sampleSize: "32,100", tpr: "84.2%", fpr: "11.8%", disparateImpact: "1.00 (Ref)", status: "PASS" },
    { group: "Age 75+", sampleSize: "13,700", tpr: "83.0%", fpr: "12.4%", disparateImpact: "0.92", status: "PASS" },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <h3 className="font-semibold text-sm">Subgroup Demographic Fairness & Disparate Impact Matrix</h3>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 font-medium">
          4/5ths Rule Verified (0.92 &gt;= 0.80)
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold text-[10px]">
              <th className="pb-2">Protected Demographic Subgroup</th>
              <th className="pb-2">Validation Samples</th>
              <th className="pb-2">Sensitivity (TPR)</th>
              <th className="pb-2">False Positive Rate (FPR)</th>
              <th className="pb-2">Disparate Impact Ratio</th>
              <th className="pb-2">Compliance Verdict</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {demographics.map((d, i) => (
              <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-2.5 font-medium text-slate-200">{d.group}</td>
                <td className="py-2.5 text-slate-400">{d.sampleSize}</td>
                <td className="py-2.5 font-mono text-emerald-400">{d.tpr}</td>
                <td className="py-2.5 font-mono text-slate-300">{d.fpr}</td>
                <td className="py-2.5 font-mono text-blue-400">{d.disparateImpact}</td>
                <td className="py-2.5">
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-950/80 border border-emerald-800 text-emerald-300 font-semibold text-[10px]">
                    <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                    <span>{d.status}</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
