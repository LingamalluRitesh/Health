"use client";

import React from "react";
import { Header } from "../../components/Header";
import { ModelCardViewer } from "../../components/ModelCardViewer";
import { FairnessMatrixChart } from "../../components/FairnessMatrixChart";

export default function GovernancePage() {
  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="AI Model Governance, EU AI Act & FDA SaMD Studio"
        subtitle="Auditable model cards, demographic parity certification, and clinical safety compliance"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Model Card Component */}
        <ModelCardViewer />

        {/* Demographic Fairness Matrix */}
        <FairnessMatrixChart />
      </div>
    </main>
  );
}
