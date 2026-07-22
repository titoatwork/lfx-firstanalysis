"""Unit tests for Artifact B exporter (no API, no network)."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from export.csv_to_param_yaml import (
    CsvRow,
    dedupe_prefer_named,
    export,
    load_csv,
)
from export.schema_validate import validate_param_dict
from export.value_type_map import schema_for_value_type


class ValueTypeMapTests(unittest.TestCase):
    def test_binary_is_boolean(self) -> None:
        s = schema_for_value_type("binary")
        self.assertEqual(s["type"], "boolean")

    def test_set_is_unique_array(self) -> None:
        s = schema_for_value_type("set")
        self.assertEqual(s["type"], "array")
        self.assertTrue(s.get("uniqueItems"))

    def test_unknown_still_returns_schema(self) -> None:
        s = schema_for_value_type("not-a-real-type")
        self.assertIn("type", s)


class DedupeTests(unittest.TestCase):
    def test_prefers_named_yes(self) -> None:
        rows = [
            CsvRow("a.adoc", "1", "short", "FOO", "no", "NORM_DIRECT", "binary", "high", ""),
            CsvRow("b.adoc", "2", "longer excerpt here", "FOO", "yes", "NORM_DIRECT", "binary", "medium", ""),
        ]
        best = dedupe_prefer_named(rows)
        self.assertEqual(best["FOO"].adoc_file, "b.adoc")
        self.assertTrue(best["FOO"].is_named)


class ExportIntegrationTests(unittest.TestCase):
    def test_named_export_validates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "parameters.csv"
            out_dir = root / "drafts"
            with csv_path.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(
                    f,
                    fieldnames=[
                        "adoc_file",
                        "line_number",
                        "excerpt",
                        "parameter_name",
                        "named",
                        "class",
                        "value_type",
                        "confidence",
                        "notes",
                    ],
                )
                w.writeheader()
                w.writerow(
                    {
                        "adoc_file": "machine.adoc",
                        "line_number": "10",
                        "excerpt": "Example implementer choice for tests.",
                        "parameter_name": "TEST_PARAM_BINARY",
                        "named": "yes",
                        "class": "NORM_DIRECT",
                        "value_type": "binary",
                        "confidence": "high",
                        "notes": "",
                    }
                )

            summary = export(
                csv_path=csv_path,
                out_dir=out_dir,
                mode="named",
                udb_root=None,
                limit=None,
                clean=True,
            )
            self.assertEqual(summary.written, 1)
            self.assertEqual(summary.schema_fail, 0)
            yaml_path = out_dir / "TEST_PARAM_BINARY.yaml"
            self.assertTrue(yaml_path.is_file())
            text = yaml_path.read_text(encoding="utf-8")
            self.assertIn("DRAFT", text)
            self.assertIn("kind: parameter", text)


class SchemaFixtureTests(unittest.TestCase):
    def test_minimal_doc_validates(self) -> None:
        doc = {
            "$schema": "param_schema.json#",
            "kind": "parameter",
            "name": "EXAMPLE_PARAM",
            "long_name": "Example",
            "description": "Example description",
            "definedBy": {"extension": {"name": "Sm"}},
            "schema": {"type": "boolean"},
        }
        errs = validate_param_dict(doc)
        self.assertEqual(errs, [], msg=errs)


if __name__ == "__main__":
    unittest.main()
