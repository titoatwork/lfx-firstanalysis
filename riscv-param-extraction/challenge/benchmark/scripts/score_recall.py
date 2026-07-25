#!/usr/bin/env python3
"""
Known-parameter re-derive score (challenge secondary benchmark).

CAVEATS (read first — same class of honesty as elite kits):
  - Cases use parameters already merged in public UDB; frontier models may have
    seen them in pretraining. This is a mechanics/sanity check, NOT a blind
    generalization estimate and NOT comparable to Spring full-corpus recall
    (e.g. 36.8% / remeasured 72.9%) on equal footing.
  - Existence = extraction recognized that a parameter is warranted.
  - Type fidelity = extracted schema.type matches ground_truth type when present.

Usage:
  python benchmark/scripts/score_recall.py
  python benchmark/scripts/score_recall.py --cases-dir benchmark/cases
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CASES = ROOT / "benchmark" / "cases"


def load_yaml(path: Path) -> dict:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError(f"not a mapping: {path}")
    return doc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-dir", type=Path, default=DEFAULT_CASES)
    args = parser.parse_args()

    cases = sorted(p for p in args.cases_dir.iterdir() if p.is_dir())
    if not cases:
        print(f"ERROR: no cases in {args.cases_dir}", file=sys.stderr)
        return 2

    print("CAVEAT: pretraining-leaky known-param re-derive — not equal to corpus GT recall.\n")

    exist_hit = 0
    type_hit = 0
    type_den = 0
    rows = []

    for case in cases:
        gt_path = case / "ground_truth.yaml"
        ex_path = case / "extraction.yaml"
        if not gt_path.is_file() or not ex_path.is_file():
            print(f"[SKIP] {case.name}: need ground_truth.yaml + extraction.yaml")
            continue
        gt = load_yaml(gt_path)
        ex = load_yaml(ex_path)
        gt_name = gt.get("name")
        ex_name = ex.get("name")
        exists = bool(ex_name) and ex.get("kind") == "parameter"
        # existence: non-empty extraction that claims a parameter
        if exists:
            exist_hit += 1
        gt_type = (gt.get("schema") or {}).get("type")
        ex_type = (ex.get("schema") or {}).get("type")
        tf = None
        if exists and gt_type is not None:
            type_den += 1
            tf = ex_type == gt_type
            if tf:
                type_hit += 1
        name_match = ex_name == gt_name
        rows.append((case.name, exists, name_match, tf, gt_type, ex_type))
        print(
            f"[{'OK' if exists else 'MISS'}] {case.name}: "
            f"exists={exists} name_match={name_match} type_fidelity={tf}"
        )

    n = len(rows)
    print(f"\nRecall (existence): {exist_hit}/{n} = {100.0 * exist_hit / n:.1f}%")
    if type_den:
        print(
            f"Schema-type fidelity (of exists with typed GT): "
            f"{type_hit}/{type_den} = {100.0 * type_hit / type_den:.1f}%"
        )
    print(
        "\nName match rate (strict): "
        f"{sum(1 for r in rows if r[2])}/{n} "
        "(renames allowed for existence; name match is stricter)"
    )
    print(
        "\nDo NOT claim this beats Spring corpus adjusted recall. "
        "Different metric, different leakage profile."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
