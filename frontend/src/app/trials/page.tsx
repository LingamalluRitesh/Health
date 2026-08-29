"use client";

import React, { useState } from "react";
import { Header } from "../../components/Header";
import { CheckCircle2, XCircle, Clock, Search, Filter } from "lucide-react";

export default function ClinicalTrialsPage() {
  const trials = [
    {
      id: "NCT04875321",
      title: "Phase III Trial of SGLT2 Inhibitor in Advanced Diabetic Nephropathy",
      phase: "Phase 3",
      condition: "Diabetic Kidney Disease",
      isEligible: true,
      score: "100%",
      criteriaPassed: ["Age 58 (Range 25-75)", "Gender Female matches", "ICU Diagnosis E11.22 & N18.3 matches", "eGFR 42 >= 25.0"],
      criteriaFailed: [],
    },
    {
      id: "NCT05219904",
      title: "Phase II Targeted Immunotherapy for EGFR Exon 20 Insertion NSCLC",
      phase: "Phase 2",
      condition: "NSCLC",
      isEligible: false,
      score: "40%",
      criteriaPassed: ["Age 58 (Range 18-80)", "Platelet count >= 100k"],
      criteriaFailed: ["Missing target mutation EGFR:exon20ins", "Missing primary ICD-10 diagnosis C34.90"],
    },
  ];

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Precision Clinical Trial Cohort Matching Engine"
        subtitle="Automated patient screening against clinical trial protocols and inclusion criteria"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        <div className="space-y-4">
          {trials.map((t) => (
            <div key={t.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-blue-950 border border-blue-800 text-blue-300 text-[10px] font-bold font-mono">
                      {t.id}
                    </span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-semibold">
                      {t.phase}
                    </span>
                  </div>
                  <h4 className="font-bold text-base mt-1.5 text-white">{t.title}</h4>
                </div>
                <div className="text-right">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${t.isEligible ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-rose-950 text-rose-300 border border-rose-800"}`}>
                    {t.isEligible ? "ELIGIBLE (MATCH 100%)" : "INELIGIBLE"}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-2 border-t border-slate-800">
                <div>
                  <div className="font-semibold text-emerald-400 mb-1.5 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Inclusion Criteria Satisfied:</span>
                  </div>
                  <ul className="space-y-1 text-slate-300">
                    {t.criteriaPassed.map((c, i) => (
                      <li key={i}>• {c}</li>
                    ))}
                  </ul>
                </div>

                {t.criteriaFailed.length > 0 && (
                  <div>
                    <div className="font-semibold text-rose-400 mb-1.5 flex items-center gap-1">
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Exclusion Criteria Triggered:</span>
                    </div>
                    <ul className="space-y-1 text-slate-300">
                      {t.criteriaFailed.map((c, i) => (
                        <li key={i}>• {c}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
