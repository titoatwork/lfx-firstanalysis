# Copyright (c) 2026 titoatwork
# SPDX-License-Identifier: BSD-3-Clause-Clear

"""Group UnifiedDB's array-valued parameters by schema shape, then read the gold's labels off each group.

`taxonomy.md` defines NORM_CSR_WARL as the case where "the parameter IS the set of
legal values" (taxonomy.md:43). That is a claim about the parameter's *shape*: a set.
UnifiedDB already states the shape, in the JSON schema on every parameter. So the
class is checkable without running a model and without inspecting the IDL at all.

This is a second, independent route to the question `audit_gold_classification.py`
asks. That script asks how the IDL *consumes* a parameter. This one asks what the
parameter *is*. Two routes that disagree would mean one of them is wrong; two routes
that agree on the same outliers is the evidence.

Only array-typed parameters can satisfy "IS the set of legal values", so the scan is
exhaustive over those and reports the total it drew from. Three shapes appear:

  set_enum     array + enumerated items + bounded + uniqueItems
               a set of legal values drawn from a named domain
  set_integer  array + integer items
               a set of legal values drawn from an integer range
  bitmask      array + boolean items + minItems == maxItems
               one flag per bit position, so it says which bits are writable,
               not which values are legal. NOT a legal-value set.

The bitmask/set distinction is the one a name or a keyword cannot make: every one of
these is "an array of things attached to a CSR field". Only `items` separates them.

Run from riscv-param-extraction/:
    python scripts/audit_param_schema_shapes.py [--udb PATH] [--gold PATH] [--json]

Exits non-zero only if the audit cannot run. A disagreement is data, not a failure.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Same helper the gold audit uses, imported rather than copied so the two audits
# cannot drift into recording provenance differently.
from audit_gold_classification import udb_revision  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    print("error: PyYAML required. The point of this script is to read the schema "
          "as the toolchain reads it, so a regex fallback is deliberately absent.",
          file=sys.stderr)
    raise SystemExit(2)

LEGAL_VALUE_CLASS = "NORM_CSR_WARL"


def param_files(udb: str) -> list[str]:
    return sorted(glob.glob(os.path.join(udb, "spec", "std", "isa", "param", "*.yaml")))


def shape_of(schema: dict) -> str | None:
    """Classify an array schema, or None if it is not an array."""
    if not isinstance(schema, dict) or schema.get("type") != "array":
        return None

    items = schema.get("items")
    bounded = "minItems" in schema or "maxItems" in schema
    fixed = schema.get("minItems") is not None and schema.get("minItems") == schema.get("maxItems")

    # `items` may be a list (tuple validation). COUNTINHIBIT_EN does this to pin
    # index 1 to a constant, and it is still a per-bit mask.
    if isinstance(items, list):
        kinds = {i.get("type") for i in items if isinstance(i, dict)}
        extra = schema.get("additionalItems")
        if isinstance(extra, dict):
            kinds.add(extra.get("type"))
        if kinds <= {"boolean", None} and "boolean" in kinds and fixed:
            return "bitmask"
        return "array_other"

    if not isinstance(items, dict):
        return "array_other"

    if items.get("enum") is not None and bounded and schema.get("uniqueItems") is True:
        return "set_enum"
    if items.get("type") == "boolean" and fixed:
        return "bitmask"
    if items.get("type") == "integer":
        return "set_integer"
    return "array_other"


def load_gold(path: str) -> dict[str, dict]:
    with open(path, encoding="utf-8") as fh:
        return {p["name"]: p for p in json.load(fh)["parameters"]}


def gold_digest(path: str) -> str:
    """Digest the parsed gold, not the bytes. See audit_gold_classification.py."""
    with open(path, encoding="utf-8") as fh:
        canon = json.dumps(json.load(fh), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def audit(udb: str, gold_path: str) -> dict:
    gold = load_gold(gold_path)
    files = param_files(udb)

    groups: dict[str, list[dict]] = {}
    for path in files:
        name = os.path.basename(path)[:-5]
        try:
            with open(path, encoding="utf-8") as fh:
                doc = yaml.safe_load(fh) or {}
        except (OSError, yaml.YAMLError):
            continue
        shape = shape_of(doc.get("schema"))
        if shape is None:
            continue
        entry = gold.get(name)
        groups.setdefault(shape, []).append({
            "name": name,
            "gold": entry.get("classification") if entry else None,
            "confidence": entry.get("classification_confidence") if entry else None,
        })

    summary = {}
    for shape, rows in groups.items():
        labels: dict[str, int] = {}
        for r in rows:
            key = r["gold"] or "not_in_gold"
            labels[key] = labels.get(key, 0) + 1
        scored = [r for r in rows if r["gold"] is not None]
        # A shape is "consistent" when every gold-labelled member of it got the
        # same class. That is the whole test: same shape, same label, or not.
        summary[shape] = {
            "total": len(rows),
            "in_gold": len(scored),
            "labels": dict(sorted(labels.items())),
            "consistent": len({r["gold"] for r in scored}) <= 1,
        }

    return {
        "provenance": {
            "gold_path": gold_path,
            "gold_canonical_sha256": gold_digest(gold_path),
            "udb_param_files": len(files),
            # Added 2026-08-05. Without this the audit reported a parameter
            # count with no way to say which tree produced it, and the gold it
            # scores against comes from `.udb-corpus`, a fork ~300 commits
            # behind main. Two numbers from two different UDB states are not
            # comparable, and a reader cannot tell without the revision.
            "udb": udb_revision(udb),
        },
        "params_scanned": len(files),
        "array_params": sum(len(v) for v in groups.values()),
        "groups": {k: sorted(v, key=lambda r: r["name"]) for k, v in sorted(groups.items())},
        "summary": dict(sorted(summary.items())),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--udb", default="../riscv-unified-db")
    ap.add_argument("--gold", default="../.udb-corpus/param_extraction/data/ground_truth.json")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.udb):
        print(f"error: --udb path not found: {args.udb}", file=sys.stderr)
        return 2
    if not os.path.isfile(args.gold):
        print(f"error: --gold path not found: {args.gold}", file=sys.stderr)
        return 2

    r = audit(args.udb, args.gold)
    if args.json:
        print(json.dumps(r, indent=2))
        return 0

    print(f"parameters scanned        : {r['params_scanned']}")
    print(f"array-valued parameters   : {r['array_params']}")
    print()
    for shape, s in r["summary"].items():
        verdict = "consistent" if s["consistent"] else "SPLIT LABEL ON ONE SHAPE"
        print(f"{shape:14} {s['total']:3} params, {s['in_gold']:3} in gold   {verdict}")
        for label, n in s["labels"].items():
            print(f"                 {n:3}  {label}")
        for row in r["groups"][shape]:
            tag = row["gold"] or "not in gold"
            print(f"                   {row['name']:26} {tag}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
