"""
HealthPulse AI — Variant Call Format (VCF v4.2 / v4.3) Parser.
Parses genomic variant headers, chromosome coordinates, alleles, genotype calls (GT), and depth (DP).
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from backend.core.exceptions import GenomicAnalysisException


@dataclass
class VCFHeader:
    file_format: str
    reference: Optional[str]
    info_fields: Dict[str, Dict[str, str]]
    format_fields: Dict[str, Dict[str, str]]
    filter_fields: Dict[str, Dict[str, str]]
    sample_names: List[str]


@dataclass
class VCFRecord:
    chrom: str
    pos: int
    id: str
    ref: str
    alt: List[str]
    qual: Optional[float]
    filter: str
    info: Dict[str, Any]
    genotypes: Dict[str, Dict[str, str]] = field(default_factory=dict)

    @property
    def is_snp(self) -> bool:
        return len(self.ref) == 1 and all(len(a) == 1 for a in self.alt)

    @property
    def is_indel(self) -> bool:
        return len(self.ref) != 1 or any(len(a) != 1 for a in self.alt)

    def get_genotype(self, sample_name: str) -> str:
        s_data = self.genotypes.get(sample_name, {})
        return s_data.get("GT", "./.")


def parse_vcf_text(vcf_text: str) -> Tuple[VCFHeader, List[VCFRecord]]:
    """Parses full raw VCF string into header and list of variant records."""
    lines = vcf_text.strip().split("\n")
    if not lines:
        raise GenomicAnalysisException("Empty VCF content")

    info_defs: Dict[str, Dict[str, str]] = {}
    format_defs: Dict[str, Dict[str, str]] = {}
    filter_defs: Dict[str, Dict[str, str]] = {}
    sample_names: List[str] = []
    file_format = "VCFv4.2"
    reference = None

    records: List[VCFRecord] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("##"):
            # Meta-information line
            if line.startswith("##fileformat="):
                file_format = line.split("=", 1)[1]
            elif line.startswith("##reference="):
                reference = line.split("=", 1)[1]
            elif line.startswith("##INFO="):
                # parse ID
                parts = line[7:-1].split(",", 3)
                info_id = parts[0].split("=")[1]
                info_defs[info_id] = {"raw": line}
            elif line.startswith("##FORMAT="):
                parts = line[9:-1].split(",", 3)
                fmt_id = parts[0].split("=")[1]
                format_defs[fmt_id] = {"raw": line}
        elif line.startswith("#CHROM"):
            # Header column line
            cols = line.split("\t")
            if len(cols) > 9:
                sample_names = cols[9:]
        else:
            # Variant data line
            cols = line.split("\t")
            if len(cols) < 8:
                continue

            chrom = cols[0]
            try:
                pos = int(cols[1])
            except ValueError:
                pos = 0

            var_id = cols[2]
            ref = cols[3]
            alt = cols[4].split(",")
            
            qual = None
            if cols[5] != ".":
                try:
                    qual = float(cols[5])
                except ValueError:
                    pass

            flt = cols[6]
            
            # INFO field parsing
            info_dict: Dict[str, Any] = {}
            for item in cols[7].split(";"):
                if "=" in item:
                    k, v = item.split("=", 1)
                    info_dict[k] = v
                else:
                    info_dict[item] = True

            genotype_dict: Dict[str, Dict[str, str]] = {}
            if len(cols) >= 9:
                fmt_keys = cols[8].split(":")
                for s_idx, s_name in enumerate(sample_names):
                    col_idx = 9 + s_idx
                    if col_idx < len(cols):
                        s_vals = cols[col_idx].split(":")
                        g_map = {k: v for k, v in zip(fmt_keys, s_vals)}
                        genotype_dict[s_name] = g_map

            records.append(
                VCFRecord(
                    chrom=chrom,
                    pos=pos,
                    id=var_id,
                    ref=ref,
                    alt=alt,
                    qual=qual,
                    filter=flt,
                    info=info_dict,
                    genotypes=genotype_dict,
                )
            )

    header = VCFHeader(
        file_format=file_format,
        reference=reference,
        info_fields=info_defs,
        format_fields=format_defs,
        filter_fields=filter_defs,
        sample_names=sample_names,
    )
    return header, records
