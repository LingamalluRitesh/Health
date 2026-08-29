"use client";

import React, { useState } from "react";
import { Header } from "../../components/Header";
import { DicomViewer } from "../../components/DicomViewer";
import { Scan, Sparkles, AlertCircle, FileSearch } from "lucide-react";

export default function RadiologyPage() {
  const [noduleSize, setNoduleSize] = useState<number>(8.5);
  const [noduleDensity, setNoduleDensity] = useState<number>(-120);

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Radiology DICOM 3D Volumetric Studio"
        subtitle="Hounsfield Unit tissue windowing, pulmonary nodule segmentation, and cardiothoracic metrics"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* DICOM Canvas Viewer Component */}
        <DicomViewer />

        {/* Quantitative Radiology Analytics Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Fleischner Pulmonary Nodule Risk Estimator */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              <Scan className="w-5 h-5 text-emerald-400" />
              <h4 className="font-semibold text-sm">Fleischner 2017 Pulmonary Nodule Morphometry</h4>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <div className="flex justify-between text-slate-300 mb-1">
                  <span>Max Axial Diameter:</span>
                  <span className="font-mono text-emerald-400 font-bold">{noduleSize} mm</span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="25"
                  step="0.5"
                  value={noduleSize}
                  onChange={(e) => setNoduleSize(Number(e.target.value))}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                />
              </div>

              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1">
                <div className="flex justify-between">
                  <span className="text-slate-400">Estimated Volume:</span>
                  <span className="font-mono font-bold text-white">
                    {((Math.PI / 6) * noduleSize * noduleSize * 0.85 * noduleSize * 0.85).toFixed(1)} mm³
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Malignancy Risk Tier:</span>
                  <span className="font-bold text-rose-400">
                    {noduleSize >= 8 ? "High Risk (>15%)" : noduleSize >= 6 ? "Intermediate (1-5%)" : "Low Risk (<1%)"}
                  </span>
                </div>
                <div className="pt-2 text-[11px] text-slate-300 border-t border-slate-800/80">
                  <strong>Recommendation:</strong>{" "}
                  {noduleSize >= 8
                    ? "Consider chest CT at 3 months, PET/CT scan, or tissue biopsy."
                    : noduleSize >= 6
                    ? "Follow-up CT at 6-12 months, then at 18-24 months if stable."
                    : "No routine follow-up required in low-risk patients."}
                </div>
              </div>
            </div>
          </div>

          {/* Cardiothoracic Ratio (CTR) Analyzer */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              <Sparkles className="w-5 h-5 text-blue-400" />
              <h4 className="font-semibold text-sm">Automated Cardiothoracic Ratio (CTR) Measurement</h4>
            </div>

            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <span className="text-slate-400 uppercase text-[10px] font-semibold">Cardiac Diameter</span>
                  <div className="text-lg font-bold text-white mt-1 font-mono">162.4 mm</div>
                </div>
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <span className="text-slate-400 uppercase text-[10px] font-semibold">Thoracic Diameter</span>
                  <div className="text-lg font-bold text-white mt-1 font-mono">298.0 mm</div>
                </div>
              </div>

              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="text-[11px] text-slate-400">Cardiothoracic Ratio (CTR):</div>
                  <div className="text-2xl font-bold font-mono text-amber-400">0.545</div>
                </div>
                <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-950 text-amber-300 border border-amber-800">
                  Mild Cardiomegaly
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
