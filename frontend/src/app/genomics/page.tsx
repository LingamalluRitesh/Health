"use client";

import React, { useState } from "react";
import { Header } from "../../components/Header";
import { Dna, ShieldAlert, CheckCircle2, Pill, Activity } from "lucide-react";

export default function GenomicsPage() {
  const [selectedGene, setSelectedGene] = useState("CYP2C19");
  const [diplotype, setDiplotype] = useState("*2/*3");

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Precision Genomics & Pharmacogenomics (PGx) Studio"
        subtitle="CPIC Level A actionable guidelines, VCF variant calling, and Polygenic Risk Scores"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* CPIC Guideline Evaluator Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-white space-y-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-2">
              <Dna className="w-5 h-5 text-emerald-400" />
              <h3 className="font-semibold text-base">CPIC Actionable Pharmacogenomics Rule Engine</h3>
            </div>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-950 text-emerald-300 border border-emerald-800">
              CPIC Level A Guideline
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-xs text-slate-400 font-semibold block mb-1.5 uppercase">Target Gene</label>
              <select
                value={selectedGene}
                onChange={(e) => setSelectedGene(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="CYP2C19">CYP2C19 (Clopidogrel / Plavix)</option>
                <option value="CYP2D6">CYP2D6 (Codeine / Tramadol)</option>
                <option value="DPYD">DPYD (5-Fluorouracil / Capecitabine)</option>
                <option value="VKORC1">VKORC1 & CYP2C9 (Warfarin)</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-slate-400 font-semibold block mb-1.5 uppercase">Diplotype</label>
              <input
                type="text"
                value={diplotype}
                onChange={(e) => setDiplotype(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-emerald-500 font-mono"
              />
            </div>

            <div className="flex flex-col justify-end">
              <div className="p-2.5 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                <span className="text-slate-400">Inferred Phenotype:</span>
                <div className="font-bold text-rose-400">Poor Metabolizer (PM)</div>
              </div>
            </div>
          </div>

          {/* Dosing Recommendation Output */}
          <div className="p-4 bg-rose-950/20 border border-rose-900/60 rounded-xl space-y-2 text-xs">
            <div className="flex items-center gap-2 font-bold text-rose-300">
              <ShieldAlert className="w-4 h-4" />
              <span>CLINICAL IMPLICATION: Diminished Antiplatelet Activation</span>
            </div>
            <p className="text-slate-300 leading-relaxed">
              Patient possesses loss-of-function alleles (*2 and *3). Bioactivation of Clopidogrel to its active thiol metabolite is severely impaired, significantly elevating stent thrombosis and ischemic stroke risk.
            </p>
            <div className="pt-2 border-t border-rose-900/40 flex items-center justify-between text-slate-200">
              <div>
                <strong>Recommendation:</strong> AVOID Clopidogrel. Prescribe alternative P2Y12 inhibitor at standard dose.
              </div>
              <span className="font-mono text-emerald-400 font-bold">Alternatives: Ticagrelor 90mg BID, Prasugrel 10mg daily</span>
            </div>
          </div>
        </div>

        {/* Polygenic Risk Scores (PRS) Matrix */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-400" />
              <h4 className="font-semibold text-sm">Polygenic Risk Scores (PRS) Disease Predisposition</h4>
            </div>
            <span className="text-xs text-slate-400">GWAS Multi-Locus Summary</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-2">
              <div className="flex justify-between">
                <span className="font-bold text-slate-200">Coronary Artery Disease</span>
                <span className="font-bold text-rose-400 font-mono">88th Percentile</span>
              </div>
              <p className="text-slate-400">Relative Risk: 2.34x vs population mean.</p>
              <div className="text-[11px] text-amber-400 font-medium">Early CAC screening & aggressive LDL lowering indicated.</div>
            </div>

            <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-2">
              <div className="flex justify-between">
                <span className="font-bold text-slate-200">Type 2 Diabetes</span>
                <span className="font-bold text-emerald-400 font-mono">34th Percentile</span>
              </div>
              <p className="text-slate-400">Relative Risk: 0.88x vs population mean.</p>
              <div className="text-[11px] text-emerald-400 font-medium">Standard preventative screening.</div>
            </div>

            <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs space-y-2">
              <div className="flex justify-between">
                <span className="font-bold text-slate-200">Atrial Fibrillation</span>
                <span className="font-bold text-amber-400 font-mono">72nd Percentile</span>
              </div>
              <p className="text-slate-400">Relative Risk: 1.65x vs population mean.</p>
              <div className="text-[11px] text-slate-300 font-medium">Annual pulse checks and wearable ECG surveillance.</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
