"use client";

import React, { useState } from "react";
import { AlertCircle, AlertTriangle, Info, ExternalLink, Check, X } from "lucide-react";

export interface CDSCardProps {
  summary: string;
  indicator: "info" | "warning" | "critical";
  source: {
    label: string;
    url?: string;
  };
  detail?: string;
  suggestions?: Array<{
    label: string;
    uuid?: string;
    actions: Array<{
      type: string;
      description: string;
    }>;
  }>;
}

export function CDSHooksCard({ summary, indicator, source, detail, suggestions }: CDSCardProps) {
  const [isDismissed, setIsDismissed] = useState(false);
  const [appliedSuggestion, setAppliedSuggestion] = useState<string | null>(null);

  if (isDismissed) return null;

  const indicatorStyles = {
    info: "border-blue-800/60 bg-blue-950/30 text-blue-300",
    warning: "border-amber-800/60 bg-amber-950/30 text-amber-300",
    critical: "border-rose-800/80 bg-rose-950/40 text-rose-300",
  };

  const badgeStyles = {
    info: "bg-blue-900/60 text-blue-300 border-blue-700/60",
    warning: "bg-amber-900/60 text-amber-300 border-amber-700/60",
    critical: "bg-rose-900/80 text-rose-200 border-rose-700/80 animate-pulse",
  };

  const Icon = indicator === "critical" ? AlertCircle : indicator === "warning" ? AlertTriangle : Info;

  return (
    <div className={`p-4 rounded-xl border ${indicatorStyles[indicator]} shadow-sm text-white space-y-3`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2.5">
          <div className="p-1 rounded bg-black/20">
            <Icon className="w-5 h-5 flex-shrink-0" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider border ${badgeStyles[indicator]}`}>
                {indicator}
              </span>
              <h4 className="font-semibold text-sm text-white">{summary}</h4>
            </div>
            {detail && <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">{detail}</p>}
          </div>
        </div>

        <button
          onClick={() => setIsDismissed(true)}
          className="text-slate-400 hover:text-white p-1"
          title="Dismiss card"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Suggestions and Actions */}
      {suggestions && suggestions.length > 0 && (
        <div className="pt-2 border-t border-white/10 space-y-2">
          {suggestions.map((sugg, idx) => (
            <div key={idx} className="flex items-center justify-between bg-black/30 p-2.5 rounded-lg text-xs">
              <div>
                <span className="font-medium text-white">{sugg.label}</span>
                {sugg.actions.map((act, aIdx) => (
                  <div key={aIdx} className="text-[11px] text-slate-400 mt-0.5">
                    • Action: {act.description}
                  </div>
                ))}
              </div>
              <button
                onClick={() => setAppliedSuggestion(sugg.label)}
                disabled={appliedSuggestion === sugg.label}
                className={`px-3 py-1.5 rounded-md font-medium text-xs flex items-center gap-1.5 transition-colors ${
                  appliedSuggestion === sugg.label
                    ? "bg-emerald-700 text-white"
                    : "bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold"
                }`}
              >
                {appliedSuggestion === sugg.label ? (
                  <>
                    <Check className="w-3.5 h-3.5" />
                    <span>Applied to EHR</span>
                  </>
                ) : (
                  <span>Accept Suggestion</span>
                )}
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Source Citation */}
      <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
        <span className="flex items-center gap-1">
          Source: <strong className="text-slate-300">{source.label}</strong>
        </span>
        {source.url && (
          <a
            href={source.url}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1 text-emerald-400 hover:underline"
          >
            <span>Guideline Evidence</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
}
