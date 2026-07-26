#!/usr/bin/env python3
"""One-off structural audit of UDB param YAMLs (local; not part of product CI)."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml


def find_dup_ext(obj, path, name, out):
    if isinstance(obj, list):
        names_seen = []
        for i, item in enumerate(obj):
            if isinstance(item, dict) and "name" in item:
                # extension-like dict
                if "extension" not in item:  # bare name entries inside allOf/anyOf
                    names_seen.append(item.get("name"))
            find_dup_ext(item, f"{path}[{i}]", name, out)
        c = Counter(n for n in names_seen if n)
        for n, cnt in c.items():
            if cnt > 1:
                out.append((name, n, cnt, path))
    elif isinstance(obj, dict):
        # definedBy.extension.allOf: [{name: X}, {name: X}]
        if "allOf" in obj and isinstance(obj["allOf"], list):
            names_seen = []
            for item in obj["allOf"]:
                if isinstance(item, dict) and "name" in item and "param" not in item:
                    names_seen.append(item.get("name"))
                elif isinstance(item, dict) and isinstance(item.get("extension"), dict):
                    names_seen.append(item["extension"].get("name"))
            c = Counter(n for n in names_seen if n)
            for n, cnt in c.items():
                if cnt > 1:
                    out.append((name, n, cnt, path + ".allOf"))
        if "anyOf" in obj and isinstance(obj["anyOf"], list):
            names_seen = []
            for item in obj["anyOf"]:
                if isinstance(item, dict) and "name" in item:
                    names_seen.append(item.get("name"))
                elif isinstance(item, dict) and isinstance(item.get("extension"), dict):
                    names_seen.append(item["extension"].get("name"))
            c = Counter(n for n in names_seen if n)
            for n, cnt in c.items():
                if cnt > 1:
                    out.append((name, n, cnt, path + ".anyOf"))
        for k, v in obj.items():
            find_dup_ext(v, f"{path}.{k}", name, out)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("spec/std/isa/param")
    files = sorted(root.glob("*.yaml"))
    print("param files", len(files))

    issues = []
    names: set[str] = set()
    schema_default_bad = []
    dup_definedby = []
    impossible_bounds = []
    twin_pairs = []

    docs = {}
    for f in files:
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            issues.append(("yaml_parse", f.name, str(e)))
            continue
        if not isinstance(doc, dict):
            issues.append(("not_map", f.name, ""))
            continue
        name = doc.get("name")
        if name in names:
            issues.append(("dup_name", f.name, name))
        if name:
            names.add(name)
            docs[name] = doc
        if name and name != f.stem:
            issues.append(("name_file_mismatch", f.name, str(name)))

        schema = doc.get("schema") or {}
        if isinstance(schema, dict) and "default" in schema:
            d = schema["default"]
            if "enum" in schema and d not in schema["enum"]:
                schema_default_bad.append((name, "default_not_in_enum", d, schema.get("enum")))
            if schema.get("type") == "integer":
                if "minimum" in schema and isinstance(d, int) and d < schema["minimum"]:
                    schema_default_bad.append((name, "default_lt_min", d, schema["minimum"]))
                if "maximum" in schema and isinstance(d, int) and d > schema["maximum"]:
                    schema_default_bad.append((name, "default_gt_max", d, schema["maximum"]))
            if schema.get("type") == "array" and isinstance(d, list):
                if "minItems" in schema and len(d) < schema["minItems"]:
                    schema_default_bad.append((name, "default_minItems", len(d), schema["minItems"]))
                if "maxItems" in schema and len(d) > schema["maxItems"]:
                    schema_default_bad.append((name, "default_maxItems", len(d), schema["maxItems"]))

        if isinstance(schema, dict):
            if "minimum" in schema and "maximum" in schema:
                try:
                    if schema["minimum"] > schema["maximum"]:
                        impossible_bounds.append((name, "min>max", schema["minimum"], schema["maximum"]))
                except TypeError:
                    pass
            if schema.get("enum") == []:
                issues.append(("empty_enum", name, ""))
            if "minItems" in schema and "maxItems" in schema:
                if schema["minItems"] > schema["maxItems"]:
                    impossible_bounds.append((name, "minItems>maxItems", schema["minItems"], schema["maxItems"]))

        db = doc.get("definedBy")
        if db is not None:
            find_dup_ext(db, "definedBy", name, dup_definedby)

    # Twin shape consistency: M_/S_/VS_ or MTVAL/STVAL/VSTVAL families
    families = [
        ("MTVAL_WIDTH", "STVAL_WIDTH", "VSTVAL_WIDTH"),
        ("REPORT_ENCODING_IN_MTVAL_ON_ILLEGAL_INSTRUCTION",
         "REPORT_ENCODING_IN_STVAL_ON_ILLEGAL_INSTRUCTION",
         "REPORT_ENCODING_IN_VSTVAL_ON_ILLEGAL_INSTRUCTION"),
        ("M_MODE_ENDIANNESS", "S_MODE_ENDIANNESS", "U_MODE_ENDIANNESS"),
        ("MTVEC_MODES", "STVEC_MODES", "VSTVEC_MODES"),
        ("ASID_WIDTH", "VMID_WIDTH"),
    ]
    for fam in families:
        present = [(n, docs[n]) for n in fam if n in docs]
        if len(present) < 2:
            continue
        shapes = []
        for n, d in present:
            sch = d.get("schema") or {}
            shapes.append((n, sch.get("type"), sch.get("minimum"), sch.get("maximum"), sch.get("enum")))
        # compare type + bounds
        base = shapes[0]
        for s in shapes[1:]:
            if s[1:] != base[1:]:
                twin_pairs.append((base, s))

    # Referenced param names in requirements text (light)
    ref_missing = []
    param_ref_re = __import__("re").compile(r"\b([A-Z][A-Z0-9_]{3,})\b")
    for name, doc in docs.items():
        blob = yaml.safe_dump(doc.get("requirements") or {}) + yaml.safe_dump(doc.get("definedBy") or {})
        for m in param_ref_re.findall(blob):
            if m in names or m in {
                "TRUE", "FALSE", "TODO", "IDL", "AND", "OR", "NOT", "WHEN", "THEN",
                "ALL", "ANY", "OF", "IF", "ELSE", "MXLEN", "SXLEN", "UXLEN",  # sometimes pseudo
            }:
                continue
            # only flag if looks like param and missing
            if m.endswith("_WIDTH") or m.endswith("_EN") or m.startswith("NUM_") or m.endswith("_IMPLEMENTED"):
                if m not in names and m not in {"XLEN", "ELEN", "VLEN"}:
                    ref_missing.append((name, m))

    print("\n=== schema default violations", len(schema_default_bad))
    for x in schema_default_bad[:40]:
        print(x)
    print("\n=== impossible bounds", len(impossible_bounds))
    for x in impossible_bounds[:20]:
        print(x)
    print("\n=== dup definedBy extension names", len(dup_definedby))
    for x in dup_definedby[:20]:
        print(x)
    print("\n=== twin shape mismatches", len(twin_pairs))
    for x in twin_pairs[:20]:
        print(x)
    print("\n=== possible missing param refs", len(ref_missing))
    for x in sorted(set(ref_missing))[:30]:
        print(x)
    print("\n=== other issues", len(issues))
    for x in issues[:30]:
        print(x)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
