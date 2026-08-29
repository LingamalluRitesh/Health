"use client";

import React from "react";
import { Header } from "../../components/Header";
import { MerkleAuditViewer } from "../../components/MerkleAuditViewer";

export default function AuditPage() {
  return (
    <main className="flex-1 flex flex-col overflow-y-auto">
      <Header
        title="HIPAA Security & Cryptographic Merkle Audit Trail"
        subtitle="Immutable append-only ledger with automated tampering and break-glass detection"
      />

      <div className="p-6 space-y-6 max-w-7xl mx-auto w-full">
        {/* Merkle Audit Viewer Component */}
        <MerkleAuditViewer />
      </div>
    </main>
  );
}
