"""Artifact A: multi-model agreement and hallucination-overlap (offline).

Does not call LLMs. Consumes Part I-style merged/deduped result JSON.
"""

from .agreement import (
    AgreementReport,
    compute_agreement,
    compute_hallucination_overlap,
    params_by_name,
)
from .load_results import load_param_list, load_udb_names

__all__ = [
    "AgreementReport",
    "compute_agreement",
    "compute_hallucination_overlap",
    "load_param_list",
    "load_udb_names",
    "params_by_name",
]
