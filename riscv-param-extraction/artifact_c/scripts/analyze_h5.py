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
  2  absent because UDB derives it               (IDL function or global, or follows
                                                  from which extension is implemented)
  3  absent because it is out of scope           (microarchitectural / execution environment)

Evidence type is pin-dependent and is recorded with the commit it was determined
against. `.udb-corpus` is a fork, not `main`, and a derivation can be `documented`
at the pin while being `executable` upstream. See the 2026-08-05 amendment.

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
    """Mechanical signals used for blind labelling: existing params, and the IDL.

    The IDL text is `globals.isa` **plus every file it includes**. Reading
    `globals.isa` alone was the original bug: `FLEN` is defined in `fp.idl`,
    which `globals.isa:10` includes, so a globals-only read reported no
    derivation and the absence was read as evidence. See the 2026-08-05
    amendment in ../PREREGISTRATION.md.
    """
    params = set()
    pdir = CORPUS / "spec" / "std" / "isa" / "param"
    if pdir.exists():
        params = {p.stem for p in pdir.glob("*.yaml")}

    isa_dir = CORPUS / "spec" / "std" / "isa" / "isa"
    g = isa_dir / "globals.isa"
    if not g.exists():
        return params, ""

    parts = [g.read_text(encoding="utf-8", errors="replace")]
    for inc in re.findall(r'^\s*include\s+"([^"]+)"', parts[0], re.M):
        f = isa_dir / inc
        if f.exists():
            parts.append(f.read_text(encoding="utf-8", errors="replace"))
    return params, "\n".join(parts)


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


def strip_idl_comments(src: str) -> str:
    """Drop `#` comments. Required, not cosmetic: at corpus pin c184e313
    `fp.idl:12` is `U32 FLEN = 64; # implemented?(...)`, so a config-dependence
    test that reads comments would call a hard-coded constant a derivation."""
    return re.sub(r"#[^\n]*", "", src)


CONFIG_DEPENDENT = ("implemented?(", "CSR[", "ExtensionName::")


def idl_derivation(name: str, idl_src: str) -> str | None:
    """Return how IDL derives `name`, or None. Executable evidence only.

      "function"  `function ialign { ... return 16 ... return 32 }`
      "global"    `U32 FLEN = implemented?(ExtensionName::Q) ? 128 : ...;`
      "constant"  `U32 FLEN = 64;` — a declaration, NOT a derivation
      None        no declaration of any form

    Three distinctions matter here and each one was got wrong at some point:
    a derivation can be a global rather than a function; it can live in any of
    the files `globals.isa` includes rather than in `globals.isa`; and a global
    bound to a literal is a fixed value, not something derived from config.
    Only "function" and "global" are executable evidence. "constant" and None
    go to a human, who records `documented` or `absent`.
    """
    src = strip_idl_comments(idl_src)
    if re.search(r"function\s+" + re.escape(name.lower()) + r"\s*\{", src):
        return "function"
    # <Type> NAME = <init>; where <Type> may carry a width, e.g. Bits<32>.
    m = re.search(r"^[ \t]*[A-Za-z_][A-Za-z0-9_]*(?:<[^>\n]*>)?[ \t]+"
                  + re.escape(name) + r"[ \t]*=([^;]*);", src, re.M)
    if not m:
        return None
    init = m.group(1)
    return "global" if any(t in init for t in CONFIG_DEPENDENT) else "constant"


def label_signals(name: str, existing: set[str], idl_src: str) -> dict:
    """Mechanical signals only. No judgement, no arm, no model.

    Evidence type is recorded alongside the category because two category-2
    labels are not equally strong. An executable derivation can be found
    automatically across the repository; prose stating a derivation cannot.
    Collapsing them would hide that difference. (@RAJVEER42)
    """
    form = idl_derivation(name, idl_src)
    if name in existing:
        return {"has_param_file": True, "idl_derivation": form,
                "auto_category": "not-a-candidate", "evidence_type": "n/a"}
    if form in ("function", "global"):
        return {"has_param_file": False, "idl_derivation": form,
                "auto_category": 2, "evidence_type": "executable"}
    # "constant" and None both fall here. A literal-valued global is a fixed
    # value, not a derivation, and prose-level derivation cannot be detected
    # mechanically at all; a human decides and records documented or absent.
    return {"has_param_file": False, "idl_derivation": form,
            "auto_category": "", "evidence_type": "TODO-human"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", type=Path, required=True)
    args = ap.parse_args()

    gold = gold_names()
    existing, idl_src = udb_signals()
    if not idl_src:
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
        row.update(label_signals(n, existing, idl_src))
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
