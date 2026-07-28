#!/usr/bin/env python3
"""Split each arm's adjusted recall into the match types that produced it.

analyze.py credits a gold parameter through one of seven passes: an exact name
match, or one of six inexact ones (one_to_many, explicit_group, concept_group,
stem, fuzzy_name) with "none" meaning unmatched. Only the totals reach
metrics_arm_*.json, so the composition of a score is invisible there. Two runs
can report the same adjusted recall while crediting entirely different passes.

This re-scores committed arms and keeps the alignment breakdown, which
analyze.py writes beside the metrics and overwrites on every call. No model is
called; scoring is deterministic, so this reproduces exactly from the
repository with no API key.

  python scripts/decompose_matches.py                 # every committed arm
  python scripts/decompose_matches.py --json out.json # machine-readable

Note on `exact_matches_evaluated` in metrics_arm_*.json: that field counts
exact matches *that also carried a comparable class* (analyze.py:510), so it is
a lower bound on exact matches, not the count of them. The numbers here come
from the alignment file's own by_type tally and are the ones to cite.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from score_arms import CORPUS, assemble, chunk_metas, load_analyze

AC = Path(__file__).resolve().parents[1]
RUNS = AC / "runs"

EXACT = "exact"
INEXACT = ("one_to_many", "explicit_group", "concept_group", "stem", "fuzzy_name")


def alignment_for(arm_dir: Path, tag: str, metas: dict) -> dict:
    """Score one arm and return the alignment file analyze.py wrote."""
    analyze = load_analyze()
    rd = CORPUS / "results"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / f"all_results_{tag}.json").write_text(
        json.dumps(assemble(arm_dir, tag, metas)), encoding="utf-8"
    )
    analyze.run_all(tag)
    return json.loads((rd / f"alignment_{tag}.json").read_text(encoding="utf-8"))


def decompose(align: dict) -> dict:
    by = align.get("by_type", {})
    exact = by.get(EXACT, 0)
    inexact = sum(by.get(k, 0) for k in INEXACT)
    matched = exact + inexact
    return {
        "by_type": by,
        "exact": exact,
        "inexact": inexact,
        "matched": matched,
        "inexact_share": (inexact / matched) if matched else 0.0,
    }


def discover(min_chunks: int) -> tuple[list, list]:
    """Return (complete, partial). Partial arms are reported, never dropped silently."""
    complete, partial = [], []
    for run in sorted(RUNS.iterdir()):
        for arm_dir in sorted(run.glob("arm_*")):
            n = len(list((arm_dir / "parsed").glob("chunk_*.json"))) \
                if (arm_dir / "parsed").is_dir() else 0
            if n == 0:
                continue
            (complete if n >= min_chunks else partial).append(
                (run.name, arm_dir.name[-1], arm_dir, n)
            )
    return complete, partial


def cross_check(run_name: str, arm: str, align_matched: int) -> tuple[int | None, str]:
    """Return the authoritative gold-side match count and how the alignment sum compares.

    The alignment file lists one entry per LLM parameter, so when several LLM
    parameters land on the same gold parameter its sum exceeds the gold-side
    matched_udb_count that adjusted recall is built from. The two agree on every
    arm here, but they are not the same quantity and the metrics count wins.
    """
    p = RUNS / run_name / f"metrics_arm_{arm}.json"
    if not p.exists():
        return None, "no-metrics"
    want = json.loads(p.read_text(encoding="utf-8"))["matched_udb_count"]
    return want, "ok" if want == align_matched else f"align={align_matched}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, help="write the full breakdown here")
    ap.add_argument("--gold-total", type=int, default=177,
                    help="gold parameter denominator used by analyze.py")
    ap.add_argument("--min-chunks", type=int, default=60,
                    help="an arm below this is a fragment and is excluded from the table")
    args = ap.parse_args()

    metas = chunk_metas()
    complete, partial = discover(args.min_chunks)
    rows = []
    for run_name, arm, arm_dir, n in complete:
        tag = f"ac_{run_name[:15]}_{arm}"
        d = decompose(alignment_for(arm_dir, tag, metas))
        gold_matched, note = cross_check(run_name, arm, d["matched"])
        if gold_matched is not None:
            d["align_matched"] = d["matched"]
            d["matched"] = gold_matched
            d["inexact"] = gold_matched - d["exact"]
            d["inexact_share"] = d["inexact"] / gold_matched if gold_matched else 0.0
        d.update(run=run_name, arm=arm, chunks=n, cross_check=note)
        rows.append(d)

    if not rows:
        print("no complete arms found under runs/", file=sys.stderr)
        return 1

    hdr = f"{'arm':<4}{'run':<10}{'matched':>8}{'exact':>7}{'inexact':>9}"
    print(hdr + f"{'exact-only%':>13}{'reported%':>11}{'inexact share':>15}{'  check'}")
    for r in rows:
        eo = 100 * r["exact"] / args.gold_total
        rep = 100 * r["matched"] / args.gold_total
        print(f"{r['arm']:<4}{r['run'][9:15]:<10}{r['matched']:>8}{r['exact']:>7}"
              f"{r['inexact']:>9}{eo:>13.1f}{rep:>11.1f}"
              f"{100*r['inexact_share']:>14.1f}%  {r['cross_check']}")

    if any(r["cross_check"] == "no-metrics" for r in rows):
        print("\nsome arms have no committed metrics; their counts are alignment-side",
              file=sys.stderr)

    ex = [r["exact"] for r in rows]
    ix = [r["inexact"] for r in rows]
    sh = [100 * r["inexact_share"] for r in rows]
    print(f"\nexact matches    spread {max(ex) - min(ex):>3}   ({min(ex)}-{max(ex)})")
    print(f"inexact matches  spread {max(ix) - min(ix):>3}   ({min(ix)}-{max(ix)})")
    print(f"inexact share of credit: {min(sh):.1f}% - {max(sh):.1f}%")

    if partial:
        print(f"\nexcluded as fragments (fewer than {args.min_chunks} chunks scored):")
        for run_name, arm, _, n in partial:
            print(f"  {run_name}  arm {arm}  {n}/{args.min_chunks} chunks")

    if args.json:
        args.json.write_text(json.dumps({
            "gold_total": args.gold_total,
            "min_chunks": args.min_chunks,
            "rows": rows,
            "excluded_fragments": [
                {"run": r, "arm": a, "chunks": n} for r, a, _, n in partial
            ],
        }, indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
