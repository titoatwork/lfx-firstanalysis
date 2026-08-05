"""How much of what the documents publish in bold is actually gated.

verify_claims.py proves that every *registered* number re-derives. It says
nothing about whether a number that got published was ever registered, and the
README used to imply otherwise. That gap is real: auditing it by hand found
"exact-name 48.6% vs 6.2%" carrying the sharpest comparison on the public
surface with no claim behind it, and "44 of 227" republished in bold from an
upstream comment with nothing behind it either.

This reports the gap rather than pretending it is closed. A number counts as
accounted for if it appears among the registered claim values, or in the text of
an UNVERIFIABLE declaration, or is a census figure that check_census.py owns.

The baseline below is a ratchet, not a target. It may fall. It may not rise
without someone deliberately editing this file, which is the point.

  python check_claim_coverage.py           report and enforce the ratchet
  python check_claim_coverage.py --list    print the unaccounted figures only

Exit 0 at or below baseline, 1 above it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "riscv-param-extraction"))

from scripts.verify_claims import CLAIMS, UNVERIFIABLE  # noqa: E402

# Documents whose bold numbers are treated as published claims.
GOVERNED = (
    "README.md",
    "docs/EVIDENCE.md",
    "docs/FAQ.md",
    "riscv-param-extraction/README.md",
    "riscv-param-extraction/docs/metrics.md",
    "riscv-param-extraction/artifact_c/results/PRIMARY_RESULTS.md",
    "riscv-param-extraction/analysis/GOLD-CLASSIFICATION-AUDIT.md",
    "riscv-param-extraction/analysis/PARAM-SCHEMA-SHAPES.md",
)

BOLD_NUMBER = re.compile(r"\*\*(\d+(?:\.\d+)?)\s*%?\*\*")

# check_census.py owns these and compares them across three documents.
CENSUS_OWNED = {"8", "6", "14", "45"}

# Raised only by someone who has read the two paragraphs above.
BASELINE = 0


def accounted_values() -> set[str]:
    """Every number a reader can trace: registered, declared, or census-owned."""
    out: set[str] = set(CENSUS_OWNED)
    for c in CLAIMS:
        for tok in re.findall(r"\d+(?:\.\d+)?", str(c.stated)):
            out.add(tok)
    for _, stated, why in UNVERIFIABLE:
        for tok in re.findall(r"\d+(?:\.\d+)?", f"{stated} {why}"):
            out.add(tok)
    return out


def unaccounted() -> dict[str, list[tuple[str, int]]]:
    known = accounted_values()
    found: dict[str, list[tuple[str, int]]] = {}
    for rel in GOVERNED:
        path = ROOT / rel
        if not path.exists():
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for value in BOLD_NUMBER.findall(line):
                if value not in known:
                    found.setdefault(value, []).append((rel, n))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--list", action="store_true", help="print the figures and stop")
    args = ap.parse_args()

    gaps = unaccounted()
    total = len(gaps)

    print(f"governed documents        {len(GOVERNED)}")
    print(f"accounted-for values      {len(accounted_values())}")
    print(f"bold figures unaccounted  {total}  (baseline {BASELINE})")
    for value in sorted(gaps, key=float):
        where = ", ".join(f"{rel}:{n}" for rel, n in gaps[value][:2])
        print(f"  **{value}**  {where}")

    if args.list:
        return 0

    if total > BASELINE:
        print(f"\nFAIL  {total - BASELINE} more unaccounted figures than the baseline.\n"
              f"      Register it in CLAIMS, declare it in UNVERIFIABLE, or say why\n"
              f"      the baseline should rise.")
        return 1
    if total < BASELINE:
        print(f"\nok  {BASELINE - total} fewer than baseline; lower BASELINE to {total} to hold the gain")
        return 0
    print("\nok  coverage gap unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
