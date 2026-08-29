"use client";

import React, { useEffect, useRef, useState } from "react";
import { Activity, Heart, Wind, Droplets } from "lucide-react";

export function VitalWaveformChart() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [heartRate, setHeartRate] = useState<number>(76);
  const [spo2, setSpo2] = useState<number>(98);
  const [respiratoryRate, setRespiratoryRate] = useState<number>(16);
  const [bloodPressure, setBloodPressure] = useState<string>("120/78");

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let step = 0;
    const width = canvas.width;
    const height = canvas.height;
    const ecgBuffer: number[] = new Array(width).fill(height / 2);

    let animationId: number;

    const render = () => {
      step = (step + 2) % width;

      // Synthetic ECG Lead II waveform generator
      const t = (step % 80) / 80;
      let yOffset = height / 2;

      // P wave, QRS complex, T wave
      if (t >= 0.1 && t < 0.2) {
        yOffset -= Math.sin(((t - 0.1) / 0.1) * Math.PI) * 8; // P wave
      } else if (t >= 0.22 && t < 0.25) {
        yOffset += 6; // Q wave
      } else if (t >= 0.25 && t < 0.30) {
        yOffset -= 38; // R peak
      } else if (t >= 0.30 && t < 0.33) {
        yOffset += 14; // S wave
      } else if (t >= 0.45 && t < 0.60) {
        yOffset -= Math.sin(((t - 0.45) / 0.15) * Math.PI) * 12; // T wave
      }

      ecgBuffer[step] = yOffset;

      // Clear & Draw grid
      ctx.fillStyle = "#020617";
      ctx.fillRect(0, 0, width, height);

      ctx.strokeStyle = "rgba(15, 45, 25, 0.4)";
      ctx.lineWidth = 0.5;
      for (let x = 0; x < width; x += 20) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += 20) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Draw ECG Trace
      ctx.strokeStyle = "#22c55e";
      ctx.lineWidth = 1.8;
      ctx.beginPath();

      for (let x = 0; x < width; x++) {
        const y = ecgBuffer[x];
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // Sweep erase cursor
      ctx.fillStyle = "#020617";
      ctx.fillRect(step + 1, 0, 12, height);

      animationId = requestAnimationFrame(render);
    };

    render();

    // Minor random vital oscillation interval
    const interval = setInterval(() => {
      setHeartRate(Math.floor(74 + Math.random() * 5));
      setSpo2(Math.floor(97 + Math.random() * 2));
      setRespiratoryRate(Math.floor(15 + Math.random() * 3));
    }, 2000);

    return () => {
      cancelAnimationFrame(animationId);
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-emerald-400 animate-pulse" />
          <h3 className="font-semibold text-sm tracking-wide">Continuous ECG Lead II & ICU Vital Telemetry</h3>
        </div>
        <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
          Telemetry: Active
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* Waveform Canvas */}
        <div className="lg:col-span-3 bg-slate-950 rounded-lg border border-slate-800 p-2 overflow-hidden">
          <canvas ref={canvasRef} width={600} height={180} className="w-full h-44 rounded" />
        </div>

        {/* Vital Readouts Column */}
        <div className="grid grid-cols-2 lg:grid-cols-1 gap-2.5">
          <div className="bg-slate-950/80 p-3 rounded-lg border border-emerald-900/40 flex items-center justify-between">
            <div>
              <span className="text-[10px] uppercase font-semibold text-slate-400">Heart Rate (ECG)</span>
              <div className="text-2xl font-bold text-emerald-400">{heartRate} <span className="text-xs font-normal text-slate-400">bpm</span></div>
            </div>
            <Heart className="w-5 h-5 text-emerald-500" />
          </div>

          <div className="bg-slate-950/80 p-3 rounded-lg border border-blue-900/40 flex items-center justify-between">
            <div>
              <span className="text-[10px] uppercase font-semibold text-slate-400">Pulse Oximetry (SpO2)</span>
              <div className="text-2xl font-bold text-blue-400">{spo2}%</div>
            </div>
            <Droplets className="w-5 h-5 text-blue-500" />
          </div>

          <div className="bg-slate-950/80 p-3 rounded-lg border border-amber-900/40 flex items-center justify-between">
            <div>
              <span className="text-[10px] uppercase font-semibold text-slate-400">Blood Pressure (NIBP)</span>
              <div className="text-xl font-bold text-amber-400">{bloodPressure} <span className="text-xs font-normal text-slate-400">mmHg</span></div>
            </div>
            <Activity className="w-5 h-5 text-amber-500" />
          </div>

          <div className="bg-slate-950/80 p-3 rounded-lg border border-teal-900/40 flex items-center justify-between">
            <div>
              <span className="text-[10px] uppercase font-semibold text-slate-400">Respiratory Rate</span>
              <div className="text-xl font-bold text-teal-400">{respiratoryRate} <span className="text-xs font-normal text-slate-400">/min</span></div>
            </div>
            <Wind className="w-5 h-5 text-teal-500" />
          </div>
        </div>
      </div>
    </div>
  );
}
