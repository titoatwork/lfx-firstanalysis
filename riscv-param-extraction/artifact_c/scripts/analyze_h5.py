#!/usr/bin/env python3
"""
H5 analysis: does dual-model agreement select for candidates a reviewer least needs?

Registered in ../PREREGISTRATION.md. Two rules from that file are enforced here
rather than left to good intentions:

1. **Agreement is computed WITHIN an arm, then pooled with the arm recorded.**
   Arms A and C hand both models the gold catalogue, so agreement there is partly
   agreement on a supplied list. Merging arms before computing agreement would let
   H0 leak into H5 invisibly. (@RAJVEER42 raised this; the analysis would have been
   wrong without it.)

2. **Rubric labelling is blind.** The worksheet this emits carries the candidate
   name and mechanical UDB signals only. It does not carry the arm, the model, or
   whether the candidate was agreed or exclusive. The key that maps names back to
   arms is written separately and is not needed to label.

Categories, from the preregistration:
  1  absent from UDB and arguably should exist   (a real gap)
  2  absent because UDB derives it               (function, or follows from an extension)
  3  absent because it is out of scope           (microarchitectural / execution environment)

Only category 1 is a genuine missed parameter.

Usage:
  python analyze_h5.py --runs ../runs/<id> [../runs/<id2> ...]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

AC = Path(__file__).resolve().parents[1]
CORPUS = AC.parents[1] / ".udb-corpus"
UDB_MAIN = AC.parents[1] / "riscv-unified-db"


def gold_names() -> set[str]:
    gt = json.loads((CORPUS / "param_extraction" / "data" / "ground_truth.json")
                    .read_text(encoding="utf-8"))
    return {p["name"] for p in gt["parameters"]}


def udb_signals() -> tuple[set[str], str]:
    """Mechanical signals used for blind labelling: existing params, and globals.isa."""
    params = set()
    pdir = CORPUS / "spec" / "std" / "isa" / "param"
    if pdir.exists():
        params = {p.stem for p in pdir.glob("*.yaml")}
    g = CORPUS / "spec" / "std" / "isa" / "isa" / "globals.isa"
    globals_src = g.read_text(encoding="utf-8", errors="replace") if g.exists() else ""
    return params, globals_src


def collect(run_dirs: list[Path]) -> dict[tuple[str, str], dict[str, dict]]:
    """(arm, model) -> {candidate_name: record}."""
    out: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for rd in run_dirs:
        man = rd / "RUN_MANIFEST.json"
        model = json.loads(man.read_text(encoding="utf-8"))["model"] if man.exists() else rd.name
        for arm_dir in sorted(rd.glob("arm_*")):
            arm = arm_dir.name.split("_", 1)[1]
            for pf in sorted((arm_dir / "parsed").glob("chunk_*.json")):
                d = json.loads(pf.read_text(encoding="utf-8"))
                for p in d.get("parameters") or []:
                    name = (p.get("parameter_name") or "").strip()
                    if not name:
                        continue
                    prev = out[(arm, model)].get(name)
                    rec = {
                        "name": name,
                        "chunk": d["chunk_id"],
                        "confidence": p.get("confidence", ""),
                        "class": p.get("class", ""),
                        "existing_udb_name": p.get("existing_udb_name") or "",
                    }
                    # keep the highest-confidence sighting
                    if prev is None or (prev["confidence"] != "high" and rec["confidence"] == "high"):
                        out[(arm, model)][name] = rec
    return out


def proposed_new(recs: dict[str, dict], gold: set[str], existing: set[str]) -> set[str]:
    """High-confidence candidates with no gold and no trusted existing-name hit."""
    out = set()
    for n, r in recs.items():
        if r["confidence"] != "high":
            continue
        if n in gold or n in existing:
            continue
        if r["existing_udb_name"]:
            continue
        out.add(n)
    return out


def label_signals(name: str, existing: set[str], globals_src: str) -> dict:
    """Mechanical signals only. No judgement, no arm, no model.

    Evidence type is recorded alongside the category because two category-2
    labels are not equally strong. A derivation function is executable and can be
    found automatically across the repository; prose stating a derivation cannot.
    Collapsing them would hide that difference. (@RAJVEER42)
    """
    fn = re.search(r"function\s+" + re.escape(name.lower()) + r"\s*\{", globals_src)
    if name in existing:
        return {"has_param_file": True, "derived_by_function_in_globals_isa": bool(fn),
                "auto_category": "not-a-candidate", "evidence_type": "n/a"}
    if fn:
        return {"has_param_file": False, "derived_by_function_in_globals_isa": True,
                "auto_category": 2, "evidence_type": "executable"}
    # Prose-level derivation cannot be detected mechanically; a human decides,
    # and records evidence_type as documented or absent when they do.
    return {"has_param_file": False, "derived_by_function_in_globals_isa": False,
            "auto_category": "", "evidence_type": "TODO-human"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", type=Path, required=True)
    args = ap.parse_args()

    gold = gold_names()
    existing, globals_src = udb_signals()
    if not globals_src:
        print("warning: globals.isa not found, category-2 auto-detection disabled",
              file=sys.stderr)

    by_key = collect([r.resolve() for r in args.runs])
    if not by_key:
        print("no parsed candidates found", file=sys.stderr)
        return 2

    arms = sorted({a for a, _ in by_key})
    models_per_arm = {a: sorted({m for aa, m in by_key if aa == a}) for a in arms}

    print("collected")
    for a in arms:
        for m in models_per_arm[a]:
            n = len(by_key[(a, m)])
            pn = len(proposed_new(by_key[(a, m)], gold, existing))
            print(f"  arm {a}  {m:<28} {n:>4} candidates, {pn:>4} high-conf proposed-new")

    # ---- within-arm agreement, never across arms ----
    agreed: dict[str, set[str]] = {}
    exclusive: dict[str, dict[str, set[str]]] = {}
    for a in arms:
        ms = models_per_arm[a]
        sets = {m: proposed_new(by_key[(a, m)], gold, existing) for m in ms}
        if len(ms) < 2:
            print(f"\narm {a}: only {len(ms)} model, agreement undefined. "
                  f"H5 needs a second model in the same arm.")
            agreed[a] = set()
            exclusive[a] = {m: sets[m] for m in ms}
            continue
        inter = set.intersection(*sets.values())
        agreed[a] = inter
        exclusive[a] = {m: sets[m] - inter for m in ms}
        print(f"\narm {a}: agreed {len(inter)}, " +
              ", ".join(f"{m} only {len(exclusive[a][m])}" for m in ms))

    # ---- blind labelling worksheet ----
    every: set[str] = set()
    for a in arms:
        every |= agreed[a]
        for s in exclusive[a].values():
            every |= s

    worksheet = []
    for n in sorted(every):
        row = {"candidate": n}
        row.update(label_signals(n, existing, globals_src))
        row["category"] = row.pop("auto_category")
        row["labelled_by"] = "auto" if row["category"] else "TODO-human"
        worksheet.append(row)

    out_dir = AC / "analysis"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "H5_BLIND_WORKSHEET.json").write_text(
        json.dumps({
            "note": "Blind by construction. No arm, model, or agreed/exclusive status. "
                    "Label each TODO-human row as 1, 2 or 3 per PREREGISTRATION H5.",
            "categories": {"1": "real gap", "2": "UDB derives it", "3": "out of scope"},
            "rows": worksheet,
        }, indent=2), encoding="utf-8")

    # the key is separate, and is not needed to label
    (out_dir / "H5_KEY.json").write_text(
        json.dumps({
            "within_arm_agreement": True,
            "arms": {a: {"agreed": sorted(agreed[a]),
                         "exclusive": {m: sorted(s) for m, s in exclusive[a].items()}}
                     for a in arms},
        }, indent=2), encoding="utf-8")

    auto = sum(1 for r in worksheet if r["labelled_by"] == "auto")
    print(f"\nworksheet: {len(worksheet)} distinct candidates, {auto} auto-labelled, "
          f"{len(worksheet)-auto} need a human category")
    print(f"  {out_dir / 'H5_BLIND_WORKSHEET.json'}")
    print(f"  {out_dir / 'H5_KEY.json'}  (do not open before labelling)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
