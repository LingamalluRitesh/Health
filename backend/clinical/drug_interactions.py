"""
HealthPulse AI — Drug-Drug Interaction (DDI) & Pharmacokinetic Matrix Engine.
Identifies major, moderate, and minor drug interactions, CYP enzyme collisions,
QT-interval prolongation synergies, and serotonin toxicity risks.
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class InteractionSeverity(str, Enum):
    CONTRAINDICATED = "contraindicated"
    MAJOR = "major"
    MODERATE = "moderate"
    MINOR = "minor"
    NO_INTERACTION = "no_interaction"


@dataclass
class DrugInteractionResult:
    drug_a: str
    drug_b: str
    severity: InteractionSeverity
    mechanism: str
    clinical_effect: str
    management_advice: str


class DrugInteractionChecker:
    """Clinical Drug Interaction Knowledge Base and Graph Evaluator."""

    def __init__(self):
        self._interaction_db: Dict[Tuple[str, str], DrugInteractionResult] = {}
        self._cyp_substrates: Dict[str, List[str]] = {}
        self._cyp_inhibitors: Dict[str, List[str]] = {}
        self._cyp_inducers: Dict[str, List[str]] = {}
        self._qt_prolonging_drugs: Set[str] = set()
        self._serotonergic_drugs: Set[str] = set()
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        # Known severe interactions
        self._add_rule(
            "warfarin",
            "aspirin",
            InteractionSeverity.MAJOR,
            "Pharmacodynamic synergism in hemostasis impairment",
            "Marked increase in risk of major gastrointestinal and intracranial hemorrhage.",
            "Avoid co-administration unless specifically indicated (e.g. mechanical heart valve + PCI). Monitor INR closely.",
        )
        self._add_rule(
            "warfarin",
            "amiodarone",
            InteractionSeverity.MAJOR,
            "CYP2C9 and CYP3A4 inhibition by amiodarone",
            "Significant decrease in warfarin metabolism resulting in supratherapeutic INR and bleed risk.",
            "Reduce warfarin dose by 33% to 50% upon initiating amiodarone. Monitor weekly INR.",
        )
        self._add_rule(
            "simvastatin",
            "clarithromycin",
            InteractionSeverity.CONTRAINDICATED,
            "Potent CYP3A4 inhibition by clarithromycin",
            "Substantial rise in simvastatin AUC (up to 10-fold), precipitating severe rhabdomyolysis and acute renal failure.",
            "Suspend simvastatin therapy during clarithromycin antibiotic course, or use azithromycin.",
        )
        self._add_rule(
            "fluoxetine",
            "tramadol",
            InteractionSeverity.MAJOR,
            "Serotonin reuptake inhibition plus CYP2D6 competition",
            "Risk of life-threatening Serotonin Syndrome and lowered seizure threshold.",
            "Avoid concomitant therapy. Monitor for tremor, hyperreflexia, agitation, and clonus.",
        )
        self._add_rule(
            "methotrexate",
            "ibuprofen",
            InteractionSeverity.MAJOR,
            "Inhibition of renal tubular secretion of methotrexate by NSAID",
            "Methotrexate toxicity including severe bone marrow suppression and hepatotoxicity.",
            "Avoid high-dose methotrexate co-prescription with NSAIDs. Substitute acetaminophen for analgesia.",
        )
        self._add_rule(
            "lisinopril",
            "spironolactone",
            InteractionSeverity.MODERATE,
            "Additive potassium retention",
            "Hyperkalemia risk, potentially causing cardiac dysrhythmias.",
            "Check serum potassium and creatinine within 1-2 weeks of initiation.",
        )
        self._add_rule(
            "clopidogrel",
            "omeprazole",
            InteractionSeverity.MODERATE,
            "CYP2C19 inhibition by omeprazole",
            "Decreased conversion of clopidogrel to active thiol metabolite; reduced antiplatelet efficacy.",
            "Switch to pantoprazole or famotidine for gastroprotection.",
        )
        self._add_rule(
            "ciprofloxacin",
            "ondansetron",
            InteractionSeverity.MAJOR,
            "Additive cardiac ventricular repolarization delay (hERG potassium channel blockade)",
            "Prolonged QT interval and increased risk of Torsades de Pointes ventricular arrhythmia.",
            "Obtain baseline ECG. Correct hypokalemia/hypomagnesemia or choose non-QT prolonging antiemetic.",
        )

        # Categorical drug lists
        self._qt_prolonging_drugs = {
            "amiodarone", "sotalol", "haloperidol", "ondansetron",
            "ciprofloxacin", "levofloxacin", "clarithromycin", "erythromycin",
            "methadone", "citalopram", "escitalopram"
        }
        self._serotonergic_drugs = {
            "fluoxetine", "sertraline", "paroxetine", "citalopram",
            "escitalopram", "venlafaxine", "duloxetine", "tramadol",
            "fentanyl", "linezolid", "methylene blue", "selegiline"
        }

    def _add_rule(
        self,
        drug_a: str,
        drug_b: str,
        severity: InteractionSeverity,
        mechanism: str,
        effect: str,
        advice: str,
    ):
        d1 = drug_a.strip().lower()
        d2 = drug_b.strip().lower()
        res = DrugInteractionResult(
            drug_a=d1,
            drug_b=d2,
            severity=severity,
            mechanism=mechanism,
            clinical_effect=effect,
            management_advice=advice,
        )
        self._interaction_db[(d1, d2)] = res
        self._interaction_db[(d2, d1)] = res

    def check_pair(self, drug_a: str, drug_b: str) -> Optional[DrugInteractionResult]:
        """Checks a specific pair of medications."""
        d1 = drug_a.strip().lower()
        d2 = drug_b.strip().lower()
        
        # Direct database hit
        if (d1, d2) in self._interaction_db:
            return self._interaction_db[(d1, d2)]

        # Class rule: QT-Prolongation synergy
        if d1 in self._qt_prolonging_drugs and d2 in self._qt_prolonging_drugs:
            return DrugInteractionResult(
                drug_a=d1,
                drug_b=d2,
                severity=InteractionSeverity.MAJOR,
                mechanism="Synergistic hERG cardiac potassium channel blockade",
                clinical_effect="Additive QTc prolongation and high risk of Torsades de Pointes.",
                management_advice="Obtain continuous telemetry monitoring and serial ECGs.",
            )

        # Class rule: Serotonin toxicity
        if d1 in self._serotonergic_drugs and d2 in self._serotonergic_drugs:
            return DrugInteractionResult(
                drug_a=d1,
                drug_b=d2,
                severity=InteractionSeverity.MAJOR,
                mechanism="Dual serotonergic transmission augmentation",
                clinical_effect="Elevated risk of Hunter Criteria Serotonin Syndrome.",
                management_advice="Monitor for hyperthermia, rigidity, and autonomic instability.",
            )

        return None

    def check_medication_list(self, drug_list: List[str]) -> List[DrugInteractionResult]:
        """Performs full pairwise combinatorial interaction check for an active medication regimen."""
        interactions: List[DrugInteractionResult] = []
        seen_pairs: Set[Tuple[str, str]] = set()

        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                d1 = drug_list[i].strip().lower()
                d2 = drug_list[j].strip().lower()
                pair_key = tuple(sorted([d1, d2]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                result = self.check_pair(d1, d2)
                if result is not None:
                    interactions.append(result)

        return interactions
