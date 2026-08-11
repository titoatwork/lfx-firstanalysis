#!/usr/bin/env python3
"""Assert hard-negative cases declare zero parameters."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "negative_controls" / "cases"


def main() -> int:
    if not CASES.is_dir():
        print(f"ERROR: missing {CASES}", file=sys.stderr)
        return 2

    failures = 0
    case_dirs = sorted(p for p in CASES.iterdir() if p.is_dir())
    if not case_dirs:
        print("ERROR: no negative control cases", file=sys.stderr)
        return 2

    for case in case_dirs:
        result = case / "result.json"
        source = case / "source.txt"
        if not result.is_file() or not source.is_file():
            print(f"[FAIL] {case.name}: need source.txt + result.json")
            failures += 1
            continue
        data = json.loads(result.read_text(encoding="utf-8"))
        params = data.get("parameters", None)
        if params != []:
            print(f"[FAIL] {case.name}: expected parameters=[], got {params!r}")
            failures += 1
            continue
        print(f"[PASS (correctly zero)] {case.name}")

    print(f"\n{len(case_dirs)} case(s) checked, {failures} failure(s)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
