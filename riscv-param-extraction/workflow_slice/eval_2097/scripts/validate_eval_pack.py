#!/usr/bin/env python3
"""
Validate frozen eval pack for upstream skill PR #2097.

Does not execute the remote skill with an LLM. Checks that:
  - every case has source + expected contract
  - positive golds carry excerpts in source text
  - negatives contain risk keywords where relevant
  - structural critiques are recorded in MANIFEST
  - example skill-shaped wrapper is NOT UDB-valid
  - clean UDB param YAML from positives validates against param_schema

Exit 0 = pack intact.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parents[3]  # riscv-param-extraction
SCHEMA_DIR = PKG / "challenge" / "schema"
MANIFEST = ROOT / "MANIFEST.yaml"


def load_schema_validator():
    from jsonschema import Draft7Validator
    from jsonschema.validators import RefResolver

    store = {}
    for path in SCHEMA_DIR.glob("*.json"):
        doc = __import__("json").loads(path.read_text(encoding="utf-8"))
        store[path.name] = doc
        store[f"{path.name}#"] = doc
    schema = __import__("json").loads((SCHEMA_DIR / "param_schema.json").read_text(encoding="utf-8"))
    resolver = RefResolver.from_schema(schema, store=store)
    return Draft7Validator(schema, resolver=resolver)


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    errors: list[str] = []
    man = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    validator = load_schema_validator()

    # structural critiques present
    critiques = man.get("skill_structural_critiques") or []
    if len(critiques) < 4:
        errors.append(f"expected >=4 structural critiques, got {len(critiques)}")

    for case in man.get("positives") or []:
        cdir = ROOT / case["path"]
        src = cdir / "source.txt"
        exp = cdir / "expected.yaml"
        gold = cdir / "gold.yaml"
        if not src.is_file():
            errors.append(f"{case['id']}: missing source.txt")
            continue
        if not exp.is_file():
            errors.append(f"{case['id']}: missing expected.yaml")
            continue
        text = src.read_text(encoding="utf-8")
        if len(text) < 40:
            errors.append(f"{case['id']}: source too short")
        exp_doc = yaml.safe_load(exp.read_text(encoding="utf-8"))
        if not exp_doc.get("expect_extract"):
            errors.append(f"{case['id']}: positive must expect_extract")
        if gold.is_file():
            g = yaml.safe_load(gold.read_text(encoding="utf-8"))
            # build minimal UDB-shaped check object from gold if incomplete
            if isinstance(g, dict) and g.get("name"):
                # curated golds are full UDB docs; temporal golds may be partial
                if g.get("$schema") and g.get("kind") == "parameter":
                    errs = sorted(validator.iter_errors(g), key=lambda e: list(e.path))
                    if errs:
                        errors.append(f"{case['id']}: gold fails UDB schema: {errs[0].message}")
                # excerpt presence: gold description or source must contain signal words
                signal = (exp_doc.get("skill_signal") or "").split()[0:1]
                if signal and signal[0].lower() not in text.lower() and "WARL" not in text and "implementation" not in text.lower() and "UNSPECIFIED" not in text and "ASID" not in text and "read-only" not in text.lower() and "writable" not in text.lower() and "MODE" not in text:
                    # soft check — only warn if totally empty of optionality language
                    if not re.search(r"implementation|WARL|UNSPECIFIED|may |optional", text, re.I):
                        errors.append(f"{case['id']}: source lacks optionality language")

    for case in man.get("negatives") or []:
        cdir = ROOT / case["path"]
        src = cdir / "source.txt"
        exp = cdir / "expected.yaml"
        if not src.is_file() or not exp.is_file():
            errors.append(f"{case['id']}: missing files")
            continue
        exp_doc = yaml.safe_load(exp.read_text(encoding="utf-8"))
        if exp_doc.get("expect_extract") or exp_doc.get("expect_params", 0) != 0:
            errors.append(f"{case['id']}: negative must expect zero params")
        text = src.read_text(encoding="utf-8")
        if case["id"] == "NEG_SOFTWARE_ADVICE" and not re.search(r"\bshould\b|\bmay\b", text, re.I):
            errors.append("NEG_SOFTWARE_ADVICE must contain should/may")
        if case["id"] == "NEG_EXT_GATED_PBMTE":
            # recall control: must carry the phrasing but NOT the token, otherwise
            # it is not testing the under-firing case it claims to test
            if not re.search(r"read-only zero", text, re.I):
                errors.append("NEG_EXT_GATED_PBMTE must contain conditional-writability phrasing")
            if re.search(r"\bWARL\b|\bWLRL\b", text):
                errors.append("NEG_EXT_GATED_PBMTE must NOT contain a WARL/WLRL token")

    # candidates: surfaced by the extractor, then classified out. Neither a
    # positive (which yields a parameter) nor a negative (which is never seen).
    for case in man.get("candidates") or []:
        cdir = ROOT / case["path"]
        src = cdir / "source.txt"
        exp = cdir / "expected.yaml"
        if not src.is_file() or not exp.is_file():
            errors.append(f"{case['id']}: missing files")
            continue
        exp_doc = yaml.safe_load(exp.read_text(encoding="utf-8"))
        if not exp_doc.get("expect_extract"):
            errors.append(f"{case['id']}: candidate must expect_extract")
        if exp_doc.get("expect_params", None) != 0:
            errors.append(f"{case['id']}: candidate must yield zero UDB parameters")
        text = src.read_text(encoding="utf-8")
        if case["id"] == "CAND_WARL_FIXED_LEGAL_SET" and "WARL" not in text:
            errors.append("CAND_WARL_FIXED_LEGAL_SET must contain WARL keyword")

    # skill wrapper is NOT a valid UDB param file
    wrapper = {
        "parameters": [
            {
                "name": "ASID_WIDTH",
                "status": "existing",
                "definedBy": {"extension": {"name": "S"}},
                "schema": {"type": "integer", "minimum": 0, "maximum": 16},
                "classification": {"named": True, "config_dependent": True},
                "excerpt": "The number of ASID bits is UNSPECIFIED.",
                "source": {"file": "supervisor.adoc", "subsection": "satp"},
            }
        ]
    }
    # wrapper top-level is not a parameter doc
    if validator.is_valid(wrapper):
        errors.append("unexpected: skill wrapper validated as param doc")
    # first element also lacks required UDB fields
    cand = wrapper["parameters"][0]
    if validator.is_valid(cand):
        errors.append("skill candidate fields alone must not pass full param_schema without kind/description/long_name")

    # counts
    if len(man.get("positives") or []) != 6:
        errors.append(f"expected 6 positives, got {len(man.get('positives') or [])}")
    if len(man.get("negatives") or []) < 4:
        errors.append("expected >=4 negatives")
    if len(man.get("candidates") or []) < 1:
        errors.append("expected >=1 candidate (extracted then classified out)")

    # the pack must test both directions, not just over-firing
    all_cases = (man.get("positives") or []) + (man.get("negatives") or [])
    recall = [c for c in all_cases if "RECALL" in c["id"] or "EXT_GATED" in c["id"]]
    if len(recall) < 2:
        errors.append("expected >=2 recall-direction cases (no WARL/WLRL token in source)")

    if errors:
        print("eval_2097 pack FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("eval_2097 pack OK")
    print(f"  positives: {len(man['positives'])}")
    print(f"  candidates: {len(man.get('candidates') or [])}")
    print(f"  negatives: {len(man['negatives'])}")
    print(f"  recall-direction cases: {len(recall)}")
    print(f"  structural critiques: {len(critiques)}")
    print("  skill parameters: wrapper is not UDB-valid (as required)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
