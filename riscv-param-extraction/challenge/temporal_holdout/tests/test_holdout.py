#!/usr/bin/env python3
"""Unit tests: normalization, leakage, scoring integrity, failure paths."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from normalize import name_variants, normalize_param_name  # noqa: E402
from score_holdout import (  # noqa: E402
    is_infra_error_text,
    load_yaml_docs,
    name_agnostic_detection,
    name_hit,
    schema_valid,
    score_condition,
)
from leak_scan import scan_text, _forbidden_strings, load_gold  # noqa: E402
import yaml  # noqa: E402


def _minimal_valid_param(name: str = "EXAMPLE_PARAM", typ: str = "boolean") -> dict:
    return {
        "$schema": "param_schema.json#",
        "kind": "parameter",
        "name": name,
        "long_name": f"Long name for {name}",
        "description": (
            "Whether the implementation supports the architectural choice described "
            "for this parameter in the RISC-V privileged specification text."
        ),
        "definedBy": {"extension": {"name": "Sm"}},
        "schema": {"type": typ},
    }


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

    def test_schema_valid_uses_json_schema(self):
        full = _minimal_valid_param("CACHE_BLOCK_SIZE", "integer")
        full["schema"] = {"type": "integer", "minimum": 1}
        self.assertTrue(schema_valid(full), "full doc should validate")
        # Two-field stub must fail real schema (missing description, etc.)
        stub = {"name": "X", "schema": {"type": "boolean"}}
        self.assertFalse(schema_valid(stub), "name+type only must not pass jsonschema")

    def test_infra_error_not_parsed_as_params(self):
        text = "# INFRA_ERROR: RateLimitError: 429\n# case=P01 condition=baseline\n"
        self.assertTrue(is_infra_error_text(text))
        self.assertEqual(load_yaml_docs(text), [])

    def test_name_agnostic_detection_implemented(self):
        gold = {
            "name": "MTVEC_MODES",
            "description": "Modes supported by mtvec vectoring for traps and interrupts",
            "long_name": "mtvec modes",
            "schema": {"type": "array"},
        }
        # Wrong name but overlapping keywords + valid schema shape
        doc = _minimal_valid_param("TRAP_VECTOR_SETTING", "array")
        doc["description"] = (
            "Modes supported by mtvec vectoring for traps and interrupts in machine mode"
        )
        doc["schema"] = {"type": "array", "items": {"type": "integer"}}
        # May still fail full schema if array needs more — use boolean gold type match path
        gold_b = {
            "name": "SATP_MODE_BARE",
            "description": "Whether bare translation mode is supported in satp",
            "long_name": "satp bare mode",
            "schema": {"type": "boolean"},
        }
        doc_b = _minimal_valid_param("BARE_TRANSLATION_SUPPORT", "boolean")
        doc_b["description"] = (
            "Whether bare translation mode is supported for the satp MODE field"
        )
        self.assertTrue(
            name_agnostic_detection([doc_b], gold_b, "SATP_MODE_BARE", []),
            "keyword + type signal should detect without exact name",
        )
        # Empty: no detection
        self.assertFalse(name_agnostic_detection([], gold_b, "SATP_MODE_BARE", []))

    def test_class_accuracy_den_includes_misses(self):
        """Missed name must lower classification accuracy denominator."""
        manifest = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            for cond in ("baseline", "treatment"):
                d = base / cond
                d.mkdir()
                # Write empty extractions for all cases → name miss, scored
                for case in manifest["positives"] + manifest["negatives"]:
                    (d / f"{case['id']}.txt").write_text(
                        "# no parameters found\n", encoding="utf-8"
                    )
            summary = score_condition(manifest, "baseline", base)
            # classification den = 10 scored positives, hits = 0
            self.assertEqual(summary["classification_accuracy"], "0/10")
            self.assertEqual(summary["exact_or_alias_name_recall"], "0/10")
            self.assertEqual(summary["name_agnostic_detection_recall"], "0/10")
            self.assertEqual(summary["infra_or_missing"], 0)

    def test_infra_error_excluded_from_model_metrics(self):
        manifest = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            for cond in ("baseline", "treatment"):
                d = base / cond
                d.mkdir()
                for case in manifest["positives"] + manifest["negatives"]:
                    p = d / f"{case['id']}.txt"
                    if case["id"] == "P01":
                        p.write_text(
                            "# INFRA_ERROR: APIConnectionError: network\n",
                            encoding="utf-8",
                        )
                        p.with_suffix(".txt.status.json").write_text(
                            json.dumps({"ok": False, "status": "infra_error"}) + "\n",
                            encoding="utf-8",
                        )
                    else:
                        p.write_text("# no parameters found\n", encoding="utf-8")
            summary = score_condition(manifest, "baseline", base)
            # P01 excluded → 9 scored positives
            self.assertEqual(summary["n_positives_scored"], 9)
            self.assertGreaterEqual(summary["infra_or_missing"], 1)
            self.assertEqual(summary["exact_or_alias_name_recall"], "0/9")
            self.assertNotEqual(
                summary["exact_or_alias_name_recall"],
                "0/10",
                "infra must not be counted as model miss denominator 10",
            )


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
        docs = load_yaml_docs("")
        self.assertEqual(docs, [])


class TestRunLiveFailurePath(unittest.TestCase):
    def test_write_infra_error_markers(self):
        sys.path.insert(0, str(SCRIPTS))
        from run_live import write_infra_error  # noqa: WPS433

        with tempfile.TemporaryDirectory() as td:
            raw = Path(td) / "raw.txt"
            parsed = Path(td) / "P01.txt"
            write_infra_error(parsed, raw, "TimeoutError: x", "P01", "baseline")
            self.assertTrue(is_infra_error_text(parsed.read_text(encoding="utf-8")))
            self.assertTrue((parsed.with_suffix(".txt.status.json")).is_file() or parsed.with_name("P01.txt.status.json").is_file())
            status_path = Path(str(parsed) + ".status.json")
            self.assertTrue(status_path.is_file())
            meta = json.loads(status_path.read_text(encoding="utf-8"))
            self.assertFalse(meta["ok"])
            self.assertEqual(meta["status"], "infra_error")
            # Must not look like a successful empty model answer
            self.assertIn("INFRA_ERROR", parsed.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
