import React from "react";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  change?: string;
  isPositive?: boolean;
  icon: LucideIcon;
  variant?: "default" | "success" | "warning" | "danger" | "info";
}

export function MetricCard({
  title,
  value,
  subtitle,
  change,
  isPositive,
  icon: Icon,
  variant = "default",
}: MetricCardProps) {
  const variantStyles = {
    default: "border-slate-800 bg-slate-900 text-white",
    success: "border-emerald-800/40 bg-emerald-950/20 text-emerald-300",
    warning: "border-amber-800/40 bg-amber-950/20 text-amber-300",
    danger: "border-rose-800/40 bg-rose-950/20 text-rose-300",
    info: "border-blue-800/40 bg-blue-950/20 text-blue-300",
  };

  const iconBgStyles = {
    default: "bg-slate-800 text-slate-300",
    success: "bg-emerald-900/60 text-emerald-400",
    warning: "bg-amber-900/60 text-amber-400",
    danger: "bg-rose-900/60 text-rose-400",
    info: "bg-blue-900/60 text-blue-400",
  };

  return (
    <div className={`p-5 rounded-xl border ${variantStyles[variant]} shadow-sm transition-all hover:border-slate-700`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</span>
        <div className={`p-2 rounded-lg ${iconBgStyles[variant]}`}>
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div className="mt-3">
        <div className="text-2xl font-bold text-white tracking-tight">{value}</div>
        {(subtitle || change) && (
          <div className="mt-1 flex items-center gap-2 text-xs">
            {change && (
              <span className={`font-semibold ${isPositive ? "text-emerald-400" : "text-rose-400"}`}>
                {change}
              </span>
            )}
            {subtitle && <span className="text-slate-400">{subtitle}</span>}
          </div>
        )}
      </div>
    </div>
  );
}
