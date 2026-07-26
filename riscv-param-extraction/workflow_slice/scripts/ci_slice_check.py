#!/usr/bin/env python3
"""
One-command reproduction for the workflow_slice package.

  python workflow_slice/scripts/ci_slice_check.py

Runs:
  1. eval_2097 adversarial pack validator
  2. vertical_5pct slice validator

No paid API. Exit 0 only if both green.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[2]
EVAL = PKG / "workflow_slice" / "eval_2097" / "scripts" / "validate_eval_pack.py"
SLICE = PKG / "workflow_slice" / "vertical_5pct" / "scripts" / "validate_slice.py"


def run(script: Path) -> int:
    print(f"\n=== {script.relative_to(PKG)} ===")
    env = dict(**__import__("os").environ)
    # RefResolver deprecation noise is not a pack failure.
    env.setdefault("PYTHONWARNINGS", "ignore::DeprecationWarning")
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(PKG),
        check=False,
        env=env,
    )
    return proc.returncode


def main() -> int:
    missing = [p for p in (EVAL, SLICE) if not p.is_file()]
    if missing:
        print("ci_slice_check FAILED: missing scripts:")
        for p in missing:
            print(f"  - {p}")
        return 1

    rc = 0
    rc |= run(EVAL)
    rc |= run(SLICE)

    print("\n=== summary ===")
    if rc == 0:
        print("workflow_slice CI GREEN")
        print("  - eval_2097 pack OK")
        print("  - vertical_5pct OK")
        print("  - no model API used")
    else:
        print("workflow_slice CI RED")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
