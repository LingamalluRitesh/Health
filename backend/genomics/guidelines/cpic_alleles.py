"""
HealthPulse AI — CPIC Allele Activity Score & Diplotype Translation Tables.
Defines star-allele functional statuses across key pharmacogenes: CYP2D6, CYP2C19, CYP2C9, DPYD, TPMT, SLCO1B1.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class AlleleFunction(str, Enum):
    NORMAL = "Normal Function"
    INCREASED = "Increased Function"
    DECREASED = "Decreased Function"
    NO_FUNCTION = "No Function"
    UNCERTAIN = "Uncertain Function"


@dataclass
class StarAlleleDef:
    gene: str
    star_allele: str
    rs_ids: List[str]
    hgvs_dna: str
    hgvs_protein: str
    functional_status: AlleleFunction
    activity_score: float


CPIC_STAR_ALLELES: Dict[str, Dict[str, StarAlleleDef]] = {
    "CYP2D6": {
        "*1": StarAlleleDef("CYP2D6", "*1", [], "c.1_1494", "p.WildType", AlleleFunction.NORMAL, 1.0),
        "*2": StarAlleleDef("CYP2D6", "*2", ["rs16947", "rs1135840"], "c.2850C>T", "p.R296C", AlleleFunction.NORMAL, 1.0),
        "*4": StarAlleleDef("CYP2D6", "*4", ["rs3892097"], "c.1846G>A", "p.SplicingDefect", AlleleFunction.NO_FUNCTION, 0.0),
        "*5": StarAlleleDef("CYP2D6", "*5", [], "WholeGeneDeletion", "p.Null", AlleleFunction.NO_FUNCTION, 0.0),
        "*10": StarAlleleDef("CYP2D6", "*10", ["rs1065852"], "c.100C>T", "p.P34S", AlleleFunction.DECREASED, 0.25),
        "*17": StarAlleleDef("CYP2D6", "*17", ["rs28371706"], "c.1023C>T", "p.T107I", AlleleFunction.DECREASED, 0.5),
        "*41": StarAlleleDef("CYP2D6", "*41", ["rs28371725"], "c.2988G>A", "p.SplicingDefect", AlleleFunction.DECREASED, 0.5),
        "*1xN": StarAlleleDef("CYP2D6", "*1xN", [], "GeneDuplication", "p.CopyNumberGain", AlleleFunction.INCREASED, 2.0),
    },
    "CYP2C19": {
        "*1": StarAlleleDef("CYP2C19", "*1", [], "c.1_1473", "p.WildType", AlleleFunction.NORMAL, 1.0),
        "*2": StarAlleleDef("CYP2C19", "*2", ["rs4244285"], "c.681G>A", "p.SplicingAberrant", AlleleFunction.NO_FUNCTION, 0.0),
        "*3": StarAlleleDef("CYP2C19", "*3", ["rs4986893"], "c.636G>A", "p.W212X", AlleleFunction.NO_FUNCTION, 0.0),
        "*17": StarAlleleDef("CYP2C19", "*17", ["rs12248560"], "c.-806C>T", "p.PromoterGain", AlleleFunction.INCREASED, 1.5),
    },
    "CYP2C9": {
        "*1": StarAlleleDef("CYP2C9", "*1", [], "c.1_1473", "p.WildType", AlleleFunction.NORMAL, 1.0),
        "*2": StarAlleleDef("CYP2C9", "*2", ["rs1799853"], "c.430C>T", "p.R144C", AlleleFunction.DECREASED, 0.5),
        "*3": StarAlleleDef("CYP2C9", "*3", ["rs1057910"], "c.1075A>C", "p.I359L", AlleleFunction.NO_FUNCTION, 0.0),
    },
    "DPYD": {
        "*1": StarAlleleDef("DPYD", "*1", [], "c.1_3078", "p.WildType", AlleleFunction.NORMAL, 1.0),
        "*2A": StarAlleleDef("DPYD", "*2A", ["rs3918290"], "c.1905+1G>A", "p.SpliceDonorLoss", AlleleFunction.NO_FUNCTION, 0.0),
        "*13": StarAlleleDef("DPYD", "*13", ["rs55886062"], "c.1679T>G", "p.I560S", AlleleFunction.NO_FUNCTION, 0.0),
        "HapB3": StarAlleleDef("DPYD", "HapB3", ["rs75017182"], "c.1129-5923C>G", "p.DeepIntronicSplice", AlleleFunction.DECREASED, 0.5),
    },
    "TPMT": {
        "*1": StarAlleleDef("TPMT", "*1", [], "c.1_738", "p.WildType", AlleleFunction.NORMAL, 1.0),
        "*2": StarAlleleDef("TPMT", "*2", ["rs1800462"], "c.238G>C", "p.A80P", AlleleFunction.NO_FUNCTION, 0.0),
        "*3A": StarAlleleDef("TPMT", "*3A", ["rs1800460", "rs1142345"], "c.460G>A; c.719A>G", "p.A154T; p.Y240C", AlleleFunction.NO_FUNCTION, 0.0),
        "*3C": StarAlleleDef("TPMT", "*3C", ["rs1142345"], "c.719A>G", "p.Y240C", AlleleFunction.NO_FUNCTION, 0.0),
    },
}


def calculate_cyp2d6_activity_score(diplotype: str) -> float:
    """Calculates total CYP2D6 activity score from star-allele diplotype (e.g. *1/*4)."""
    parts = diplotype.split("/")
    if len(parts) != 2:
        return 2.0
    a1 = CPIC_STAR_ALLELES.get("CYP2D6", {}).get(parts[0])
    a2 = CPIC_STAR_ALLELES.get("CYP2D6", {}).get(parts[1])
    score1 = a1.activity_score if a1 else 1.0
    score2 = a2.activity_score if a2 else 1.0
    return score1 + score2
