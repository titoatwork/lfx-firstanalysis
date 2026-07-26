#!/usr/bin/env python3
"""
Fail-closed leakage scanner for treatment CSR/field context.

Fails if context (or full prompt) contains:
  - exact gold parameter name
  - normalized gold parameter name (alphanumeric only, case-insensitive)
  - substantial ground-truth YAML content (schema/description body)

Exit 0 = clean; 1 = leakage found; 2 = usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from normalize import name_variants, normalize_param_name, normalize_ws

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "holdout_cases.yaml"


def load_manifest(path: Path = MANIFEST) -> dict[str, Any]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError(f"manifest not a mapping: {path}")
    return doc


def load_gold(path: Path) -> dict[str, Any]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise ValueError(f"gold not a mapping: {path}")
    return doc


def _forbidden_strings(case: dict[str, Any], gold: dict[str, Any]) -> list[tuple[str, str]]:
    """Return list of (label, needle) that must not appear in context."""
    needles: list[tuple[str, str]] = []
    names = [case["name"], *case.get("aliases", [])]
    for n in names:
        for v in name_variants(n):
            if len(v) >= 4:  # avoid ultra-short accidents
                needles.append((f"name:{n}", v))

    # GT body snippets (not the whole file headers)
    for key in ("description", "long_name"):
        val = gold.get(key)
        if isinstance(val, str):
            chunk = normalize_ws(val)
            if len(chunk) >= 40:
                needles.append((f"gold.{key}", chunk[:80]))

    schema = gold.get("schema")
    if isinstance(schema, dict):
        dumped = normalize_ws(yaml.safe_dump(schema, sort_keys=True))
        if len(dumped) >= 20:
            needles.append(("gold.schema", dumped[:60]))

    return needles


def scan_text(text: str, needles: list[tuple[str, str]]) -> list[str]:
    """Scan for forbidden needles using token boundaries only.

    Do **not** concatenate the whole document into alphanumeric form — that
    creates false positives when adjacent words join into a param name
    (e.g. ``mtvec`` + ``MODE`` → ``MTVECMODE``).
    """
    errors: list[str] = []
    plain = text
    plain_ws = normalize_ws(text)
    # Token stream for normalized equality (identifiers only)
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_]*", plain)
    token_norms = {normalize_param_name(t) for t in tokens}

    for label, needle in needles:
        if not needle:
            continue
        # Exact / case-insensitive substring for multi-token / YAML fragments
        if " " in needle or ":" in needle or ("\n" in needle):
            if needle.lower() in plain_ws.lower() or needle in plain:
                errors.append(f"leak {label}: found gold content fragment")
            continue
        if len(needle) > 48 and needle[:40].lower() in plain_ws.lower():
            errors.append(f"leak {label}: found gold content fragment")
            continue
        # Param-name style: word-boundary match on original forms
        pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(needle)}(?![A-Za-z0-9_])", re.I)
        if pat.search(plain):
            errors.append(f"leak {label}: parameter name variant '{needle}'")
            continue
        # Normalized equality against individual identifier tokens only
        n_norm = normalize_param_name(needle)
        if n_norm and len(n_norm) >= 8 and n_norm in token_norms:
            errors.append(f"leak {label}: normalized token '{n_norm}'")
    return errors


def scan_case(case: dict[str, Any], root: Path = ROOT) -> list[str]:
    if case.get("class") == "NEGATIVE" or case.get("expected_params") == 0:
        return []
    gold_path = root / case["gold_path"]
    gold = load_gold(gold_path)
    needles = _forbidden_strings(case, gold)
    errors: list[str] = []

    ctx_ids = case.get("csr_context_ids") or []
    for cid in ctx_ids:
        ctx_path = root / "contexts" / f"{cid}.txt"
        if not ctx_path.is_file():
            errors.append(f"missing context file: {ctx_path.name}")
            continue
        errors.extend(f"{ctx_path.name}: {e}" for e in scan_text(ctx_path.read_text(encoding="utf-8"), needles))

    # Also scan treatment prompt if present
    prompt_path = root / "prompts" / "built" / f"{case['id']}_treatment.txt"
    if prompt_path.is_file():
        errors.extend(
            f"{prompt_path.name}: {e}" for e in scan_text(prompt_path.read_text(encoding="utf-8"), needles)
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--expect-fail", action="store_true", help="Exit 0 only if leakage found")
    parser.add_argument("--fixture", type=Path, help="Scan a single text file against all positive names")
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    all_errors: list[str] = []

    if args.fixture:
        text = args.fixture.read_text(encoding="utf-8")
        for case in manifest["positives"]:
            gold = load_gold(ROOT / case["gold_path"])
            needles = _forbidden_strings(case, gold)
            for e in scan_text(text, needles):
                all_errors.append(f"{case['name']}: {e}")
    else:
        for case in manifest["positives"]:
            for e in scan_case(case):
                all_errors.append(f"{case['id']} {case['name']}: {e}")

    if all_errors:
        print("LEAKAGE DETECTED (fail-closed):")
        for e in all_errors:
            print(f"  - {e}")
        return 0 if args.expect_fail else 1

    print("leak_scan: CLEAN")
    return 1 if args.expect_fail else 0


if __name__ == "__main__":
    # allow running as script without package install
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
