#!/usr/bin/env python3
"""
Score existing live multi-model dirs offline (no API).

For each results/live/<model>/:
  - CMO: count CACHE_* (or any) param YAMLs
  - CSR: PASS if NO_PARAMETERS_FOUND or zero YAMLs; FAIL if FALSE_POSITIVE or param yaml present

Usage:
  python challenge/scripts/score_live_matrix.py
  python challenge/scripts/score_live_matrix.py --json results/live/matrix_scores.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "results" / "live"

CMO_NAMES = {"CACHE_BLOCK_SIZE", "CACHE_CAPACITY", "CACHE_ORGANIZATION"}


def score_model_dir(d: Path) -> dict:
    yamls = sorted(d.glob("*.yaml"))
    names = [p.stem for p in yamls]
    cmo_hit = [n for n in names if n in CMO_NAMES or n.startswith("CACHE_")]
    other = [n for n in names if n not in cmo_hit]

    csr_pass = None
    csr_note = ""
    if (d / "csr_address_mapping.NO_PARAMETERS_FOUND.txt").is_file():
        csr_pass = True
        csr_note = "NO_PARAMETERS_FOUND"
    elif (d / "csr_address_mapping.FALSE_POSITIVE.txt").is_file():
        csr_pass = False
        csr_note = "FALSE_POSITIVE marker"
    elif any(n.startswith("CSR_") or n in {"MAX_CSRS", "CSR_ADDRESS_SPACE_SIZE", "CSR_ADDRESS_SPACE_BITS"} for n in names):
        csr_pass = False
        csr_note = f"CSR-like params: {other}"
    elif not yamls and not list(d.glob("*.txt")):
        csr_pass = None
        csr_note = "incomplete dir"
    else:
        # only CMO yamls, no CSR marker — treat CSR as pass if no CSR-named yaml
        csr_pass = not any("CSR" in n or n.startswith("MAX_") for n in names)
        csr_note = "inferred from absence of CSR-named YAML"

    return {
        "model": d.name,
        "cmo_count": len(cmo_hit),
        "cmo_names": cmo_hit,
        "other_params": other,
        "csr_pass": csr_pass,
        "csr_note": csr_note,
        "yaml_count": len(yamls),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-dir", type=Path, default=LIVE)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()

    if not args.live_dir.is_dir():
        print(f"missing {args.live_dir}", file=sys.stderr)
        return 2

    rows = []
    for d in sorted(args.live_dir.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        rows.append(score_model_dir(d))

    print("| Model | CMO # | CSR | Note |")
    print("|-------|------:|-----|------|")
    for r in rows:
        csr = "PASS" if r["csr_pass"] is True else ("FAIL" if r["csr_pass"] is False else "?")
        print(f"| `{r['model']}` | {r['cmo_count']} | {csr} | {r['csr_note'][:40]} |")

    strong = [r for r in rows if r["cmo_count"] >= 3 and r["csr_pass"] is True]
    under = [r for r in rows if r["cmo_count"] < 3]
    csr_fail = [r for r in rows if r["csr_pass"] is False]
    print()
    print(f"models_scored: {len(rows)}")
    print(f"full_cmo_and_csr_pass: {len(strong)} → {[r['model'] for r in strong]}")
    print(f"under_extract_cmo: {len(under)} → {[r['model'] for r in under]}")
    print(f"csr_fail: {len(csr_fail)} → {[r['model'] for r in csr_fail]}")
    print()
    print(
        "Disagreement is a review-routing signal: strong free models agree on "
        "CMO=3+CSR clean; several open-weight/commercial legs under-extract or "
        "false-positive CSR — do not single-model auto-merge."
    )

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({"models": rows}, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
