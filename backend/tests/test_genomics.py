"""
HealthPulse AI — Genomics, Pharmacogenomics & ACMG Unit Tests.
"""

from backend.genomics.vcf_parser import parse_vcf_text
from backend.genomics.pharmacogenomics import PharmacogenomicsEngine, MetabolizerPhenotype
from backend.genomics.polygenic_risk import PolygenicRiskEngine
from backend.genomics.acmg_classifier import ACMGVariantClassifier, PathogenicityClass
from backend.genomics.somatic_oncology import SomaticVariantAnnotator, OncologicActionabilityTier


SAMPLE_VCF = """##fileformat=VCFv4.2
##reference=GRCh38
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE1
chr7\t140453136\trs121913343\tA\tT\t100\tPASS\tDP=60\tGT\t0/1
chr17\t41244435\trs80357906\tT\tC\t99\tPASS\tDP=45\tGT\t1/1
"""


def test_vcf_parsing():
    header, records = parse_vcf_text(SAMPLE_VCF)
    assert header.file_format == "VCFv4.2"
    assert len(records) == 2
    assert records[0].chrom == "chr7"
    assert records[0].id == "rs121913343"
    assert records[0].get_genotype("SAMPLE1") == "0/1"


def test_cyp2c19_clopidogrel_pgx():
    engine = PharmacogenomicsEngine()
    res = engine.evaluate_clopidogrel_cyp2c19("*2/*2")
    assert res.phenotype == MetabolizerPhenotype.POOR
    assert "AVOID clopidogrel" in res.dosing_recommendation
    assert "Ticagrelor" in res.therapeutic_alternatives


def test_cyp2d6_codeine_pgx():
    engine = PharmacogenomicsEngine()
    res = engine.evaluate_codeine_cyp2d6("*1/*1xN")
    assert res.phenotype == MetabolizerPhenotype.ULTRA_RAPID
    assert "AVOID" in res.dosing_recommendation


def test_acmg_pathogenic_classification():
    classifier = ACMGVariantClassifier()
    res = classifier.classify_variant(
        variant_id="BRCA1:c.5266dupC",
        gene="BRCA1",
        criteria_codes=["PVS1", "PS1", "PM2"],
    )
    assert res.classification == PathogenicityClass.PATHOGENIC


def test_somatic_annotation():
    annotator = SomaticVariantAnnotator()
    res = annotator.annotate("BRAF", "V600E", "Melanoma")
    assert res.actionability_tier == OncologicActionabilityTier.TIER_I
    assert any("Dabrafenib" in t for t in res.indicated_therapies)
