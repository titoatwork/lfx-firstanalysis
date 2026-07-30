# Copyright (c) 2026 titoatwork
# SPDX-License-Identifier: BSD-3-Clause-Clear

"""Audit the pinned gold's parameter classifications against UDB structure.

The gold assigns every parameter one class from taxonomy.md. Those labels were
produced by an LLM with a confidence and a free-text reason. This script does not
re-run a model. It derives, from the UnifiedDB data alone, which parameters are the
legal-value set of a CSR field, and reports where that disagrees with the gold.

The derivation uses how the IDL actually consumes a parameter, not its schema shape
and not its name. Two idioms mark a parameter as a field's legal-value set, and both
come straight from taxonomy.md's own definition of NORM_CSR_WARL, "the parameter IS
the set of legal values":

  membership   $array_includes?(P, csr_value.X)   legalises a write against P
  cardinality  $array_size(P) <op>                the size of P decides RO vs RW

Run:
    python scripts/audit_gold_classification.py [--udb PATH] [--gold PATH]

Exits non-zero if the audit cannot run. Disagreements are data, not failures, so
they are reported and the script still exits 0.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

MEMBERSHIP = re.compile(r"\$array_includes\?\(\s*([A-Z][A-Z0-9_]+)")
CARDINALITY = re.compile(r"\$array_size\(\s*([A-Z][A-Z0-9_]+)\s*\)\s*[<>=!]")
NAME_RECOGNITION = re.compile(r"^Well-known architectural parameter")

# Only the two idioms above decide the question mechanically. A legal-value set is
# also encoded as a family of booleans, one per legal value, and there the same
# syntax serves both roles: `if (SATP_MODE_BARE && csr_value.MODE == 0)` decides
# whether one value is legal, while `if (JVT_READ_ONLY) return ...` gates mutability.
# Both sit inside sw_write, both are a bare boolean test, and separating them needs
# the surrounding logic rather than a pattern. Two attempts at a heuristic are
# recorded in this file's history; both misclassified cases verified by hand.
#
# So this script does not guess. It reports which gold labels the data decides, which
# refer to parameters that no longer exist, and which fall in the region where the
# taxonomy's two classes are not syntactically separable. That region is the finding.
LEGAL_VALUE_CLASS = "NORM_CSR_WARL"


def csr_sources(udb: str) -> list[str]:
    pat = os.path.join(udb, "spec", "std", "isa", "csr", "**", "*.yaml")
    return sorted(set(glob.glob(pat, recursive=True)))


def legal_value_set_params(udb: str) -> dict[str, set[str]]:
    """Map parameter -> the decidable idioms that make it a field's legal-value set."""
    found: dict[str, set[str]] = {}
    for path in csr_sources(udb):
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        body = "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("#")
        )
        for name in MEMBERSHIP.findall(body):
            found.setdefault(name, set()).add("membership")
        for name in CARDINALITY.findall(body):
            found.setdefault(name, set()).add("cardinality")
    return found


def udb_param_names(udb: str) -> set[str]:
    pat = os.path.join(udb, "spec", "std", "isa", "param", "*.yaml")
    return {os.path.basename(p)[:-5] for p in glob.glob(pat)}


def load_gold(path: str) -> dict[str, dict]:
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    return {p["name"]: p for p in doc["parameters"]}


def audit(udb: str, gold_path: str) -> dict:
    gold = load_gold(gold_path)
    known = udb_param_names(udb)
    evidence = legal_value_set_params(udb)

    agree, disagree, absent = [], [], []
    for name, idioms in sorted(evidence.items()):
        entry = gold.get(name)
        if entry is None:
            absent.append(name)
            continue
        actual = entry.get("classification")
        row = {
            "name": name,
            "gold": actual,
            "derived": LEGAL_VALUE_CLASS,
            "idioms": sorted(idioms),
            "confidence": entry.get("classification_confidence"),
            "reason": (entry.get("classification_reasoning") or "").strip(),
        }
        (agree if actual == LEGAL_VALUE_CLASS else disagree).append(row)

    name_only = [
        p["name"]
        for p in gold.values()
        if NAME_RECOGNITION.match((p.get("classification_reasoning") or "").strip())
    ]

    # gold entries labelled WARL that no evidence supports, split by cause
    warl_gold = [n for n, p in gold.items() if p.get("classification") == LEGAL_VALUE_CLASS]
    unsupported = [n for n in warl_gold if n not in evidence]
    stale = sorted(n for n in unsupported if n not in known)
    undecidable = sorted(n for n in unsupported if n in known)

    return {
        "gold_size": len(gold),
        "evidence_params": len(evidence),
        "agree": agree,
        "disagree": disagree,
        "not_in_gold": absent,
        "name_recognition": sorted(name_only),
        "warl_in_gold": len(warl_gold),
        "warl_stale": stale,
        "warl_undecidable": undecidable,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--udb", default="../riscv-unified-db")
    ap.add_argument(
        "--gold", default="../.udb-corpus/param_extraction/data/ground_truth.json"
    )
    ap.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = ap.parse_args()

    if not os.path.isdir(args.udb):
        print(f"error: --udb path not found: {args.udb}", file=sys.stderr)
        return 2
    if not os.path.isfile(args.gold):
        print(f"error: --gold path not found: {args.gold}", file=sys.stderr)
        return 2

    r = audit(args.udb, args.gold)
    if args.json:
        print(json.dumps(r, indent=2))
        return 0

    print(f"gold entries                     : {r['gold_size']}")
    print(f"parameters used as a legal-value set in the IDL : {r['evidence_params']}")
    print(f"  of those, present in the gold  : {len(r['agree']) + len(r['disagree'])}")
    print(f"  agreeing with the gold         : {len(r['agree'])}")
    print(f"  disagreeing                    : {len(r['disagree'])}")
    print(f"  not in the pinned gold         : {len(r['not_in_gold'])} {r['not_in_gold']}")
    print()
    print(f"classified by name recognition alone : {len(r['name_recognition'])}")
    print()

    if r["disagree"]:
        print("A. legal-value sets the gold calls NORM_DIRECT")
        for row in r["disagree"]:
            print(f"  {row['name']}")
            print(f"    gold       : {row['gold']}  (confidence: {row['confidence']})")
            print(f"    derived    : {row['derived']}")
            print(f"    idioms     : {', '.join(row['idioms'])}")
            print(f"    gold reason: {row['reason'][:90]}")
        print()

    print(f"B. gold entries labelled {LEGAL_VALUE_CLASS}: {r['warl_in_gold']}")
    print(f"     confirmed by a decidable idiom : {len(r['agree'])}")
    print(f"     parameter no longer in UDB     : {len(r['warl_stale'])} {r['warl_stale']}")
    print(f"     not decidable from syntax      : {len(r['warl_undecidable'])}")
    for n in r["warl_undecidable"]:
        print(f"       {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
