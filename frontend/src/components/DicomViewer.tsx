"use client";

import React, { useState, useRef, useEffect } from "react";
import { CLIENT_CT_PRESETS, renderVoiLutWindow, classifyHounsfieldDensity } from "../lib/dicomProcessing";
import { ZoomIn, ZoomOut, RotateCcw, Sliders, Eye } from "lucide-react";

export function DicomViewer() {
  const [windowCenter, setWindowCenter] = useState<number>(40);
  const [windowWidth, setWindowWidth] = useState<number>(400);
  const [selectedPreset, setSelectedPreset] = useState<string>("soft_tissue");
  const [zoomLevel, setZoomLevel] = useState<number>(1.0);
  const [hoveredHu, setHoveredHu] = useState<number | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Generate synthetic CT chest axial slice HU array (128x128)
  const [huMatrix, setHuMatrix] = useState<number[]>(() => {
    const size = 128;
    const data = new Array(size * size);
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const dx = x - size / 2;
        const dy = y - size / 2;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > 56) {
          data[y * size + x] = -1000; // Air
        } else if (dist > 50) {
          data[y * size + x] = -60;   // Subcutaneous Fat
        } else if (dist > 45) {
          data[y * size + x] = 600;   // Rib Cortical Bone
        } else {
          // Lung fields vs mediastinum
          if (x < 55 && Math.abs(dy) < 35) {
            data[y * size + x] = -750 + Math.sin(x * 0.2) * 40; // Right Lung
          } else if (x > 73 && Math.abs(dy) < 35) {
            data[y * size + x] = -750 + Math.cos(y * 0.2) * 40; // Left Lung
          } else {
            data[y * size + x] = 45 + Math.sin(dx * 0.3) * 15;  // Mediastinum & Heart
          }
        }
      }
    }
    return data;
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const size = 128;
    const rendered8Bit = renderVoiLutWindow(huMatrix, windowCenter, windowWidth);
    const imgData = ctx.createImageData(size, size);

    for (let i = 0; i < rendered8Bit.length; i++) {
      const val = rendered8Bit[i];
      const idx = i * 4;
      imgData.data[idx] = val;     // R
      imgData.data[idx + 1] = val; // G
      imgData.data[idx + 2] = val; // B
      imgData.data[idx + 3] = 255; // Alpha
    }

    ctx.putImageData(imgData, 0, 0);
  }, [huMatrix, windowCenter, windowWidth]);

  const handlePresetChange = (presetKey: string) => {
    setSelectedPreset(presetKey);
    const p = CLIENT_CT_PRESETS[presetKey];
    if (p) {
      setWindowCenter(p.windowCenter);
      setWindowWidth(p.windowWidth);
    }
  };

  const handleCanvasMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor(((e.clientX - rect.left) / rect.width) * 128);
    const y = Math.floor(((e.clientY - rect.top) / rect.height) * 128);

    if (x >= 0 && x < 128 && y >= 0 && y < 128) {
      setHoveredHu(Math.round(huMatrix[y * 128 + x]));
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
        <div>
          <h3 className="font-semibold text-base">Interactive DICOM Multi-Planar Viewer</h3>
          <p className="text-xs text-slate-400">Series: CT Chest Axial (1.25mm thin slice) | SOP UID: 1.2.840.113619.2.55</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setZoomLevel((z) => Math.min(2.5, z + 0.2))}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 rounded-md text-slate-300"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => setZoomLevel((z) => Math.max(0.6, z - 0.2))}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 rounded-md text-slate-300"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              setZoomLevel(1.0);
              handlePresetChange("soft_tissue");
            }}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 rounded-md text-slate-300"
            title="Reset View"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Canvas Display */}
        <div className="md:col-span-2 bg-black rounded-lg border border-slate-800 flex flex-col items-center justify-center p-4 relative min-h-[340px] overflow-hidden">
          <div
            style={{ transform: `scale(${zoomLevel})`, transition: "transform 0.1s ease-out" }}
            className="origin-center"
          >
            <canvas
              ref={canvasRef}
              width={128}
              height={128}
              onMouseMove={handleCanvasMouseMove}
              onMouseLeave={() => setHoveredHu(null)}
              className="w-72 h-72 image-rendering-pixelated cursor-crosshair border border-slate-900"
            />
          </div>

          {/* On-screen DICOM HUD */}
          <div className="absolute top-3 left-3 text-[11px] font-mono text-emerald-400 bg-slate-950/80 px-2 py-1 rounded">
            <div>WC: {windowCenter} | WW: {windowWidth}</div>
            <div>Zoom: {(zoomLevel * 100).toFixed(0)}%</div>
          </div>

          {hoveredHu !== null && (
            <div className="absolute bottom-3 left-3 text-[11px] font-mono bg-slate-950/90 text-white px-2.5 py-1 rounded border border-slate-700 flex items-center gap-2">
              <span className="text-amber-400">HU: {hoveredHu}</span>
              <span className="text-slate-400">|</span>
              <span>{classifyHounsfieldDensity(hoveredHu).tissue}</span>
            </div>
          )}
        </div>

        {/* Windowing & Presets Controls */}
        <div className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              CT Window Presets
            </label>
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(CLIENT_CT_PRESETS).map(([key, preset]) => (
                <button
                  key={key}
                  onClick={() => handlePresetChange(key)}
                  className={`px-2.5 py-2 rounded-lg text-xs font-medium text-left border transition-all ${
                    selectedPreset === key
                      ? "border-emerald-500 bg-emerald-950/40 text-emerald-300"
                      : "border-slate-800 bg-slate-800/60 text-slate-300 hover:border-slate-700"
                  }`}
                >
                  <div className="font-semibold">{preset.name}</div>
                  <div className="text-[10px] text-slate-400">C:{preset.windowCenter} W:{preset.windowWidth}</div>
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3 pt-2 border-t border-slate-800">
            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1">
                <span>Window Center (Level):</span>
                <span className="font-mono text-emerald-400">{windowCenter} HU</span>
              </div>
              <input
                type="range"
                min="-1000"
                max="1000"
                value={windowCenter}
                onChange={(e) => setWindowCenter(Number(e.target.value))}
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs text-slate-300 mb-1">
                <span>Window Width:</span>
                <span className="font-mono text-emerald-400">{windowWidth} HU</span>
              </div>
              <input
                type="range"
                min="1"
                max="3000"
                value={windowWidth}
                onChange={(e) => setWindowWidth(Number(e.target.value))}
                className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
