#!/usr/bin/env python3
"""
Stratify the 60 chunks by whether a "baiting" clause sits next to an
implementation-defined clause.

Registered in ../PREREGISTRATION.md section 5b, tier 1. The question, from
@RAJVEER42's capacity result: when a model wrongly extracts a parameter, does it
happen because the passage places a discovery or enumeration clause immediately
beside the implementation-defined clause, inviting the reading that a
discoverable quantity is a parameter? His case was

    "Software can discover the cache capacity through the means provided by the
     execution environment."

which is a real sentence, passes a verbatim-excerpt check, and is still the wrong
basis for a parameter, because discoverability via the execution environment is
not ISA-visibility.

If over-extraction concentrates in the baited stratum, that is a prompt gap. If
it appears regardless, it is a model prior. Different problems, different fixes.

**This labelling is done on chunk text alone and must be run before any arm C/D
result is examined.** It records nothing about models, arms or outcomes.

Registered limitation: observational and confounded. Chunks differ in more than
the adjacent clause. Minimal-edit pairs are the follow-up, only if this shows
something.

Usage:
  python label_baiting.py --udb-root ../../../.udb-corpus
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Language that delegates a choice to the implementer.
IMPL = re.compile(
    r"implementation[- ]defined|implementation[- ]specific|"
    r"implementation[s]?\s+may\b|is\s+implementation\b|"
    r"\bWARL\b|left\s+to\s+the\s+implement",
    re.I,
)

# Language inviting the "it is discoverable, therefore it is a parameter" reading.
BAIT = re.compile(
    r"\bdiscover(?:ed|able|y|s)?\b|\benumerat\w*|"
    r"software\s+can\s+(?:determine|query|read|discover)|"
    r"means\s+provided\s+by\s+the\s+execution\s+environment|"
    r"execution\s+environment|\breport(?:ed|s|ing)?\s+(?:by|through|via)\b",
    re.I,
)

SENT = re.compile(r"(?<=[.!?])\s+")


def strat(text: str) -> dict:
    """Label one chunk. Text only, no gold, no model output."""
    sentences = SENT.split(text)
    same_sentence = 0
    adjacent_sentence = 0
    impl_total = 0

    for i, s in enumerate(sentences):
        if not IMPL.search(s):
            continue
        impl_total += 1
        if BAIT.search(s):
            same_sentence += 1
            continue
        neighbours = sentences[max(0, i - 1):i] + sentences[i + 1:i + 2]
        if any(BAIT.search(n) for n in neighbours):
            adjacent_sentence += 1

    baited = same_sentence + adjacent_sentence
    return {
        "impl_clauses": impl_total,
        "baited_same_sentence": same_sentence,
        "baited_adjacent_sentence": adjacent_sentence,
        "stratum": ("baited" if baited else ("unbaited" if impl_total else "no_impl_clause")),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--udb-root", type=Path, required=True)
    args = ap.parse_args()

    udb = args.udb_root.resolve()
    inv = json.loads((ROOT.parent / "results" / "artifact_a_chunk_inventory.json")
                     .read_text(encoding="utf-8"))
    scored = [c["chunk_id"] for c in inv["chunks"]]

    out = {}
    for cid in scored:
        p = udb / "param_extraction" / "chunks" / f"{cid}.txt"
        if not p.exists():
            continue
        out[cid] = strat(p.read_text(encoding="utf-8", errors="replace"))

    counts = {}
    for v in out.values():
        counts[v["stratum"]] = counts.get(v["stratum"], 0) + 1

    print(f"chunks labelled: {len(out)}")
    for k in ("baited", "unbaited", "no_impl_clause"):
        print(f"  {k:<16} {counts.get(k, 0)}")
    tot_impl = sum(v["impl_clauses"] for v in out.values())
    tot_bait = sum(v["baited_same_sentence"] + v["baited_adjacent_sentence"]
                   for v in out.values())
    print(f"\nimplementation-defined clauses found : {tot_impl}")
    print(f"  of which baited                    : {tot_bait}"
          f"  ({100.0 * tot_bait / tot_impl:.1f}%)" if tot_impl else "")

    d = ROOT / "analysis"
    d.mkdir(exist_ok=True)
    (d / "baiting_strata.json").write_text(
        json.dumps({
            "note": "Labelled from chunk text only, before any arm C/D result was "
                    "examined. Observational and confounded: chunks differ in more "
                    "than the adjacent clause.",
            "registered": "../PREREGISTRATION.md section 5b, tier 1",
            "counts": counts,
            "per_chunk": out,
        }, indent=2), encoding="utf-8")
    print(f"\nwrote {d / 'baiting_strata.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
