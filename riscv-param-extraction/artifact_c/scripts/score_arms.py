#!/usr/bin/env python3
"""
Score Artifact C arms with the Part I corpus's own analyze.py, unmodified.

The scorer must not be a reimplementation. If arm A is to be a control against
the published figures, the same code that produced those figures has to produce
these. So this assembles each arm's outputs into the merged-results shape
analyze.py already consumes, then calls it.

Validate first, spend later:

  python score_arms.py --validate
      Scores the committed Claude v2 results and checks the output against the
      published numbers (72.9 adj, 88.4 class, 12/24 WARL). Costs nothing. If
      this fails, nothing else here is trustworthy.

  python score_arms.py --run-dir ../runs/<id> --arm A
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

AC = Path(__file__).resolve().parents[1]
CORPUS = AC.parents[1] / ".udb-corpus" / "param_extraction"

PUBLISHED = {
    "adjusted_recall": 72.9,
    "classification_accuracy": 88.4,
    "warl": (12, 24),
    "direct": (83, 100),
    "csr_rw": (32, 51),
}


def load_analyze():
    sys.path.insert(0, str(CORPUS / "scripts"))
    import analyze  # noqa: E402
    return analyze


def assemble(arm_dir: Path, tag: str, metas: dict) -> dict:
    """Build the merged-results structure analyze.py expects."""
    results = []
    n_params = 0
    for pf in sorted((arm_dir / "parsed").glob("chunk_*.json")):
        d = json.loads(pf.read_text(encoding="utf-8"))
        cid = d["chunk_id"]
        raw = arm_dir / "raw" / f"{cid}.txt"
        m = metas.get(cid, {})
        params = d.get("parameters") or []
        n_params += len(params)
        results.append({
            "chunk_id": cid,
            "source_file": m.get("source_file", ""),
            "start_line": m.get("start_line", 0),
            "end_line": m.get("end_line", 0),
            "content_start_line": m.get("content_start_line", 0),
            "model": tag,
            "parameters": params,
            "skipped_non_parameters": [],
            "raw_response": raw.read_text(encoding="utf-8") if raw.exists() else "",
            "input_tokens": 0,
            "output_tokens": 0,
            "latency_ms": 0,
            "timestamp": "",
            "error": None,
            "retry_count": 0,
        })
    return {
        "model": tag,
        "total_chunks": len(results),
        "total_parameters": n_params,
        "total_skipped": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "errors": 0,
        "results": results,
    }


def chunk_metas() -> dict:
    out = {}
    for f in sorted((CORPUS / "results" / "v2" / "claude-sonnet-4").glob("chunk_*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        out[d["chunk_id"]] = {k: d.get(k) for k in
                              ("source_file", "start_line", "end_line", "content_start_line")}
    return out


def score(tag: str, merged: dict) -> dict:
    analyze = load_analyze()
    rd = CORPUS / "results"
    rd.mkdir(parents=True, exist_ok=True)
    (rd / f"all_results_{tag}.json").write_text(json.dumps(merged), encoding="utf-8")
    analyze.run_all(tag)
    return json.loads((rd / f"metrics_{tag}.json").read_text(encoding="utf-8"))


def _near(got: float | None, want: float, tol: float = 0.06) -> bool:
    return got is not None and abs(got - want) <= tol


def pct(m: dict, key: str) -> float | None:
    """analyze.py emits fractions plus a *_pct string. Return a float percentage."""
    if f"{key}_pct" in m:
        return float(str(m[f"{key}_pct"]).rstrip("%"))
    if key in m and m[key] is not None:
        return float(m[key]) * 100.0
    return None


def class_counts(m: dict, cls: str) -> tuple[int, int] | None:
    v = (m.get("per_class_recall") or {}).get(cls)
    if isinstance(v, dict):
        for a, b in (("found", "total"), ("matched", "total"), ("n", "total")):
            if a in v and b in v:
                return int(v[a]), int(v[b])
    return None


def show(m: dict, label: str) -> None:
    print(f"\n=== {label} ===")
    for k in ("adjusted_recall", "classification_accuracy"):
        p = pct(m, k)
        if p is not None:
            print(f"  {k:<26} {p:.1f}%")
    for cls in sorted(m.get("per_class_recall") or {}):
        c = class_counts(m, cls)
        v = (m["per_class_recall"])[cls]
        print(f"  {cls:<26} {f'{c[0]}/{c[1]}' if c else v}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true",
                    help="score the committed Claude v2 results against published figures")
    ap.add_argument("--run-dir", type=Path)
    ap.add_argument("--arm")
    args = ap.parse_args()

    if args.validate:
        src = CORPUS / "results" / "v2" / "all_results_claude-sonnet-4.json"
        if not src.exists():
            print(f"missing {src}", file=sys.stderr)
            return 2
        merged = json.loads(src.read_text(encoding="utf-8"))
        tag = "VALIDATE-claude-v2"
        merged["model"] = tag
        m = score(tag, merged)
        show(m, "harness validation against committed Claude v2")

        checks = {
            "adjusted_recall 72.9%": _near(pct(m, "adjusted_recall"), PUBLISHED["adjusted_recall"]),
            "classification 88.4%": _near(pct(m, "classification_accuracy"),
                                          PUBLISHED["classification_accuracy"]),
            "WARL 12/24": class_counts(m, "NORM_CSR_WARL") == PUBLISHED["warl"],
            "DIRECT 83/100": class_counts(m, "NORM_DIRECT") == PUBLISHED["direct"],
            "CSR_RW 32/51": class_counts(m, "NORM_CSR_RW") == PUBLISHED["csr_rw"],
        }
        print("\n  against docs/metrics.md:")
        for k, v in checks.items():
            print(f"    {'PASS' if v else 'FAIL'}  {k}")
        ok = all(checks.values())
        print(f"\n  HARNESS REPRODUCES PUBLISHED FIGURES: {ok}")
        return 0 if ok else 1

    if not args.run_dir or not args.arm:
        print("need --run-dir and --arm, or --validate", file=sys.stderr)
        return 2

    arm_dir = args.run_dir.resolve() / f"arm_{args.arm}"
    if not arm_dir.exists():
        print(f"missing {arm_dir}", file=sys.stderr)
        return 2
    tag = f"AC-{args.run_dir.name}-arm{args.arm}"
    merged = assemble(arm_dir, tag, chunk_metas())
    m = score(tag, merged)
    show(m, f"arm {args.arm}")
    out = args.run_dir.resolve() / f"metrics_arm_{args.arm}.json"
    out.write_text(json.dumps(m, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
