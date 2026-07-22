"""
Conservative adoc_file → UDB extension name guesses for draft `definedBy`.

These are **drafts**, not ground truth. Prefer copying `definedBy` from an
existing UDB param YAML when one exists (see csv_to_param_yaml).
"""

from __future__ import annotations

import re

# Stem of isa-manual src/*.adoc → extension name matching
# schema_defs extension_name: ^(([A-WY])|([SXZ][a-z0-9]+))$
_ADOC_STEM_TO_EXT: dict[str, str] = {
    "machine": "Sm",
    "supervisor": "S",
    "hypervisor": "H",
    "priv-csrs": "Sm",
    "counters": "Smcdeleg",  # weak; often Sm — see note in exporter
    "smstateen": "Smstateen",
    "ssstateen": "Ssstateen",
    "priv-cfi": "Smcdeleg",
    "unpriv-cfi": "Zicfiss",
    "cmo": "Zicbom",
    "a-st-ext": "A",
    "c-st-ext": "C",
    "f-st-ext": "F",
    "d-st-ext": "D",
    "v-st-ext": "V",
    "b-st-ext": "B",
    "zc": "Zca",
    "zabha": "Zabha",
    "zfinx": "Zfinx",
    "zpm": "Zpm",
    "rvwmo": "A",  # weak
    "indirect-csr": "Smcsrind",
    "intro": "I",
    "bfloat16": "Zfbfmin",
}


def guess_extension(adoc_file: str) -> tuple[str, str]:
    """
    Return (extension_name, confidence) where confidence is
    'mapped' | 'filename' | 'fallback'.
    """
    if not adoc_file:
        return "Sm", "fallback"

    stem = adoc_file
    if stem.lower().endswith(".adoc"):
        stem = stem[: -len(".adoc")]
    stem_l = stem.lower()

    if stem_l in _ADOC_STEM_TO_EXT:
        return _ADOC_STEM_TO_EXT[stem_l], "mapped"

    # Sm* / Ss* / Z* style filenames often match extension names.
    # e.g. smcntrpmf.adoc → Smcntrpmf is not always right; only if pattern fits.
    if re.fullmatch(r"[A-WY]", stem):
        return stem, "filename"
    if re.fullmatch(r"[SXZ][a-z0-9]+", stem, flags=re.IGNORECASE):
        # Normalize: first letter upper for S/X/Z, rest lower as UDB does for Sm*
        name = stem[0].upper() + stem[1:].lower()
        if re.fullmatch(r"([A-WY])|([SXZ][a-z0-9]+)", name):
            return name, "filename"

    return "Sm", "fallback"
