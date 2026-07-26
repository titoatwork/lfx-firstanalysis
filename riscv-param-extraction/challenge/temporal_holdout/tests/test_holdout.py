#!/usr/bin/env python3
"""Unit tests: integrity gates for pre-live holdout pilot."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from normalize import name_variants, normalize_param_name  # noqa: E402
from score_holdout import (  # noqa: E402
    name_agnostic_detection,
    name_hit,
    parse_model_output,
    quote_grounded,
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


def _model_text(param: dict, eval_items: list) -> str:
    return yaml.safe_dump(param, sort_keys=False) + "\n" + json.dumps({"eval": True, "items": eval_items}) + "\n"


class TestNormalize(unittest.TestCase):
    def test_normalize_strips_underscores(self):
        self.assertEqual(normalize_param_name("MTVEC_MODES"), "MTVECMODES")

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

    def test_leaked_name_detected(self):
        gold = load_gold(ROOT / "gold" / "MTVEC_MODES.yaml")
        case = {"name": "MTVEC_MODES", "aliases": ["MTVEC_MODE"]}
        errs = scan_text("The parameter MTVEC_MODES controls modes.", _forbidden_strings(case, gold))
        self.assertTrue(errs)

    def test_leak_scan_cli_clean(self):
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "leak_scan.py")],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_leak_scan_fixture_expect_fail(self):
        fix = ROOT / "fixtures" / "leaked" / "contains_param_name.txt"
        r = subprocess.run(
            [sys.executable, str(SCRIPTS / "leak_scan.py"), "--fixture", str(fix), "--expect-fail"],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TestSchemaUntouched(unittest.TestCase):
    def test_full_doc_validates(self):
        self.assertTrue(schema_valid(_minimal_valid_param()))

    def test_class_on_param_fails_schema(self):
        doc = _minimal_valid_param()
        doc["class"] = "NORM_CSR_WARL"
        self.assertFalse(schema_valid(doc), "UDB additionalProperties:false must reject class")

    def test_no_injection_missing_schema_fails(self):
        doc = _minimal_valid_param()
        del doc["$schema"]
        self.assertFalse(schema_valid(doc), "must not inject missing $schema")

    def test_no_injection_missing_kind_fails(self):
        doc = _minimal_valid_param()
        del doc["kind"]
        self.assertFalse(schema_valid(doc), "must not inject missing kind")


class TestParseAndGrounding(unittest.TestCase):
    def test_parse_separates_eval_metadata(self):
        param = _minimal_valid_param("MTVEC_MODES", "array")
        param["schema"] = {"type": "array", "items": {"type": "integer"}}
        text = _model_text(
            param,
            [{"name": "MTVEC_MODES", "class": "NORM_CSR_WARL", "quote": "MODE may support Direct"}],
        )
        docs, items = parse_model_output(text)
        self.assertEqual(len(docs), 1)
        self.assertNotIn("class", docs[0])
        self.assertEqual(items[0]["class"], "NORM_CSR_WARL")

    def test_missing_quote_not_grounded(self):
        self.assertFalse(quote_grounded(None, "source text here with enough chars", ""))
        self.assertFalse(quote_grounded("", "source text here with enough chars", ""))
        self.assertFalse(quote_grounded("  ", "source text here with enough chars", ""))

    def test_quote_present_and_in_source(self):
        src = "MODE may support Direct and Vectored modes for traps."
        self.assertTrue(quote_grounded("MODE may support Direct", src, ""))

    def test_per_param_grounding_denominator_includes_missing(self):
        manifest = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        # Use MTVEC_MODES case source for quote
        p01 = next(c for c in manifest["positives"] if c["id"] == "P01")
        src = (ROOT / p01["source_path"]).read_text(encoding="utf-8")
        # take a real substring from source
        quote = " ".join(src.split()[:12])
        param = _minimal_valid_param("MTVEC_MODES", "array")
        param["schema"] = {
            "type": "array",
            "items": {"type": "integer", "enum": [0, 1]},
            "minItems": 1,
            "uniqueItems": True,
        }
        good = _model_text(
            param,
            [{"name": "MTVEC_MODES", "class": "NORM_CSR_WARL", "quote": quote}],
        )
        bad = _model_text(
            param,
            [{"name": "MTVEC_MODES", "class": "NORM_CSR_WARL"}],  # missing quote
        )
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            for cond in ("baseline", "treatment"):
                d = base / cond
                d.mkdir()
                for case in manifest["positives"] + manifest["negatives"]:
                    if case["id"] == "P01":
                        (d / "P01.txt").write_text(bad if cond == "baseline" else good, encoding="utf-8")
                    else:
                        (d / f"{case['id']}.txt").write_text(
                            json.dumps({"eval": True, "items": []}) + "\n",
                            encoding="utf-8",
                        )
            s_base = score_condition(manifest, "baseline", base)
            s_treat = score_condition(manifest, "treatment", base)
            # baseline: one extracted param, missing quote → 0/1
            self.assertEqual(s_base["quote_grounding"], "0/1")
            # treatment: grounded → 1/1
            self.assertEqual(s_treat["quote_grounding"], "1/1")


class TestScoringMetrics(unittest.TestCase):
    def test_name_hit_alias(self):
        docs = [{"name": "TRAP_VECTOR_MODES", "schema": {"type": "array"}}]
        self.assertIsNotNone(name_hit(docs, "MTVEC_MODES", ["TRAP_VECTOR_MODES"]))

    def test_name_agnostic_detection(self):
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
        self.assertTrue(name_agnostic_detection([doc_b], gold_b, "SATP_MODE_BARE", []))

    def test_class_accuracy_den_includes_misses(self):
        manifest = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            for cond in ("baseline", "treatment"):
                d = base / cond
                d.mkdir()
                for case in manifest["positives"] + manifest["negatives"]:
                    (d / f"{case['id']}.txt").write_text(
                        json.dumps({"eval": True, "items": []}) + "\n",
                        encoding="utf-8",
                    )
            summary = score_condition(manifest, "baseline", base)
            self.assertEqual(summary["classification_accuracy"], "0/10")
            self.assertEqual(summary["exact_or_alias_name_recall"], "0/10")


class TestRunLiveGates(unittest.TestCase):
    def test_model_pin_mismatch_exits_before_calls(self):
        r = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "run_live.py"),
                "--live",
                "--model",
                "gpt-4o-not-the-pin",
            ],
            cwd=str(SCRIPTS),
            capture_output=True,
            text=True,
            env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "OPENAI_API_KEY": "sk-test-fake"},
        )
        self.assertEqual(r.returncode, 2)
        self.assertIn("FAIL-CLOSED", r.stderr)
        self.assertIn("No API calls", r.stderr)

    def test_refuse_overwrite_existing_run(self):
        with tempfile.TemporaryDirectory() as td:
            fake_runs = Path(td) / "runs"
            run_id = "already_exists_model"
            (fake_runs / run_id).mkdir(parents=True)
            with mock.patch("run_live.RUNS", fake_runs):
                with mock.patch("run_live.PRIMARY_POINTER", Path(td) / "PRIMARY_RUN.json"):
                    with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-fake"}):
                        import run_live as rl

                        argv = ["run_live.py", "--live", "--model", "gpt-4o-mini-2024-07-18", "--run-id", run_id]
                        with mock.patch.object(sys, "argv", argv):
                            code = rl.main()
            self.assertEqual(code, 2)

    def test_refuse_second_primary_when_pointer_exists(self):
        with tempfile.TemporaryDirectory() as td:
            fake_runs = Path(td) / "runs"
            fake_runs.mkdir()
            primary = Path(td) / "PRIMARY_RUN.json"
            primary.write_text(json.dumps({"run_id": "locked", "locked": True}) + "\n", encoding="utf-8")
            with mock.patch("run_live.RUNS", fake_runs):
                with mock.patch("run_live.PRIMARY_POINTER", primary):
                    with mock.patch.dict("os.environ", {"OPENAI_API_KEY": "sk-test-fake"}):
                        import run_live as rl

                        argv = [
                            "run_live.py",
                            "--live",
                            "--model",
                            "gpt-4o-mini-2024-07-18",
                            "--run-id",
                            "second_primary",
                        ]
                        with mock.patch.object(sys, "argv", argv):
                            code = rl.main()
            self.assertEqual(code, 2)


class TestPrimaryMetaGate(unittest.TestCase):
    def test_results_dir_without_run_meta_not_primary(self):
        from score_holdout import validate_primary_meta  # noqa: WPS433

        manifest = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            for cond in ("baseline", "treatment"):
                d = base / cond
                d.mkdir()
                for case in manifest["positives"] + manifest["negatives"]:
                    (d / f"{case['id']}.txt").write_text(
                        json.dumps({"eval": True, "items": []}) + "\n", encoding="utf-8"
                    )
            errs = validate_primary_meta(None, manifest, base)
            self.assertTrue(any("RUN_META" in e for e in errs))

    def test_schema_totals_include_negative_extractions(self):
        manifest = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        param = _minimal_valid_param("FAKE_NEG", "boolean")
        text = _model_text(param, [{"name": "FAKE_NEG", "class": "OTHER", "quote": "not in source really"}])
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            for cond in ("baseline", "treatment"):
                d = base / cond
                d.mkdir()
                for case in manifest["positives"] + manifest["negatives"]:
                    if case["id"] == "N01":
                        (d / "N01.txt").write_text(text, encoding="utf-8")
                    else:
                        (d / f"{case['id']}.txt").write_text(
                            json.dumps({"eval": True, "items": []}) + "\n", encoding="utf-8"
                        )
            s = score_condition(manifest, "baseline", base)
            # one doc from N01 counted in schema totals
            self.assertEqual(s["schema_validity_docs"], "1/1")


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

    def test_prompt_version_bumped(self):
        m = yaml.safe_load((ROOT / "manifests" / "holdout_cases.yaml").read_text(encoding="utf-8"))
        self.assertEqual(m["pins"]["prompt_version"], "holdout-v1.2")
        # SEW_MIN must not be guided as Sm-only
        p09 = next(c for c in m["positives"] if c["id"] == "P09")
        self.assertIn("Zvl32b", p09.get("definedby_guidance", ""))


if __name__ == "__main__":
    unittest.main()
