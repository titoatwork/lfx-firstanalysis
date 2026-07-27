#!/usr/bin/env python3
"""
Sweep UDB param + schema trees for structural invariant defects.

Machine-found candidates for human review before any filing.
Does NOT open issues/PRs. Does NOT call the GitHub API.

Usage:
  python workflow_slice/scripts/sweep_invariants.py
  python workflow_slice/scripts/sweep_invariants.py --udb-root ../riscv-unified-db
  python workflow_slice/scripts/sweep_invariants.py --json-out workflow_slice/findings/sweep.json

Exit codes:
  0 — sweep completed; no high-severity filable candidates
  1 — sweep completed; >=1 high-severity candidate (still success as a tool)
  2 — configuration / path / parse failure
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

# json used throughout; keep import at module top

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PKG = Path(__file__).resolve().parents[2]  # riscv-param-extraction
DEFAULT_UDB = PKG.parent / "riscv-unified-db"

SEVERITY_HIGH = "high"
SEVERITY_MED = "medium"
SEVERITY_LOW = "low"
SEVERITY_CENSUS = "census"  # never auto-file as N PRs


@dataclass
class Finding:
    class_id: str
    severity: str
    title: str
    detail: str
    paths: list[str] = field(default_factory=list)
    filable: bool = False  # high + small + regression-shaped
    notes: str = ""


def power_of_two(n: int) -> bool:
    return isinstance(n, int) and n > 0 and (n & (n - 1)) == 0


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def schema_bounds(schema: dict | None) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    out: dict[str, Any] = {}
    for k in ("type", "minimum", "maximum", "enum", "const", "minItems", "maxItems"):
        if k in schema:
            out[k] = schema[k]
    # items for array-of-enum
    if "items" in schema and isinstance(schema["items"], dict):
        out["items"] = {
            k: schema["items"][k]
            for k in ("type", "enum", "minimum", "maximum")
            if k in schema["items"]
        }
    return out


def walk_enums(obj: Any, path: str = "") -> list[tuple[str, list[Any]]]:
    """Collect all enum arrays in a JSON-like structure."""
    found: list[tuple[str, list[Any]]] = []
    if isinstance(obj, dict):
        if "enum" in obj and isinstance(obj["enum"], list):
            found.append((path or "<root>", obj["enum"]))
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            found.extend(walk_enums(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found.extend(walk_enums(v, f"{path}[{i}]"))
    return found


def is_pow2_context(path: str, description: str | None) -> bool:
    blob = f"{path} {(description or '')}".lower()
    keys = (
        "pow2",
        "power of 2",
        "power-of-two",
        "power of two",
        "unsigned_pow2",
        "alignment",
    )
    return any(k in blob for k in keys)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_pow2_schema_enums(schemas_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    schema_defs = schemas_dir / "schema_defs.json"
    if not schema_defs.is_file():
        return [
            Finding(
                "POW2_ENUM",
                SEVERITY_HIGH,
                "schema_defs.json missing",
                f"expected {schema_defs}",
                [str(schema_defs)],
                filable=False,
            )
        ]

    doc = json.loads(schema_defs.read_text(encoding="utf-8"))
    # $defs and nested
    for enum_path, values in walk_enums(doc):
        # only flag integer-ish non-pow2 when context is pow2
        desc = None
        # try to attach description from parent def name
        if "unsigned_pow2" in enum_path or "pow2" in enum_path.lower():
            non = [
                v
                for v in values
                if isinstance(v, int) and not power_of_two(v)
            ]
            missing_4096 = 4096 not in values and 4095 in values
            if non or missing_4096:
                # 4095 is the defect already reported as #2137 and fixed by #2138.
                # Report it so the sweep stays honest about upstream state, but do
                # not present it as something new to file.
                only_4095 = set(non) <= {4095}
                findings.append(
                    Finding(
                        class_id="POW2_ENUM",
                        severity=SEVERITY_MED if only_4095 else SEVERITY_HIGH,
                        title=f"Non-power-of-two values in {enum_path}",
                        detail=(
                            f"non_pow2={non}; has4095={4095 in values}; "
                            f"has4096={4096 in values}; n={len(values)}"
                        ),
                        paths=[str(schema_defs)],
                        filable=not only_4095,
                        notes=(
                            "Already reported as riscv-unified-db#2137 and fixed by #2138"
                            if only_4095
                            else "New non-power-of-two value; verify before filing"
                        ),
                    )
                )
        elif is_pow2_context(enum_path, desc):
            non = [v for v in values if isinstance(v, int) and v > 0 and not power_of_two(v)]
            if non:
                findings.append(
                    Finding(
                        class_id="POW2_ENUM",
                        severity=SEVERITY_MED,
                        title=f"Possible non-pow2 in pow2-ish enum {enum_path}",
                        detail=f"non_pow2={non}",
                        paths=[str(schema_defs)],
                        filable=bool(non),
                    )
                )

    # Also scan all schema JSON files for enum + "power of 2" description nearby
    for path in sorted(schemas_dir.glob("*.json")):
        if path.name == "schema_defs.json":
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for enum_path, values in walk_enums(doc):
            if not is_pow2_context(enum_path, path.name):
                continue
            non = [v for v in values if isinstance(v, int) and v > 0 and not power_of_two(v)]
            if non:
                findings.append(
                    Finding(
                        class_id="POW2_ENUM",
                        severity=SEVERITY_MED,
                        title=f"{path.name}:{enum_path} non-pow2 values",
                        detail=f"non_pow2={non}",
                        paths=[str(path)],
                        filable=True,
                    )
                )
    return findings


def check_pow2_param_inline_enums(param_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(param_dir.glob("*.yaml")):
        try:
            doc = load_yaml(path)
        except Exception as exc:  # noqa: BLE001
            findings.append(
                Finding(
                    "PARSE",
                    SEVERITY_MED,
                    f"YAML parse failure {path.name}",
                    str(exc),
                    [str(path)],
                    filable=False,
                )
            )
            continue
        if not isinstance(doc, dict):
            continue
        schema = doc.get("schema") or {}
        desc = " ".join(
            str(x)
            for x in (
                schema.get("description") if isinstance(schema, dict) else "",
                doc.get("description"),
                doc.get("long_name"),
                path.stem,
            )
            if x
        )
        if not is_pow2_context(path.stem, desc):
            continue
        enums = walk_enums(schema)
        for ep, values in enums:
            non = [v for v in values if isinstance(v, int) and v > 0 and not power_of_two(v)]
            if non:
                findings.append(
                    Finding(
                        class_id="POW2_PARAM_ENUM",
                        severity=SEVERITY_HIGH,
                        title=f"{path.stem}: non-pow2 in alignment/pow2 enum",
                        detail=f"{ep}: {non}",
                        paths=[str(path)],
                        filable=True,
                        notes="MTVEC class; #2090 fixed param YAMLs — flag only if still present on main",
                    )
                )
    return findings


def privilege_twin_groups(names: list[str]) -> dict[str, list[tuple[str, str]]]:
    """Group params by stripping leading M/S/VS/H/U privilege tags."""
    groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
    # Prefer longest prefix first
    for n in names:
        m = re.match(r"^(VS|M|S|H|U)_(.+)$", n)
        if m:
            groups[m.group(2)].append((m.group(1), n))
            continue
        m = re.match(r"^(VS|M|S|H|U)(.+)$", n)
        if m and m.group(2) and m.group(2)[0].isupper():
            groups[m.group(2)].append((m.group(1), n))
    return {k: v for k, v in groups.items() if len(v) > 1}


def check_twin_divergence(param_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    docs: dict[str, dict] = {}
    for path in param_dir.glob("*.yaml"):
        try:
            doc = load_yaml(path)
        except Exception:
            continue
        if isinstance(doc, dict) and doc.get("name"):
            docs[doc["name"]] = doc
        else:
            docs[path.stem] = doc if isinstance(doc, dict) else {}

    groups = privilege_twin_groups(list(docs.keys()))
    # Focus on well-known high-value twin families
    priority_suffixes = {
        "TVAL_WIDTH",
        "TVEC_MODES",
        "TVEC_BASE_ALIGNMENT_DIRECT",
        "TVEC_BASE_ALIGNMENT_VECTORED",
        "XLEN",
        "COUNTENABLE_EN",
        "CONTEXT_AVAILABLE",
        "_MODE_ENDIANNESS",
        "MODE_ENDIANNESS",
    }

    for suffix, members in sorted(groups.items()):
        bounds_map: dict[str, dict] = {}
        for pref, name in members:
            sch = schema_bounds((docs.get(name) or {}).get("schema"))
            bounds_map[name] = sch

        # Compare pairwise when same type
        names = [n for _, n in members]
        # Only compare M vs S, S vs VS, M vs VS when all present
        interesting = False
        for s in priority_suffixes:
            if suffix == s or suffix.endswith(s) or s in suffix:
                interesting = True
                break
        # Always check TVAL_WIDTH / TVEC / XLEN style
        if re.search(r"TVAL|TVEC|XLEN|COUNTENABLE|ENDIAN|CONTEXT_AVAILABLE|STATEEN", suffix):
            interesting = True
        if not interesting:
            continue

        # Pick a reference: prefer M* then S*
        ref_name = None
        for cand in names:
            if cand.startswith("M") and not cand.startswith("VS"):
                ref_name = cand
                break
        if ref_name is None:
            ref_name = names[0]
        ref = bounds_map[ref_name]

        for name in names:
            if name == ref_name:
                continue
            other = bounds_map[name]
            # skip empty
            if not ref and not other:
                continue
            diffs = []
            for k in set(ref) | set(other):
                if ref.get(k) != other.get(k):
                    diffs.append(f"{k}: {ref_name}={ref.get(k)!r} vs {name}={other.get(k)!r}")
            if diffs:
                # Two reasons a real divergence is still not worth filing:
                # already fixed upstream, or reviewed and found architecturally
                # correct. Both are reported, neither is filable.
                known = ""
                pair = {ref_name, name}
                if pair == {"MTVAL_WIDTH", "STVAL_WIDTH"}:
                    known = "Already covered by open PR #2103"
                elif ref_name == "MXLEN" and name in ("SXLEN", "UXLEN", "VSXLEN"):
                    # Verified against the ISA, not a defect: MXLEN is fixed for a
                    # hart, so it is a scalar. SXLEN/UXLEN/VSXLEN describe the *set*
                    # of supported widths and are runtime-switchable via
                    # mstatus.SXL, mstatus.UXL and hstatus.VSXL, so they are arrays.
                    known = (
                        "NOT A DEFECT (reviewed): MXLEN is fixed per hart and scalar; "
                        f"{name} is a runtime-switchable set. See riscv-unified-db#2145."
                    )
                severity = SEVERITY_HIGH if known == "" else SEVERITY_MED
                filable = known == ""
                # enum-only cosmetic differences on huge pow2 lists may be ok
                findings.append(
                    Finding(
                        class_id="TWIN_BOUNDS",
                        severity=severity,
                        title=f"Twin schema divergence: {ref_name} vs {name}",
                        detail="; ".join(diffs)[:800],
                        paths=[
                            str(param_dir / f"{ref_name}.yaml"),
                            str(param_dir / f"{name}.yaml"),
                        ],
                        filable=filable,
                        notes=known
                        or "Generalizes STVAL/MTVAL class; verify ISA before filing",
                    )
                )
    return findings


def check_required_field_census(param_dir: Path) -> list[Finding]:
    """Census only — never emit N filable PRs for long_name TODO."""
    required = ["$schema", "kind", "description", "long_name", "definedBy", "schema"]
    missing_counts: Counter[str] = Counter()
    todo_long = 0
    todo_examples: list[str] = []
    missing_name = 0
    total = 0
    parse_fail = 0

    for path in sorted(param_dir.glob("*.yaml")):
        total += 1
        try:
            doc = load_yaml(path)
        except Exception:
            parse_fail += 1
            continue
        if not isinstance(doc, dict):
            parse_fail += 1
            continue
        for key in required:
            if key not in doc or doc[key] in (None, ""):
                missing_counts[key] += 1
        # name recommended though not always required by schema
        if "name" not in doc:
            missing_name += 1
        ln = doc.get("long_name")
        if isinstance(ln, str) and ln.strip() == "TODO":
            todo_long += 1
            if len(todo_examples) < 8:
                todo_examples.append(path.stem)
        elif isinstance(ln, str) and "TODO" in ln:
            todo_long += 1

    detail = (
        f"total_params={total}; parse_fail={parse_fail}; "
        f"missing_counts={dict(missing_counts)}; "
        f"missing_name_key={missing_name}; "
        f"long_name_TODO={todo_long}; examples={todo_examples}"
    )
    return [
        Finding(
            class_id="REQUIRED_FIELDS_CENSUS",
            severity=SEVERITY_CENSUS,
            title="Param required-field / long_name TODO census (do not bulk-PR)",
            detail=detail,
            paths=[str(param_dir)],
            filable=False,
            notes=(
                "If maintainers want a systematic fix: one issue with breakdown, "
                "not N long_name PRs; prefer one issue carrying the full census."
            ),
        )
    ]


def check_duplicate_enum_values(param_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(param_dir.glob("*.yaml")):
        try:
            doc = load_yaml(path)
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        for ep, values in walk_enums(doc.get("schema") or {}):
            # only care about hashable scalars
            scalars = [v for v in values if isinstance(v, (int, str, bool))]
            c = Counter(scalars)
            dups = [v for v, n in c.items() if n > 1]
            if dups:
                findings.append(
                    Finding(
                        class_id="DUP_ENUM",
                        severity=SEVERITY_HIGH,
                        title=f"{path.stem}: duplicate enum entries",
                        detail=f"{ep}: duplicates={dups}",
                        paths=[str(path)],
                        filable=True,
                    )
                )

        # definedBy anyOf / allOf duplicate extension names
        def collect_ext_names(node: Any, acc: list[str]) -> None:
            if isinstance(node, dict):
                if "extension" in node and isinstance(node["extension"], dict):
                    n = node["extension"].get("name")
                    if isinstance(n, str):
                        acc.append(n)
                if "name" in node and "extension" not in node and isinstance(node.get("name"), str):
                    # sometimes {name: X} under anyOf of extensions
                    pass
                for v in node.values():
                    collect_ext_names(v, acc)
            elif isinstance(node, list):
                for v in node:
                    collect_ext_names(v, acc)

        # HPM-style: list of indexes in definedBy
        def collect_indexes(node: Any, acc: list[Any]) -> None:
            if isinstance(node, dict):
                if "index" in node:
                    acc.append(node["index"])
                if "indexes" in node and isinstance(node["indexes"], list):
                    acc.extend(node["indexes"])
                for v in node.values():
                    collect_indexes(v, acc)
            elif isinstance(node, list):
                for v in node:
                    collect_indexes(v, acc)

        db = doc.get("definedBy")
        idxs: list[Any] = []
        collect_indexes(db, idxs)
        if idxs:
            c = Counter(idxs)
            dups = [i for i, n in c.items() if n > 1]
            if dups:
                note = ""
                if path.stem in ("HPM_EVENTS", "HPM_COUNTER_EN"):
                    note = "KNOWN class: #2046/#1991 — verify still present before filing"
                findings.append(
                    Finding(
                        class_id="DUP_INDEX",
                        severity=SEVERITY_HIGH if not note else SEVERITY_MED,
                        title=f"{path.stem}: duplicate index in definedBy",
                        detail=f"duplicates={dups}",
                        paths=[str(path)],
                        filable=not bool(note),
                        notes=note,
                    )
                )

        exts: list[str] = []
        collect_ext_names(db, exts)
        if exts:
            c = Counter(exts)
            # only flag if same name appears twice under anyOf siblings — weak signal
            dups = [e for e, n in c.items() if n > 1]
            if dups and path.stem.startswith("HPM"):
                findings.append(
                    Finding(
                        class_id="DUP_EXT_REF",
                        severity=SEVERITY_MED,
                        title=f"{path.stem}: repeated extension name in definedBy tree",
                        detail=f"duplicates={dups}",
                        paths=[str(path)],
                        filable=False,
                        notes="May be intentional allOf; manual review",
                    )
                )
    return findings


def check_definedby_shape(param_dir: Path) -> list[Finding]:
    """Red-flag definedBy that is empty, non-mapping, or obviously incomplete."""
    findings: list[Finding] = []
    for path in sorted(param_dir.glob("*.yaml")):
        try:
            doc = load_yaml(path)
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        db = doc.get("definedBy")
        if db is None:
            findings.append(
                Finding(
                    class_id="DEFINEDBY_MISSING",
                    severity=SEVERITY_HIGH,
                    title=f"{path.stem}: missing definedBy",
                    detail="required by param_schema",
                    paths=[str(path)],
                    filable=True,
                )
            )
            continue
        if not isinstance(db, dict):
            findings.append(
                Finding(
                    class_id="DEFINEDBY_SHAPE",
                    severity=SEVERITY_HIGH,
                    title=f"{path.stem}: definedBy is not a mapping",
                    detail=f"type={type(db).__name__}",
                    paths=[str(path)],
                    filable=True,
                )
            )
            continue
        # empty
        if not db:
            findings.append(
                Finding(
                    class_id="DEFINEDBY_EMPTY",
                    severity=SEVERITY_HIGH,
                    title=f"{path.stem}: empty definedBy",
                    detail="",
                    paths=[str(path)],
                    filable=True,
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def resolve_udb(root: Path | None) -> Path:
    if root is not None:
        return root.resolve()
    env_raw = (__import__("os").environ.get("UDB_ROOT") or "").strip()
    if env_raw:
        env = Path(env_raw)
        if env.is_dir():
            return env.resolve()
    if DEFAULT_UDB.is_dir():
        return DEFAULT_UDB.resolve()
    raise SystemExit(2)


def materialize_git_ref(udb: Path, ref: str) -> Path:
    """Export param + schemas trees from a git ref into a temp directory."""
    import shutil
    import subprocess
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="udb_sweep_"))
    for sub in ("spec/schemas", "spec/std/isa/param"):
        # list files via git ls-tree
        try:
            out = subprocess.check_output(
                ["git", "-C", str(udb), "ls-tree", "-r", "--name-only", ref, sub],
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            shutil.rmtree(tmp, ignore_errors=True)
            raise SystemExit(f"git ls-tree failed for {ref}:{sub}: {exc}") from exc
        for rel in out.splitlines():
            rel = rel.strip()
            if not rel:
                continue
            dest = tmp / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            blob = subprocess.check_output(
                ["git", "-C", str(udb), "show", f"{ref}:{rel}"]
            )
            dest.write_bytes(blob)
    return tmp


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--udb-root", type=Path, default=None)
    ap.add_argument(
        "--git-ref",
        default=None,
        help="Read params/schemas from this git ref (e.g. origin/main) instead of worktree",
    )
    ap.add_argument(
        "--json-out",
        type=Path,
        default=PKG / "workflow_slice" / "findings" / "sweep_invariants.json",
    )
    ap.add_argument(
        "--md-out",
        type=Path,
        default=PKG / "workflow_slice" / "findings" / "SWEEP_FINDINGS.md",
    )
    args = ap.parse_args(argv)

    try:
        udb = resolve_udb(args.udb_root)
    except SystemExit:
        print("ERROR: cannot find UDB root; pass --udb-root", file=sys.stderr)
        return 2

    cleanup: Path | None = None
    if args.git_ref:
        try:
            cleanup = materialize_git_ref(udb, args.git_ref)
            tree = cleanup
            source_label = f"{udb}@{args.git_ref}"
        except SystemExit as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    else:
        tree = udb
        source_label = str(udb)

    param_dir = tree / "spec" / "std" / "isa" / "param"
    schemas_dir = tree / "spec" / "schemas"
    if not param_dir.is_dir() or not schemas_dir.is_dir():
        print(f"ERROR: bad UDB tree under {tree}", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    findings.extend(check_pow2_schema_enums(schemas_dir))
    findings.extend(check_pow2_param_inline_enums(param_dir))
    findings.extend(check_twin_divergence(param_dir))
    findings.extend(check_required_field_census(param_dir))
    findings.extend(check_duplicate_enum_values(param_dir))
    findings.extend(check_definedby_shape(param_dir))

    # Dedup by title+class
    seen: set[str] = set()
    unique: list[Finding] = []
    for f in findings:
        key = f"{f.class_id}|{f.title}|{f.detail[:120]}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)
    findings = unique

    high = [f for f in findings if f.severity == SEVERITY_HIGH]
    filable = [f for f in findings if f.filable]
    census = [f for f in findings if f.severity == SEVERITY_CENSUS]

    # Write outputs
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "udb_root": str(udb),
        "source": source_label,
        "git_ref": args.git_ref,
        "param_count": len(list(param_dir.glob("*.yaml"))),
        "finding_count": len(findings),
        "high_count": len(high),
        "filable_count": len(filable),
        "findings": [asdict(f) for f in findings],
    }
    args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Sweep findings: candidates for human triage",
        "",
        f"- UDB root: `{udb}`",
        f"- Source: `{source_label}`",
        f"- Param YAML count: **{payload['param_count']}**",
        f"- Findings: **{len(findings)}** (high={len(high)}, filable={len(filable)})",
        "",
        "## Discipline",
        "",
        "Before filing any issue/PR, clear all four:",
        "1. Reproduces on current `origin/main`",
        "2. No existing PR touches it",
        "3. No open issue claim / \"I am working on this\"",
        "4. Small fix + regression test in `tools/ruby-gems/udb/test/run.rb`",
        "",
        "**Do not** bulk-file `long_name: TODO` (census only below).",
        "",
        "## Filable / high / medium candidates",
        "",
    ]
    for f in findings:
        if f.severity == SEVERITY_CENSUS:
            continue
        lines.append(f"### [{f.severity}] {f.class_id}: {f.title}")
        lines.append("")
        lines.append(f"- filable: **{f.filable}**")
        lines.append(f"- detail: {f.detail}")
        if f.notes:
            lines.append(f"- notes: {f.notes}")
        for p in f.paths:
            lines.append(f"- path: `{p}`")
        lines.append("")

    lines.append("## Census (not filable as N PRs)")
    lines.append("")
    for f in census:
        lines.append(f"- **{f.title}**: {f.detail}")
        lines.append(f"  - {f.notes}")
    lines.append("")
    lines.append("## All findings (compact)")
    lines.append("")
    lines.append("| severity | class | filable | title |")
    lines.append("|----------|-------|---------|-------|")
    for f in findings:
        title = f.title.replace("|", "/")
        lines.append(
            f"| {f.severity} | {f.class_id} | {f.filable} | {title} |"
        )
    lines.append("")
    lines.append(f"Machine JSON: `{args.json_out}`")
    args.md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"UDB: {source_label}")
    print(f"params: {payload['param_count']}")
    print(f"findings: {len(findings)} high={len(high)} filable={len(filable)}")
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print()
    for f in findings:
        if f.severity == SEVERITY_CENSUS:
            continue
        print(f"[{f.severity}] filable={f.filable} {f.class_id}: {f.title}")
        print(f"  {f.detail[:220]}")
        if f.notes:
            print(f"  note: {f.notes}")
    for f in census:
        print(f"[census] {f.detail[:240]}")

    if cleanup is not None:
        import shutil

        shutil.rmtree(cleanup, ignore_errors=True)

    return 1 if high or filable else 0


if __name__ == "__main__":
    raise SystemExit(main())
