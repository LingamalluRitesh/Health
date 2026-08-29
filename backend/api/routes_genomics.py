"""
HealthPulse AI — Precision Genomics & Pharmacogenomics Endpoints.
"""

from fastapi import APIRouter
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from backend.genomics.pharmacogenomics import PharmacogenomicsEngine
from backend.genomics.polygenic_risk import PolygenicRiskEngine
from backend.genomics.acmg_classifier import ACMGVariantClassifier
from backend.genomics.somatic_oncology import SomaticVariantAnnotator


router = APIRouter()
pgx_engine = PharmacogenomicsEngine()
prs_engine = PolygenicRiskEngine()
acmg_engine = ACMGVariantClassifier()
somatic_engine = SomaticVariantAnnotator()


class PGxRequest(BaseModel):
    gene: str = Field(..., example="CYP2C19")
    diplotype: str = Field(..., example="*2/*3")
    target_drug: str = Field(..., example="Clopidogrel")


class ACMGRequest(BaseModel):
    variant_id: str = Field(..., example="NM_000059.3:c.5266dupC")
    gene: str = Field(..., example="BRCA1")
    criteria_codes: List[str] = Field(..., example=["PVS1", "PS1", "PM2"])


class SomaticRequest(BaseModel):
    gene: str = Field(..., example="BRAF")
    alteration: str = Field(..., example="V600E")
    cancer_type: str = Field("Melanoma", example="Melanoma")


@router.post("/pgx-guideline")
def evaluate_pgx(payload: PGxRequest):
    if payload.gene.upper() == "CYP2D6":
        res = pgx_engine.evaluate_codeine_cyp2d6(payload.diplotype)
    elif payload.gene.upper() == "CYP2C19":
        res = pgx_engine.evaluate_clopidogrel_cyp2c19(payload.diplotype)
    else:
        res = pgx_engine.evaluate_fluoropyrimidine_dpyd([payload.diplotype])
    return res.__dict__


@router.post("/acmg-classify")
def classify_acmg(payload: ACMGRequest):
    res = acmg_engine.classify_variant(payload.variant_id, payload.gene, payload.criteria_codes)
    return res.__dict__


@router.post("/somatic-annotate")
def annotate_somatic(payload: SomaticRequest):
    res = somatic_engine.annotate(payload.gene, payload.alteration, payload.cancer_type)
    return res.__dict__
