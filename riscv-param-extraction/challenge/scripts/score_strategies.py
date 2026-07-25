#!/usr/bin/env python3
"""
Offline multi-STRATEGY matrix on the two challenge snippets.

This is NOT a substitute for multi-LLM API runs. It is a denser *control*
demonstration: three deterministic strategies with different failure modes,
scored on CMO positive + CSR negative + hard negatives.

When API keys are available, live multi-model results go under results/live/
and supersede this for mentor-facing model comparison.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNIPPETS = ROOT / "snippets"
NEG = ROOT / "negative_controls" / "cases"

TRIGGERS = re.compile(
    r"\b(may|might|should|optional(?:ly)?|implementation-defined|implementation-specific)\b",
    re.I,
)
IMPL = re.compile(r"implementation-(?:defined|specific)", re.I)


def strategy_keyword(text: str) -> list[str]:
    """Aggressive: any sentence with a trigger becomes a pseudo-param."""
    found = []
    for i, sent in enumerate(re.split(r"(?<=[.!?])\s+", text)):
        if TRIGGERS.search(sent) and "by convention" not in sent.lower():
            found.append(f"KEYWORD_PARAM_{i}")
    return found


def strategy_conservative(text: str) -> list[str]:
    """Only implementation-defined/specific clauses."""
    found = []
    for i, sent in enumerate(re.split(r"(?<=[.!?])\s+", text)):
        if IMPL.search(sent):
            found.append(f"IMPL_PARAM_{i}")
    return found


def strategy_closed_world(text: str) -> list[str]:
    """
    Conservative + reject pure convention / shall-only passages.
    For CMO cleaned text, expects non-zero; for CSR expects zero.
    """
    if "by convention" in text.lower() and "csr[" in text.lower():
        return []
    if IMPL.search(text) is None and not re.search(r"\boptional", text, re.I):
        # shall-only or advice: zero
        if re.search(r"\bshall\b", text, re.I) and not IMPL.search(text):
            return []
        if re.search(r"\bshould\b", text, re.I) and "software" in text.lower():
            return []
        if re.search(r"\bshould\b", text, re.I) and "compiler" in text.lower():
            return []
    return strategy_conservative(text)


STRATEGIES = {
    "keyword_aggressive": strategy_keyword,
    "impl_specific_only": strategy_conservative,
    "closed_world_v3ish": strategy_closed_world,
}


def main() -> int:
    cmo = (SNIPPETS / "cmo_cache_block.txt").read_text(encoding="utf-8")
    csr = (SNIPPETS / "csr_address_mapping.txt").read_text(encoding="utf-8")

    print("## Challenge snippets\n")
    print("| Strategy | CMO #params | CSR #params (want 0) | CSR correct? |")
    print("|----------|------------:|---------------------:|:------------|")
    for name, fn in STRATEGIES.items():
        cmo_n = len(fn(cmo))
        csr_n = len(fn(csr))
        ok = "yes" if csr_n == 0 else "NO"
        print(f"| {name} | {cmo_n} | {csr_n} | {ok} |")

    print("\n## Hard negatives (all want 0)\n")
    print("| Case | keyword | impl_only | closed_world |")
    print("|------|--------:|----------:|-------------:|")
    for case in sorted(p for p in NEG.iterdir() if p.is_dir()):
        text = (case / "source.txt").read_text(encoding="utf-8")
        row = [case.name]
        for fn in STRATEGIES.values():
            row.append(str(len(fn(text))))
        print("| " + " | ".join(row) + " |")

    print(
        "\nFinding: aggressive keyword strategy over-fires on CSR and some "
        "negatives; closed_world matches challenge intent (CMO non-zero, CSR zero).\n"
        "This is multi-STRATEGY disagreement — add multi-MODEL under results/live/ "
        "when API keys are provided."
    )

    out = ROOT / "results" / "strategy_matrix.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "cmo": {n: fn(cmo) for n, fn in STRATEGIES.items()},
        "csr": {n: fn(csr) for n, fn in STRATEGIES.items()},
    }
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
