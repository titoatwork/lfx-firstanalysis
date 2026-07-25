#!/usr/bin/env python3
"""Compare naive vs tag-aware quote grounding on raw AsciiDoc cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Reuse validators from validate.py
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import quote_in_source  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "robustness" / "cases"


def main() -> int:
    if not CASES.is_dir():
        print(f"ERROR: missing {CASES}", file=sys.stderr)
        return 2

    rows = []
    for case in sorted(p for p in CASES.iterdir() if p.is_dir()):
        source = (case / "source.raw.adoc").read_text(encoding="utf-8")
        evidence = json.loads((case / "evidence.json").read_text(encoding="utf-8"))
        quote = evidence["quote"]
        naive = quote_in_source(quote, source, "naive")
        tag = quote_in_source(quote, source, "tag-aware")
        rows.append((case.name, naive, tag))
        print(f"| {case.name} | {'pass' if naive else 'FAIL'} | {'pass' if tag else 'FAIL'} |")

    naive_ok = sum(1 for _, n, _ in rows if n)
    tag_ok = sum(1 for _, _, t in rows if t)
    print(f"\nNaive grounding:     {naive_ok}/{len(rows)}")
    print(f"Tag-aware grounding: {tag_ok}/{len(rows)}")

    # Expect tag-aware perfect; naive may fail some
    if tag_ok != len(rows):
        print("ERROR: tag-aware should pass all cases", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
