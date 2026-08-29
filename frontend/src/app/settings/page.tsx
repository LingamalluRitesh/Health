"use client";

import React from "react";
import { Header } from "../../components/Header";
import { Settings, Server, ShieldCheck, Database, Zap } from "lucide-react";

export default function SettingsPage() {
  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="Hospital System Configuration & EHR Interoperability"
        subtitle="FHIR R4 servers, HL7 message brokers, PACS WADO-RS endpoints, and security keys"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-white space-y-6">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-4">
            <Server className="w-5 h-5 text-emerald-400" />
            <h3 className="font-semibold text-base">EHR Interoperability Endpoints</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="text-slate-400 font-semibold block mb-1 uppercase">FHIR R4 Server Base URL</label>
              <input
                type="text"
                defaultValue="https://ehr.hospital-main.org/fhir/r4"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white font-mono"
              />
            </div>
            <div>
              <label className="text-slate-400 font-semibold block mb-1 uppercase">HL7 MLLP Gateway Port</label>
              <input
                type="text"
                defaultValue="2575 (MLLP TCP/IP)"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white font-mono"
              />
            </div>
            <div>
              <label className="text-slate-400 font-semibold block mb-1 uppercase">PACS DICOMweb WADO-RS URL</label>
              <input
                type="text"
                defaultValue="http://pacs.radiology.internal:8042/dicom-web"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white font-mono"
              />
            </div>
            <div>
              <label className="text-slate-400 font-semibold block mb-1 uppercase">Telemetry WebSocket Port</label>
              <input
                type="text"
                defaultValue="8000 (/ws/telemetry)"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white font-mono"
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
