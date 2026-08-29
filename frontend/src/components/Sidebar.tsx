"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  User,
  HeartPulse,
  Scan,
  Dna,
  ShieldCheck,
  FileText,
  GitPullRequest,
  CheckCircle2,
  Settings,
  Bell,
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { label: "Executive Dashboard", href: "/", icon: Activity },
    { label: "Patient 360 EHR", href: "/patients/", icon: User },
    { label: "ICU Telemetry Center", href: "/icu/", icon: HeartPulse },
    { label: "Radiology DICOM Studio", href: "/radiology/", icon: Scan },
    { label: "Genomics & PGx", href: "/genomics/", icon: Dna },
    { label: "AI Governance & FDA", href: "/governance/", icon: ShieldCheck },
    { label: "Cryptographic Audit", href: "/audit/", icon: FileText },
    { label: "Clinical Trial Matcher", href: "/trials/", icon: CheckCircle2 },
    { label: "CDS Hooks v1.0 Sandbox", href: "/cds-hooks/", icon: Bell },
    { label: "Federated Learning Hub", href: "/federated/", icon: GitPullRequest },
    { label: "System Settings", href: "/settings/", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-200 min-h-screen flex flex-col border-r border-slate-800">
      <div className="p-5 border-b border-slate-800 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-emerald-500 flex items-center justify-center text-slate-950 font-bold">
          HP
        </div>
        <div>
          <h1 className="font-semibold text-white tracking-wide text-sm">HealthPulse AI</h1>
          <p className="text-xs text-emerald-400">Clinical Intelligence</p>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? "bg-emerald-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        <p className="font-medium text-slate-400">HIPAA Protected</p>
        <p>SHA-256 Merkle Chain Active</p>
      </div>
    </aside>
  );
}
