#!/usr/bin/env python3
"""One-shot local CI gate (same checks as GitHub Actions)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]  # LFX-Mentorship or monorepo root depending on layout
# challenge is at riscv-param-extraction/challenge → package root is parent
PKG = ROOT.parent


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd or ROOT))


def main() -> int:
    py = sys.executable
    validate = ROOT / "scripts" / "validate.py"

    # Good results must pass
    run([py, str(validate), "--results", str(ROOT / "results" / "curated"), "--grounding", "naive"])

    # Bad fixtures must fail (expect-fail)
    run(
        [
            py,
            str(validate),
            "--results",
            str(ROOT / "tests" / "bad_examples"),
            "--grounding",
            "naive",
            "--expect-fail",
        ]
    )

    run([py, str(ROOT / "scripts" / "check_negatives.py")])
    run([py, str(ROOT / "scripts" / "check_grounding_modes.py")])
    run([py, str(ROOT / "scripts" / "score_strategies.py")])
    run([py, str(ROOT / "benchmark" / "scripts" / "score_recall.py")])
    # Offline re-score of committed live multi-model dirs (no API)
    if (ROOT / "results" / "live").is_dir():
        run([py, str(ROOT / "scripts" / "score_live_matrix.py")])
        # Unified offline score surface (writes DISAGREEMENT.md)
        run([py, str(ROOT / "scripts" / "score.py")])

    # Temporal holdout pilot (offline: unit tests + fail-closed leakage)
    holdout = ROOT / "temporal_holdout"
    run([py, str(holdout / "tests" / "test_holdout.py"), "-v"])
    run([py, str(holdout / "scripts" / "leak_scan.py")])

    # Export unit tests at package level
    run([py, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=PKG)

    print("\nci_check: ALL PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"\nci_check: FAILED ({exc.returncode})", file=sys.stderr)
        raise SystemExit(exc.returncode)
