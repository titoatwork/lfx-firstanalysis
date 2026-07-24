#!/usr/bin/env python3
"""Stage v2 merged results where Part I ``analyze.py`` expects them.

``extract.py`` with ``PROMPT_VERSION=v2`` writes::

  param_extraction/results/v2/all_results_<display>.json

``analyze.py`` always reads::

  param_extraction/results/all_results_<display>.json

This helper copies (does not move) the v2 merged file to the root results path
so ``python param_extraction/scripts/analyze.py all --model <display>`` works.

Also can restore GT185 freeze from git for headline metrics comparable to Part I.

Does **not** call APIs. Local UDB tree only.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def stage_merged(udb_root: Path, display: str, prompt_version: str = "v2") -> Path:
    src = udb_root / "param_extraction" / "results" / prompt_version / f"all_results_{display}.json"
    dst = udb_root / "param_extraction" / "results" / f"all_results_{display}.json"
    if not src.is_file():
        raise FileNotFoundError(f"Missing merged results: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def restore_gt185(udb_root: Path) -> None:
    """Checkout committed ground_truth.json from HEAD of current branch.

    On ``lfx-1832`` this is the Part I freeze (185). Fails if git unavailable.
    """
    path = "param_extraction/data/ground_truth.json"
    r = subprocess.run(
        ["git", "checkout", "HEAD", "--", path],
        cwd=udb_root,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"git checkout failed: {r.stderr or r.stdout}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Stage v2 results for analyze.py")
    p.add_argument(
        "--udb-root",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "riscv-unified-db",
    )
    p.add_argument("--model-display", required=True, help="e.g. gpt-4o-mini")
    p.add_argument("--prompt-version", default="v2")
    p.add_argument(
        "--restore-gt185",
        action="store_true",
        help="git checkout HEAD -- ground_truth.json (Part I freeze on lfx-1832)",
    )
    args = p.parse_args(argv)

    udb = args.udb_root.resolve()
    if not udb.is_dir():
        print(f"error: UDB root not found: {udb}", file=sys.stderr)
        return 2

    dst = stage_merged(udb, args.model_display, args.prompt_version)
    print(f"Staged: {dst}")

    if args.restore_gt185:
        restore_gt185(udb)
        print("Restored ground_truth.json from HEAD (expect 185 on lfx-1832)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
