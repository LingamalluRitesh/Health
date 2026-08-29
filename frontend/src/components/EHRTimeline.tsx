"use client";

import React from "react";
import { Calendar, FileText, FlaskConical, Pill, Stethoscope, AlertCircle } from "lucide-react";

export interface TimelineEvent {
  id: string;
  timestamp: string;
  category: "encounter" | "lab" | "medication" | "imaging" | "alert" | "note";
  title: string;
  description: string;
  provider: string;
  badgeText?: string;
  badgeVariant?: "danger" | "warning" | "success" | "info";
}

interface EHRTimelineProps {
  events: TimelineEvent[];
}

export function EHRTimeline({ events }: EHRTimelineProps) {
  const getIcon = (category: string) => {
    switch (category) {
      case "encounter":
        return Stethoscope;
      case "lab":
        return FlaskConical;
      case "medication":
        return Pill;
      case "alert":
        return AlertCircle;
      default:
        return FileText;
    }
  };

  const getIconBg = (category: string) => {
    switch (category) {
      case "alert":
        return "bg-rose-900/60 text-rose-400 border-rose-700/60";
      case "medication":
        return "bg-blue-900/60 text-blue-400 border-blue-700/60";
      case "lab":
        return "bg-emerald-900/60 text-emerald-400 border-emerald-700/60";
      default:
        return "bg-slate-800 text-slate-300 border-slate-700";
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-6">
        <h3 className="font-semibold text-base">Longitudinal Patient EHR Timeline</h3>
        <span className="text-xs text-slate-400">FHIR R4 Event Stream</span>
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-3 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
        {events.map((evt) => {
          const Icon = getIcon(evt.category);
          const iconStyles = getIconBg(evt.category);

          return (
            <div key={evt.id} className="relative group">
              {/* Timeline Marker */}
              <div className={`absolute -left-6 top-1 w-6 h-6 rounded-full border ${iconStyles} flex items-center justify-center -translate-x-1/2 shadow-sm`}>
                <Icon className="w-3 h-3" />
              </div>

              {/* Event Card */}
              <div className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-4 transition-all hover:border-slate-700">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-semibold text-slate-200">{evt.title}</h4>
                      {evt.badgeText && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full font-medium bg-rose-950 border border-rose-800 text-rose-300">
                          {evt.badgeText}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-400 mt-1">{evt.description}</p>
                  </div>
                  <span className="text-[11px] font-mono text-slate-400 whitespace-nowrap">{evt.timestamp}</span>
                </div>

                <div className="mt-3 pt-2 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-slate-400">
                  <span>Provider: {evt.provider}</span>
                  <span className="capitalize text-slate-400">Type: {evt.category}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
