#!/usr/bin/env python3
# Copyright (c) 2026 Ibteshamul Haque
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""Gate 8: re-derive the GT223 figures by actually re-running the Part I scorer.

Until 2026-08-11 the three GT223 numbers lived in verify_claims.py's UNVERIFIABLE
list, on the belief that the 223-parameter gold "is not committed" and so the
score could not be reproduced. That was half right. The *gold* is not committed,
but everything needed to rebuild it is: the corpus pin carries the 223 parameter
files, and `export_udb_params.py` regenerates the gold from them deterministically.
So the figures are reproducible after all, and this gate proves it rather than
asking to be believed.

What it checks, in order:

  1. Control. Score the committed Part I output against the *unchanged* GT185
     gold and require 72.9% / 88.4% / 129 matched. If the control drifts, the
     pipeline is not deterministic and the GT223 result below would mean nothing.
  2. Regenerate the gold from the pin's spec/std/isa/param and require 223.
  3. Re-score the same output against it and require 64.2% / 88.6% / 138 matched.

The corpus is never written to. Everything runs in a temporary workspace built by
copying the ~6 MB of inputs the two scripts actually read, because a check that
dirties a git tree to prove a number is a check that can leave the tree dirty
when it is interrupted.

Exit codes:  0 pass   1 a figure disagrees   3 cannot run here (skipped)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CORPUS = REPO_ROOT / ".udb-corpus"

# The pin these figures were measured at. A different pin is a different tree
# with a different parameter count, so the expectations below would not apply.
PIN = "c184e3135ea60fe73d6bcec56cef2c3ac09ca18d"

# The Part I run that produced the committed artifact. Note this is
# VALIDATE-claude-v2 and *not* the analyze.py default of claude-sonnet-4 —
# scoring the default input reproduces neither figure.
MODEL = "VALIDATE-claude-v2"

# published in metrics.md §1-2, README.md, EVIDENCE.md, FAQ.md and the essay
GT185_EXPECTED = {
    "total_udb_params": 185,
    "matched_non_debug_count": 129,
    "adjusted_recall_pct": "72.9%",
    "classification_accuracy_pct": "88.4%",
}
GT223_EXPECTED = {
    "total_udb_params": 223,
    "matched_non_debug_count": 138,
    "adjusted_recall_pct": "64.2%",
    "classification_accuracy_pct": "88.6%",
}

# Only what export_udb_params.py and analyze.py actually read.
NEEDED_TREES = [
    Path("spec/std/isa/param"),
    Path("spec/std/isa/csr"),
    Path("param_extraction/scripts"),
    Path("param_extraction/data"),
]
NEEDED_FILES = [Path(f"param_extraction/results/all_results_{MODEL}.json")]


def skip(msg: str) -> None:
    print(f"skip  {msg}")
    sys.exit(3)


def die(msg: str) -> None:
    print(f"FAIL  {msg}")
    sys.exit(1)


def build_workspace(tmp: Path) -> None:
    """Copy the inputs into tmp, preserving the layout both scripts assume.

    export_udb_params.py resolves its repo root as scripts/../../.. and analyze.py
    resolves its project dir as scripts/.., so the nesting has to survive the copy.
    """
    for tree in NEEDED_TREES:
        shutil.copytree(CORPUS / tree, tmp / tree)
    for f in NEEDED_FILES:
        (tmp / f.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(CORPUS / f, tmp / f)


def run(script: Path, *args: str, cwd: Path) -> None:
    # The Part I scorer writes a discrepancies CSV containing U+2265, which dies
    # under the cp1252 default on Windows. verify.sh exports PYTHONUTF8=1 for the
    # same reason; set it here too so the gate behaves the same run directly.
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf8",
        errors="replace",
        env=env,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-6:]
        die(f"{script.name} exited {proc.returncode}\n      " + "\n      ".join(tail))


def read_metrics(tmp: Path) -> dict:
    path = tmp / "param_extraction" / "results" / f"metrics_{MODEL}.json"
    if not path.exists():
        die(f"scorer produced no metrics at {path.name}")
    return json.loads(path.read_text(encoding="utf8"))


def compare(label: str, got: dict, expected: dict) -> bool:
    ok = True
    print(f"  {label}")
    for key, want in expected.items():
        have = got.get(key)
        mark = "ok " if have == want else "BAD"
        if have != want:
            ok = False
        print(f"    {mark} {key:28} expected {want!s:8} got {have!s:8}")
    return ok


def main() -> int:
    if not CORPUS.is_dir():
        skip(".udb-corpus is not present beside this repository")

    head = subprocess.run(
        ["git", "-C", str(CORPUS), "rev-parse", "HEAD"],
        capture_output=True, text=True,
    )
    if head.returncode != 0:
        skip(".udb-corpus is not a git checkout, so its pin cannot be confirmed")
    at = head.stdout.strip()
    if at != PIN:
        skip(f"corpus is at {at[:8]}, these figures were measured at {PIN[:8]}")

    for p in NEEDED_TREES + NEEDED_FILES:
        if not (CORPUS / p).exists():
            skip(f"corpus is missing {p.as_posix()}")

    scorer_args = ["--model", MODEL, "all"]
    with tempfile.TemporaryDirectory(prefix="gt223-") as td:
        tmp = Path(td)
        build_workspace(tmp)
        scripts = tmp / "param_extraction" / "scripts"

        gold = tmp / "param_extraction" / "data" / "ground_truth.json"
        n = len(json.loads(gold.read_text(encoding="utf8"))["parameters"])
        if n != 185:
            skip(f"the corpus gold holds {n} parameters, expected the 185 Part I freeze")

        # 1. Control against the untouched GT185.
        run(scripts / "analyze.py", *scorer_args, cwd=tmp)
        control_ok = compare(
            "control, committed Part I output vs the unchanged GT185 gold",
            read_metrics(tmp), GT185_EXPECTED,
        )
        if not control_ok:
            die("the control drifted, so the pipeline is not reproducing Part I; "
                "the GT223 result below would prove nothing and was not run")

        # 2. Rebuild the gold from the pin's parameter files.
        run(scripts / "export_udb_params.py", cwd=tmp)
        regenerated = len(json.loads(gold.read_text(encoding="utf8"))["parameters"])
        print(f"\n  gold regenerated from {PIN[:8]}: {regenerated} parameters")
        if regenerated != GT223_EXPECTED["total_udb_params"]:
            die(f"regenerated gold holds {regenerated}, expected 223")

        # 3. Same output, larger denominator.
        run(scripts / "analyze.py", *scorer_args, cwd=tmp)
        rescore_ok = compare(
            "\n  same output vs the regenerated GT223 gold",
            read_metrics(tmp), GT223_EXPECTED,
        )

    if not rescore_ok:
        die("a published GT223 figure does not re-derive")

    print("\nok  72.9%/88.4% and 64.2%/88.6% both re-derive from the pin; "
          "223 is a rebuilt count, not a typed one")
    return 0


if __name__ == "__main__":
    sys.exit(main())
