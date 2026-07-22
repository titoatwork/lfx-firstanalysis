#!/usr/bin/env python3
"""
Artifact B — parameters.csv → draft UDB param YAML.

Maps Part I spreadsheet rows to draft files under drafts/param/, validates
each document against a vendored copy of UDB param_schema.json, and (when
--udb-root is given) reports name-overlap / definedBy reuse against live UDB.

Does **not** claim merge readiness. Every file is marked DRAFT.

Usage:
  python -m export.csv_to_param_yaml \\
      --csv data/parameters.csv \\
      --out drafts/param \\
      --mode named \\
      --udb-root ../riscv-unified-db

  python -m export.csv_to_param_yaml --mode new --limit 20 --udb-root ...
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Literal, Optional

import yaml

from export.adoc_extension import guess_extension
from export.schema_validate import validate_param_dict, validate_yaml_file
from export.value_type_map import schema_for_value_type

REPO_ROOT = Path(__file__).resolve().parent.parent
PARAM_NAME_RE = re.compile(r"^[A-Z][A-Z_0-9]*$")

Mode = Literal["named", "new", "all"]


@dataclass
class CsvRow:
    adoc_file: str
    line_number: str
    excerpt: str
    parameter_name: str
    named: str
    class_: str
    value_type: str
    confidence: str
    notes: str

    @property
    def is_named(self) -> bool:
        return self.named.strip().lower() in {"yes", "y", "true", "1"}


@dataclass
class ExportRecord:
    name: str
    path: str
    mode_bucket: str  # named_existing | named_missing_udb | new_candidate
    named: bool
    class_: str
    value_type: str
    confidence: str
    adoc_file: str
    line_number: str
    defined_by_source: str  # udb_copy | adoc_map | fallback
    extension: str
    schema_valid: bool
    validation_errors: list[str] = field(default_factory=list)
    udb_exists: bool = False


@dataclass
class ExportSummary:
    generated_at: str
    mode: str
    csv_path: str
    out_dir: str
    udb_root: Optional[str]
    rows_read: int
    unique_names: int
    named_yes_rows: int
    named_yes_unique: int
    written: int
    schema_ok: int
    schema_fail: int
    udb_overlap: int
    class_counts: dict[str, int]
    records: list[ExportRecord]


def load_csv(path: Path) -> list[CsvRow]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {
            "adoc_file",
            "line_number",
            "excerpt",
            "parameter_name",
            "named",
            "class",
            "value_type",
            "confidence",
            "notes",
        }
        if reader.fieldnames is None:
            raise SystemExit(f"empty CSV: {path}")
        missing = required - set(reader.fieldnames)
        if missing:
            raise SystemExit(f"CSV missing columns {sorted(missing)}: {path}")

        rows: list[CsvRow] = []
        for raw in reader:
            rows.append(
                CsvRow(
                    adoc_file=(raw.get("adoc_file") or "").strip(),
                    line_number=(raw.get("line_number") or "").strip(),
                    excerpt=(raw.get("excerpt") or "").strip(),
                    parameter_name=(raw.get("parameter_name") or "").strip(),
                    named=(raw.get("named") or "").strip(),
                    class_=(raw.get("class") or "").strip(),
                    value_type=(raw.get("value_type") or "").strip(),
                    confidence=(raw.get("confidence") or "").strip(),
                    notes=(raw.get("notes") or "").strip(),
                )
            )
        return rows


def dedupe_prefer_named(rows: Iterable[CsvRow]) -> dict[str, CsvRow]:
    """
    One row per parameter_name. Prefer named=yes, then higher confidence,
    then longer excerpt (more context).
    """
    conf_rank = {"high": 3, "medium": 2, "low": 1}
    best: dict[str, CsvRow] = {}

    def score(r: CsvRow) -> tuple:
        return (
            1 if r.is_named else 0,
            conf_rank.get(r.confidence.lower(), 0),
            len(r.excerpt),
        )

    for r in rows:
        if not r.parameter_name:
            continue
        prev = best.get(r.parameter_name)
        if prev is None or score(r) > score(prev):
            best[r.parameter_name] = r
    return best


def load_udb_param_names(udb_root: Optional[Path]) -> set[str]:
    if udb_root is None:
        return set()
    param_dir = udb_root / "spec" / "std" / "isa" / "param"
    if not param_dir.is_dir():
        return set()
    return {p.stem for p in param_dir.glob("*.yaml")}


def load_udb_defined_by(udb_root: Path, name: str) -> Optional[dict[str, Any]]:
    path = udb_root / "spec" / "std" / "isa" / "param" / f"{name}.yaml"
    if not path.is_file():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    if isinstance(doc, dict) and isinstance(doc.get("definedBy"), dict):
        return doc["definedBy"]
    return None


def _yaml_str_block(text: str) -> str:
    """Normalize excerpt for YAML description block."""
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not cleaned:
        return (
            "DRAFT: no excerpt in parameters.csv. "
            "Replace with ISA-manual prose before any upstream contribution."
        )
    return cleaned


def build_param_doc(
    row: CsvRow,
    *,
    defined_by: dict[str, Any],
    defined_by_source: str,
    bucket: str,
) -> dict[str, Any]:
    excerpt = _yaml_str_block(row.excerpt)
    long_name = (
        f"DRAFT from Part I spreadsheet ({row.class_} / {row.value_type})"
    )
    # Keep the ISA excerpt first; pack provenance in a compact NOTE so mentors
    # can audit locus without inventing schema fields (additionalProperties: false).
    note_bits = [
        f"class={row.class_}",
        f"value_type={row.value_type}",
        f"confidence={row.confidence}",
        f"named={row.named}",
        f"source={row.adoc_file}:{row.line_number}",
        f"definedBy_source={defined_by_source}",
        f"bucket={bucket}",
    ]
    description_parts = [
        excerpt,
        "",
        "[NOTE]",
        "====",
        "DRAFT from Part I parameters.csv (" + "; ".join(note_bits) + ").",
        "Not reviewed for merge into riscv/riscv-unified-db.",
        "====",
    ]
    if row.notes:
        description_parts.extend(["", f"Spreadsheet notes: {row.notes}"])
    description = "\n".join(description_parts) + "\n"

    doc: dict[str, Any] = {
        "$schema": "param_schema.json#",
        "kind": "parameter",
        "name": row.parameter_name,
        "long_name": long_name,
        "description": description,
        "definedBy": defined_by,
        "schema": schema_for_value_type(row.value_type),
        "$source": f"parameters.csv:{row.adoc_file}:{row.line_number}",
    }
    return doc


def _str_representer(dumper: yaml.Dumper, data: str) -> yaml.Node:
    """Prefer block scalars for multi-line strings (readable drafts)."""
    if "\n" in data:
        # Ensure trailing newline so PyYAML uses '|' not '|-'
        payload = data if data.endswith("\n") else data + "\n"
        return dumper.represent_scalar("tag:yaml.org,2002:str", payload, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


class _DraftDumper(yaml.SafeDumper):
    pass


_DraftDumper.add_representer(str, _str_representer)


def render_yaml(doc: dict[str, Any], header_comments: list[str]) -> str:
    """
    Emit stable, reviewable YAML. Uses safe_dump with explicit ordering.
    """
    # Preferred key order for human review (matches UDB samples).
    order = [
        "$schema",
        "kind",
        "name",
        "long_name",
        "definedBy",
        "description",
        "schema",
        "requirements",
        "$source",
    ]
    ordered: dict[str, Any] = {}
    for k in order:
        if k in doc:
            ordered[k] = doc[k]
    for k, v in doc.items():
        if k not in ordered:
            ordered[k] = v

    body = yaml.dump(
        ordered,
        Dumper=_DraftDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=88,
    )
    lines = [f"# {c}" if not c.startswith("#") else c for c in header_comments]
    lines.append("")
    lines.append(
        "# yaml-language-server: $schema=../../../export/schemas/param_schema.json"
    )
    lines.append("")
    return "\n".join(lines) + "\n" + body


def select_rows(
    by_name: dict[str, CsvRow],
    *,
    mode: Mode,
    udb_names: set[str],
    limit: Optional[int],
) -> list[tuple[str, CsvRow, str]]:
    """
    Return list of (name, row, bucket).

    buckets:
      named_existing — named=yes and present in UDB
      named_missing_udb — named=yes but not in UDB (unexpected on current freeze)
      new_candidate — named=no and not in UDB
    """
    items: list[tuple[str, CsvRow, str]] = []

    for name, row in sorted(by_name.items()):
        in_udb = name in udb_names
        if row.is_named:
            bucket = "named_existing" if in_udb else "named_missing_udb"
            if mode in ("named", "all"):
                items.append((name, row, bucket))
        else:
            if in_udb:
                continue  # already has UDB YAML; not a "new" draft target
            bucket = "new_candidate"
            if mode in ("new", "all"):
                items.append((name, row, bucket))

    # Prefer high-confidence for new candidates when limiting.
    if mode == "new" and limit is not None:
        conf_rank = {"high": 3, "medium": 2, "low": 1}

        def sort_key(t: tuple[str, CsvRow, str]) -> tuple:
            _n, r, _b = t
            return (-conf_rank.get(r.confidence.lower(), 0), r.parameter_name)

        items = sorted(items, key=sort_key)[:limit]
    elif limit is not None and mode != "named":
        items = items[:limit]

    return items


def resolve_defined_by(
    name: str,
    row: CsvRow,
    udb_root: Optional[Path],
) -> tuple[dict[str, Any], str, str]:
    """Return (definedBy, source_tag, extension_name_for_summary)."""
    if udb_root is not None:
        copied = load_udb_defined_by(udb_root, name)
        if copied is not None:
            ext = ""
            if isinstance(copied.get("extension"), dict):
                ext = str(copied["extension"].get("name") or "")
            return copied, "udb_copy", ext or "?"

    ext, conf = guess_extension(row.adoc_file)
    source = "adoc_map" if conf in ("mapped", "filename") else "fallback"
    return {"extension": {"name": ext}}, source, ext


def export(
    *,
    csv_path: Path,
    out_dir: Path,
    mode: Mode,
    udb_root: Optional[Path],
    limit: Optional[int],
    clean: bool,
) -> ExportSummary:
    rows = load_csv(csv_path)
    by_name = dedupe_prefer_named(rows)
    udb_names = load_udb_param_names(udb_root)

    selected = select_rows(by_name, mode=mode, udb_names=udb_names, limit=limit)

    if clean and out_dir.exists():
        for old in out_dir.glob("*.yaml"):
            old.unlink()
    out_dir.mkdir(parents=True, exist_ok=True)

    records: list[ExportRecord] = []
    class_counts: Counter[str] = Counter()

    for name, row, bucket in selected:
        if not PARAM_NAME_RE.match(name):
            records.append(
                ExportRecord(
                    name=name,
                    path="",
                    mode_bucket=bucket,
                    named=row.is_named,
                    class_=row.class_,
                    value_type=row.value_type,
                    confidence=row.confidence,
                    adoc_file=row.adoc_file,
                    line_number=row.line_number,
                    defined_by_source="invalid_name",
                    extension="",
                    schema_valid=False,
                    validation_errors=[
                        f"parameter_name fails UDB pattern: {name!r}"
                    ],
                    udb_exists=name in udb_names,
                )
            )
            continue

        defined_by, db_source, ext = resolve_defined_by(name, row, udb_root)
        doc = build_param_doc(
            row,
            defined_by=defined_by,
            defined_by_source=db_source,
            bucket=bucket,
        )

        header = [
            "DRAFT - generated by export/csv_to_param_yaml.py",
            "NOT for unsolicited merge into riscv/riscv-unified-db",
            f"bucket: {bucket}",
            f"provenance: parameters.csv name={name} named={row.named} "
            f"class={row.class_} value_type={row.value_type} "
            f"confidence={row.confidence}",
            f"spec_locus: {row.adoc_file}:{row.line_number}",
            f"definedBy_source: {db_source}",
            "Copyright (c) 2026 Ibteshamul Haque",
            "SPDX-License-Identifier: BSD-3-Clause-Clear",
        ]
        text = render_yaml(doc, header)
        out_path = out_dir / f"{name}.yaml"
        out_path.write_text(text, encoding="utf-8", newline="\n")

        # Validate both the in-memory doc and the round-tripped file.
        errs = validate_param_dict(doc)
        file_result = validate_yaml_file(out_path)
        if file_result.errors:
            # Prefer file-level errors if they differ (parse issues).
            for e in file_result.errors:
                if e not in errs:
                    errs.append(e)

        try:
            rel_path = str(out_path.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            rel_path = str(out_path).replace("\\", "/")

        class_counts[row.class_ or "UNKNOWN"] += 1
        records.append(
            ExportRecord(
                name=name,
                path=rel_path,
                mode_bucket=bucket,
                named=row.is_named,
                class_=row.class_,
                value_type=row.value_type,
                confidence=row.confidence,
                adoc_file=row.adoc_file,
                line_number=row.line_number,
                defined_by_source=db_source,
                extension=ext,
                schema_valid=not errs,
                validation_errors=errs,
                udb_exists=name in udb_names,
            )
        )

    written = sum(1 for r in records if r.path)
    schema_ok = sum(1 for r in records if r.schema_valid)
    schema_fail = written - schema_ok
    named_rows = [r for r in rows if r.is_named]
    named_unique = {r.parameter_name for r in named_rows}

    try:
        out_dir_s = str(out_dir.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        out_dir_s = str(out_dir).replace("\\", "/")

    return ExportSummary(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        mode=mode,
        csv_path=str(csv_path).replace("\\", "/"),
        out_dir=out_dir_s,
        udb_root=str(udb_root).replace("\\", "/") if udb_root else None,
        rows_read=len(rows),
        unique_names=len(by_name),
        named_yes_rows=len(named_rows),
        named_yes_unique=len(named_unique),
        written=written,
        schema_ok=schema_ok,
        schema_fail=schema_fail,
        udb_overlap=sum(1 for r in records if r.udb_exists),
        class_counts=dict(class_counts),
        records=records,
    )


def write_report(summary: ExportSummary, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(summary)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def print_human_summary(summary: ExportSummary) -> None:
    print("=== Artifact B export summary ===")
    print(f"mode:            {summary.mode}")
    print(f"rows_read:       {summary.rows_read}")
    print(f"unique_names:    {summary.unique_names}")
    print(
        f"named=yes:       {summary.named_yes_rows} rows / "
        f"{summary.named_yes_unique} unique"
    )
    print(f"written:         {summary.written}")
    print(f"schema_ok:       {summary.schema_ok}")
    print(f"schema_fail:     {summary.schema_fail}")
    print(f"udb_overlap:     {summary.udb_overlap}")
    print(f"class_counts:    {summary.class_counts}")
    fails = [r for r in summary.records if r.path and not r.schema_valid]
    if fails:
        print("--- validation failures (first 10) ---")
        for r in fails[:10]:
            print(f"  {r.name}: {r.validation_errors[:2]}")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Export parameters.csv rows to draft UDB param YAML (Artifact B)."
    )
    p.add_argument(
        "--csv",
        type=Path,
        default=REPO_ROOT / "data" / "parameters.csv",
        help="Path to Part I parameters.csv",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "drafts" / "param",
        help="Output directory for draft YAML files",
    )
    p.add_argument(
        "--mode",
        choices=("named", "new", "all"),
        default="named",
        help="named=named:yes only; new=not in UDB; all=both",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max drafts for mode=new (default: no limit for named; 20 for new if unset)",
    )
    p.add_argument(
        "--udb-root",
        type=Path,
        default=None,
        help="Path to riscv-unified-db checkout (for overlap + definedBy copy)",
    )
    p.add_argument(
        "--report",
        type=Path,
        default=REPO_ROOT / "results" / "export_b_report.json",
        help="JSON report path",
    )
    p.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing drafts/param/*.yaml before writing",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)

    mode: Mode = args.mode
    limit = args.limit
    if mode == "new" and limit is None:
        limit = 20  # plan: 10–20 new drafts

    udb_root = args.udb_root
    if udb_root is not None:
        udb_root = udb_root.resolve()
        if not udb_root.is_dir():
            print(f"error: --udb-root not a directory: {udb_root}", file=sys.stderr)
            return 2

    if not args.csv.is_file():
        print(f"error: CSV not found: {args.csv}", file=sys.stderr)
        return 2

    summary = export(
        csv_path=args.csv.resolve(),
        out_dir=args.out.resolve(),
        mode=mode,
        udb_root=udb_root,
        limit=limit,
        clean=args.clean,
    )
    write_report(summary, args.report.resolve())
    print_human_summary(summary)
    print(f"report: {args.report}")

    return 0 if summary.schema_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
