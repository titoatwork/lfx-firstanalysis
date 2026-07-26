#!/usr/bin/env python3
"""Unit tests: normalization, leakage fail-closed, scoring, negatives."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from normalize import name_variants, normalize_param_name  # noqa: E402
from score_holdout import load_yaml_docs, name_hit, schema_valid  # noqa: E402
from leak_scan import scan_text, _forbidden_strings, load_gold  # noqa: E402
import yaml  # noqa: E402


class TestNormalize(unittest.TestCase):
    def test_normalize_strips_underscores(self):
        self.assertEqual(normalize_param_name("MTVEC_MODES"), "MTVECMODES")
        self.assertEqual(normalize_param_name("mtvec-modes"), "MTVECMODES")

    def test_variants_include_exact_and_norm(self):
        v = name_variants("MTVEC_MODES")
        self.assertIn("MTVEC_MODES", v)
        self.assertIn("MTVECMODES", v)


class TestLeakage(unittest.TestCase):
    def test_clean_context_has_no_gold_names(self):
        ctx_path = ROOT / "contexts" / "mtvec.txt"
        if not ctx_path.is_file():
            self.skipTest("contexts not built yet")
        ctx = ctx_path.read_text(encoding="utf-8")
        self.assertNotIn("MTVEC_MODES", ctx)
        self.assertNotIn("MTVEC_ACCESS", ctx)

    def test_leaked_name_detected(self):
        if not (SCRIPTS / "leak_scan.py").is_file():
            self.skipTest("leak_scan not present")
        gold = load_gold(ROOT / "gold" / "MTVEC_MODES.yaml")
        case = {"name": "MTVEC_MODES", "aliases": ["MTVEC_MODE"]}
        needles = _forbidden_strings(case, gold)
        errs = scan_text("The parameter MTVEC_MODES controls modes.", needles)
        self.assertTrue(errs)

    def test_leak_scan_cli_clean(self):
        if not (SCRIPTS / "leak_scan.py").is_file():
            self.skipTest("leak_scan not present")
        if not (ROOT / "contexts" / "mtvec.txt").is_file():
            self.skipTest("contexts not built yet")
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "leak_scan.py")],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_leak_scan_fixture_expect_fail(self):
        if not (SCRIPTS / "leak_scan.py").is_file():
            self.skipTest("leak_scan not present")
        fix = ROOT / "fixtures" / "leaked" / "contains_param_name.txt"
        if not fix.is_file():
            self.skipTest("leak fixture missing")
        r = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "leak_scan.py"),
                "--fixture",
                str(fix),
                "--expect-fail",
            ],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestScoring(unittest.TestCase):
    def test_load_yaml_docs(self):
        text = """
$schema: param_schema.json#
kind: parameter
name: MTVEC_MODES
schema:
  type: array
---
name: OTHER
schema: {type: boolean}
"""
        docs = load_yaml_docs(text)
        self.assertGreaterEqual(len(docs), 1)
        self.assertTrue(any(d.get("name") == "MTVEC_MODES" for d in docs))

    def test_name_hit_alias(self):
        docs = [{"name": "TRAP_VECTOR_MODES", "schema": {"type": "array"}}]
        hit = name_hit(docs, "MTVEC_MODES", ["TRAP_VECTOR_MODES"])
        self.assertIsNotNone(hit)

    def test_schema_valid(self):
        self.assertTrue(schema_valid({"name": "X", "schema": {"type": "boolean"}}))
        self.assertFalse(schema_valid({"name": "X"}))


class TestManifest(unittest.TestCase):
    def test_strata_counts(self):
        m = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        pos = m["positives"]
        self.assertEqual(len(pos), 10)
        self.assertEqual(sum(1 for c in pos if c["strata"] == "warl"), 5)
        self.assertEqual(sum(1 for c in pos if c["strata"] in ("csr_rw", "wlrl")), 2)
        self.assertEqual(sum(1 for c in pos if c["strata"] == "direct"), 3)
        self.assertEqual(len(m["negatives"]), 3)

    def test_temporal_after_model(self):
        m = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        release = m["pins"]["model_release_date"]
        for c in m["positives"]:
            self.assertGreater(c["udb_first_add_date"], release, c["name"])

    def test_sources_exist(self):
        m = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        for c in m["positives"] + m["negatives"]:
            p = ROOT / c["source_path"]
            self.assertTrue(p.is_file(), p)
            self.assertGreater(p.stat().st_size, 40)


class TestNegativesExpectZero(unittest.TestCase):
    def test_empty_extraction_scores_clean(self):
        # scorer treats empty file as 0 docs → no FP
        docs = load_yaml_docs("")
        self.assertEqual(docs, [])


if __name__ == "__main__":
    unittest.main()
