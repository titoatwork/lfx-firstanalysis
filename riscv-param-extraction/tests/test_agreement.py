"""Offline unit tests for Artifact A agreement / hallucination-overlap."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pipeline.agreement import (
    compute_agreement,
    compute_hallucination_overlap,
    is_proposed_new,
)
from pipeline.load_results import deduplicate_params, load_param_list


class DedupTests(unittest.TestCase):
    def test_keeps_higher_confidence(self) -> None:
        params = [
            {"parameter_name": "FOO", "confidence": "medium", "class": "NORM_DIRECT"},
            {"parameter_name": "FOO", "confidence": "high", "class": "NORM_CSR_RW"},
        ]
        out = deduplicate_params(params)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["confidence"], "high")
        self.assertEqual(out[0]["class"], "NORM_CSR_RW")


class AgreementTests(unittest.TestCase):
    def test_self_agreement_is_full(self) -> None:
        params = [
            {"parameter_name": "A", "class": "NORM_DIRECT", "confidence": "high"},
            {"parameter_name": "B", "class": "NORM_CSR_WARL", "confidence": "medium"},
        ]
        r = compute_agreement(params, params, model_a="x", model_b="x")
        self.assertEqual(r.n_a, 2)
        self.assertEqual(len(r.shared_names), 2)
        self.assertEqual(r.jaccard, 1.0)
        self.assertEqual(r.match_rate_vs_a, 1.0)
        self.assertEqual(r.class_agreement_rate, 1.0)

    def test_partial_overlap(self) -> None:
        a = [
            {"parameter_name": "SHARED", "class": "NORM_DIRECT", "confidence": "high"},
            {"parameter_name": "ONLY_A", "class": "NORM_DIRECT", "confidence": "high"},
        ]
        b = [
            {"parameter_name": "SHARED", "class": "NORM_CSR_RW", "confidence": "high"},
            {"parameter_name": "ONLY_B", "class": "NORM_DIRECT", "confidence": "high"},
        ]
        r = compute_agreement(a, b, model_a="a", model_b="b")
        self.assertEqual(r.shared_names, ["SHARED"])
        self.assertEqual(r.only_a, ["ONLY_A"])
        self.assertEqual(r.only_b, ["ONLY_B"])
        self.assertEqual(r.shared_class_disagree, 1)
        self.assertEqual(r.class_agreement_rate, 0.0)


class HallucinationTests(unittest.TestCase):
    def test_proposed_new_filter(self) -> None:
        udb = {"REAL_PARAM"}
        self.assertFalse(
            is_proposed_new(
                {"parameter_name": "REAL_PARAM", "existing_udb_name": "REAL_PARAM"},
                udb,
            )
        )
        self.assertTrue(
            is_proposed_new(
                {"parameter_name": "HALLUC", "existing_udb_name": None},
                udb,
            )
        )

    def test_overlap_counts(self) -> None:
        udb = {"KNOWN"}
        a = [
            {"parameter_name": "BOTH_NEW", "confidence": "high"},
            {"parameter_name": "ONLY_A_NEW", "confidence": "high"},
            {"parameter_name": "KNOWN", "confidence": "high", "existing_udb_name": "KNOWN"},
            {"parameter_name": "LOW_NEW", "confidence": "low"},
        ]
        b = [
            {"parameter_name": "BOTH_NEW", "confidence": "high"},
            {"parameter_name": "ONLY_B_NEW", "confidence": "high"},
        ]
        h = compute_hallucination_overlap(
            a, b, udb, model_a="a", model_b="b", high_confidence_only=True
        )
        self.assertEqual(h.both_new, ["BOTH_NEW"])
        self.assertEqual(h.only_a_new, ["ONLY_A_NEW"])
        self.assertEqual(h.only_b_new, ["ONLY_B_NEW"])
        self.assertNotIn("LOW_NEW", h.new_a)
        self.assertNotIn("KNOWN", h.new_a)


class LoadMergedTests(unittest.TestCase):
    def test_load_merged_shape(self) -> None:
        payload = {
            "results": [
                {
                    "chunk_id": "c1",
                    "parameters": [
                        {"parameter_name": "X", "confidence": "low"},
                        {"parameter_name": "X", "confidence": "high"},
                    ],
                }
            ]
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "merged.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            params = load_param_list(path)
            self.assertEqual(len(params), 1)
            self.assertEqual(params[0]["confidence"], "high")


if __name__ == "__main__":
    unittest.main()
