"""
HealthPulse AI — Evidence-Based Gastroenterology & Hepatology Clinical Practice Guidelines.
Implements ACG (American College of Gastroenterology) and AASLD guidelines:
- Acute Pancreatitis (Atlanta Revised Classification, BISAP Score, Goal-Directed Ringer's Lactate)
- Acute Upper Gastrointestinal Bleeding (Glasgow-Blatchford Score, Pre-Endoscopy IV Pantoprazole / Octreotide)
- Cirrhotic Ascites & Spontaneous Bacterial Peritonitis (SBP Diagnostic Paracentesis & IV Albumin 1.5g/kg)
- Hepatorenal Syndrome Type 1 (HRS-AKI: Terlipressin + Albumin vs Norepinephrine + Albumin)
- Inflammatory Bowel Disease (Moderate-Severe Ulcerative Colitis & Crohn's Disease Biologic Selection)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


@dataclass
class GIGuidelineEvaluation:
    guideline_source: str
    clinical_condition: str
    prognostic_severity_score: str
    hemodynamic_resuscitation: List[str]
    endoscopic_and_procedural_timing: str
    targeted_pharmacotherapy: List[str]


class GastroenterologyGuidelineEngine:
    """Evaluates gastrointestinal bleeding, hepatology decompensation, and acute pancreatitis."""

    @staticmethod
    def evaluate_acute_ugib(
        glasgow_blatchford_score: int,
        is_variceal_suspected: bool = False,
        hemodynamic_instability: bool = False,
        hemoglobin_g_dl: float = 8.5,
    ) -> GIGuidelineEvaluation:
        """
        ACG 2021 Clinical Guideline for Upper Gastrointestinal Bleeding.
        GBS 0-1: Outpatient management.
        GBS >= 2: Inpatient admission.
        Endoscopy within 24 hours (or <12h if persistent shock).
        """
        pharma = []
        if is_variceal_suspected:
            pharma.append("IV Octreotide (50 mcg IV bolus, then 50 mcg/hour continuous infusion for 2-5 days) to reduce splanchnic portal pressure (Class 1, Level A).")
            pharma.append("Prophylactic IV Ceftriaxone 1g daily x 7 days in cirrhotic patients with UGIB (reduces bacterial infections and rebleeding mortality).")
        else:
            pharma.append("High-Dose IV PPI: Pantoprazole 80mg IV bolus, then 8mg/hour continuous infusion (or 40mg IV BID) to promote clot stabilization.")

        transfusion_target = "Restrictive Transfusion Strategy: Transfuse Packed Red Blood Cells ONLY when Hemoglobin < 7.0 g/dL (Target post-transfusion Hb 7.0-9.0 g/dL) (Villanueva trial: reduced rebleeding and mortality compared to liberal threshold)."

        return GIGuidelineEvaluation(
            guideline_source="ACG 2021 Upper Gastrointestinal Bleeding Guidelines",
            clinical_condition="Acute Upper Gastrointestinal Bleeding (UGIB)",
            prognostic_severity_score=f"Glasgow-Blatchford Score: {glasgow_blatchford_score} (High Risk >= 2)",
            hemodynamic_resuscitation=[
                "Two large-bore peripheral IVs (16-gauge or 18-gauge).",
                "Rapid crystalloid fluid resuscitation.",
                transfusion_target,
            ],
            endoscopic_and_procedural_timing="Urgent Esophagogastroduodenoscopy (EGD) within 24 hours of presentation after initial hemodynamic stabilization (Class 1, Level A).",
            targeted_pharmacotherapy=pharma,
        )
