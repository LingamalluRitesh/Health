"use client";

import React from "react";
import { Bell, Shield, Activity, UserCircle } from "lucide-react";

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  return (
    <header className="h-16 bg-slate-900 border-b border-slate-800 px-6 flex items-center justify-between">
      <div>
        <h2 className="text-lg font-semibold text-white">{title}</h2>
        {subtitle && <p className="text-xs text-slate-400">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 px-2.5 py-1 bg-emerald-950/60 border border-emerald-800/60 rounded-full text-xs font-medium text-emerald-400">
          <Shield className="w-3.5 h-3.5" />
          <span>HIPAA Safe Harbor Active</span>
        </div>

        <div className="flex items-center gap-1.5 px-2.5 py-1 bg-blue-950/60 border border-blue-800/60 rounded-full text-xs font-medium text-blue-400">
          <Activity className="w-3.5 h-3.5" />
          <span>ICU Telemetry: Live</span>
        </div>

        <div className="flex items-center gap-2 pl-2 border-l border-slate-800 text-slate-300">
          <UserCircle className="w-6 h-6 text-slate-400" />
          <div className="text-xs text-left">
            <p className="font-medium text-white">Dr. Sarah Jenkins</p>
            <p className="text-slate-400">Attending Physician (ICU)</p>
          </div>
        </div>
      </div>
    </header>
  );
}
