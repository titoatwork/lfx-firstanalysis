#!/usr/bin/env python3
"""
Diff two runs of the same arm at the level of individual parameters.

This is the audit that could not be done on the published Artifact A number,
because its per-chunk outputs were not retained. Given two runs of the same arm
and model it answers: which specific gold parameters did one run find that the
other missed, and in which chunk did they diverge.

Run-to-run variance at temperature 0 is real on hosted models. The question is
whether it is small enough that a single run's per-class figures mean anything.

Usage:
  python compare_runs.py --a ../runs/<id1> --b ../runs/<id2> --arm A
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

AC = Path(__file__).resolve().parents[1]
CORPUS = AC.parents[1] / ".udb-corpus" / "param_extraction"
DEBUG = ("DBG_", "DCSR_", "TRIGGER_", "TDATA_", "MCONTEXT_", "HCONTEXT_", "SCONTEXT_")


def gold() -> dict[str, str]:
    gt = json.loads((CORPUS / "data" / "ground_truth.json").read_text(encoding="utf-8"))
    return {p["name"]: p["classification"] for p in gt["parameters"]
            if not p["name"].startswith(DEBUG)}


def candidates(run: Path, arm: str) -> dict[str, set[str]]:
    """chunk_id -> set of names the model claimed (parameter_name or existing_udb_name)."""
    out: dict[str, set[str]] = defaultdict(set)
    for pf in sorted((run / f"arm_{arm}" / "parsed").glob("chunk_*.json")):
        d = json.loads(pf.read_text(encoding="utf-8"))
        for p in d.get("parameters") or []:
            for key in ("existing_udb_name", "parameter_name"):
                v = (p.get(key) or "").strip()
                if v:
                    out[d["chunk_id"]].add(v)
    return out


def flat(c: dict[str, set[str]]) -> set[str]:
    s: set[str] = set()
    for v in c.values():
        s |= v
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=Path, required=True)
    ap.add_argument("--b", type=Path, required=True)
    ap.add_argument("--arm", default="A")
    args = ap.parse_args()

    g = gold()
    ca, cb = candidates(args.a.resolve(), args.arm), candidates(args.b.resolve(), args.arm)
    fa, fb = flat(ca), flat(cb)

    hit_a = {n for n in fa if n in g}
    hit_b = {n for n in fb if n in g}

    print(f"arm {args.arm}")
    print(f"  run A: {args.a.name}")
    print(f"  run B: {args.b.name}")
    print(f"\n  distinct names claimed : {len(fa)} vs {len(fb)}")
    print(f"  gold parameters hit    : {len(hit_a)} vs {len(hit_b)}")
    print(f"  hit by both            : {len(hit_a & hit_b)}")
    print(f"  only run A             : {len(hit_a - hit_b)}")
    print(f"  only run B             : {len(hit_b - hit_a)}")

    denom = len(hit_a | hit_b)
    stable = len(hit_a & hit_b) / denom * 100 if denom else 0.0
    print(f"\n  stability: {stable:.1f}% of gold hits appear in both runs")

    for label, s in (("only in run A", hit_a - hit_b), ("only in run B", hit_b - hit_a)):
        if not s:
            continue
        print(f"\n  {label}:")
        by_cls = defaultdict(list)
        for n in sorted(s):
            by_cls[g[n]].append(n)
        for cls in sorted(by_cls):
            print(f"    {cls}: {', '.join(by_cls[cls])}")

    out = AC / "analysis" / f"variance_arm{args.arm}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "arm": args.arm,
        "run_a": args.a.name,
        "run_b": args.b.name,
        "gold_hits_a": sorted(hit_a),
        "gold_hits_b": sorted(hit_b),
        "both": sorted(hit_a & hit_b),
        "only_a": sorted(hit_a - hit_b),
        "only_b": sorted(hit_b - hit_a),
        "stability_pct": round(stable, 1),
    }, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
