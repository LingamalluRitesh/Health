"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Header } from "../../components/Header";
import { Search, User, Filter, ArrowRight, ShieldCheck } from "lucide-react";

export default function PatientsPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const patients = [
    {
      id: "P-100234",
      name: "Eleanor Vance",
      mrn: "MRN-882319",
      age: 58,
      gender: "Female",
      department: "ICU-East",
      bed: "BED-04",
      diagnosis: "Sepsis secondary to acute pyelonephritis",
      acuity: "Critical",
      sofa: 4,
    },
    {
      id: "P-100235",
      name: "Marcus Bennett",
      mrn: "MRN-773192",
      age: 71,
      gender: "Male",
      department: "Cardiology Step-Down",
      bed: "BED-12",
      diagnosis: "Acute decompensated heart failure with AFib",
      acuity: "Moderate",
      sofa: 2,
    },
    {
      id: "P-100236",
      name: "Sophia Chen",
      mrn: "MRN-991204",
      age: 64,
      gender: "Female",
      department: "Oncology Ward",
      bed: "BED-08",
      diagnosis: "Stage IV NSCLC (EGFR L858R)",
      acuity: "Stable",
      sofa: 0,
    },
    {
      id: "P-100237",
      name: "James Robertson",
      mrn: "MRN-554109",
      age: 49,
      gender: "Male",
      department: "Surgical ICU",
      bed: "BED-02",
      diagnosis: "Post-op liver transplant with acute rejection risk",
      acuity: "Severe",
      sofa: 3,
    },
  ];

  const filtered = patients.filter(
    (p) =>
      p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.mrn.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.diagnosis.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Patient 360 & Longitudinal EHR Registry"
        subtitle="Searchable inpatient and outpatient clinical cohort management"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Search & Filter Header */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-slate-900 p-4 rounded-xl border border-slate-800">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by Patient Name, MRN, or Diagnosis..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
            />
          </div>
          <div className="flex items-center gap-2">
            <button className="flex items-center gap-2 px-3 py-2 bg-slate-800 text-slate-200 text-xs font-medium rounded-lg hover:bg-slate-700">
              <Filter className="w-3.5 h-3.5" />
              <span>Filter by Unit</span>
            </button>
          </div>
        </div>

        {/* Patients Table */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase font-semibold text-[10px]">
              <tr>
                <th className="py-3 px-4">Patient Name & MRN</th>
                <th className="py-3 px-4">Demographics</th>
                <th className="py-3 px-4">Unit & Bed</th>
                <th className="py-3 px-4">Primary Diagnosis</th>
                <th className="py-3 px-4">Clinical Acuity</th>
                <th className="py-3 px-4">SOFA Score</th>
                <th className="py-3 px-4 text-right">EHR Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {filtered.map((pt) => (
                <tr key={pt.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4">
                    <div className="font-semibold text-white">{pt.name}</div>
                    <div className="text-[11px] font-mono text-slate-400">{pt.mrn}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-300">
                    {pt.age}y / {pt.gender}
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="text-white">{pt.department}</div>
                    <div className="text-[11px] text-slate-400 font-mono">{pt.bed}</div>
                  </td>
                  <td className="py-3.5 px-4 max-w-xs truncate text-slate-300">
                    {pt.diagnosis}
                  </td>
                  <td className="py-3.5 px-4">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        pt.acuity === "Critical"
                          ? "bg-rose-950 text-rose-300 border border-rose-800"
                          : pt.acuity === "Severe"
                          ? "bg-amber-950 text-amber-300 border border-amber-800"
                          : "bg-emerald-950 text-emerald-300 border border-emerald-800"
                      }`}
                    >
                      {pt.acuity}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono font-bold">
                    <span className={pt.sofa >= 2 ? "text-rose-400" : "text-emerald-400"}>
                      {pt.sofa}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <Link
                      href={`/patients/${pt.id}/`}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold rounded-md text-xs transition-colors"
                    >
                      <span>Patient 360</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
