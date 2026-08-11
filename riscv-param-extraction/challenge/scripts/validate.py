#!/usr/bin/env python3
"""
Fail-closed challenge validator.

Checks:
  1. Each *.yaml param document validates against vendored UDB param_schema.json
  2. Sibling <NAME>.evidence.json exists with a quote found in the cited snippet
     (whitespace-normalized; optional tag-aware AsciiDoc strip mode)
  3. Optional WARN (or FAIL with --strict-triggers): optionality trigger near quote
     (relevance layer — does NOT require param name to appear in the source text)

Exit codes:
  0 — all checks passed (or --expect-fail and failures found)
  1 — validation failures
  2 — usage / environment error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from jsonschema import Draft7Validator
    from jsonschema.validators import RefResolver
except ImportError:  # pragma: no cover
    print("ERROR: jsonschema required. pip install jsonschema PyYAML", file=sys.stderr)
    sys.exit(2)

CHALLENGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = CHALLENGE_ROOT / "schema"
SNIPPETS_DIR = CHALLENGE_ROOT / "snippets"
PARAM_NAME_RE = re.compile(r"^[A-Z][A-Z_0-9]*$")
TRIGGER_RE = re.compile(
    r"\b(may|might|should|optional(?:ly)?|"
    r"implementation-defined|implementation-specific)\b",
    re.I,
)
DEFAULT_TRIGGER_WINDOW = 200


def _ws_norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _strip_asciidoc_markup(s: str) -> str:
    """Best-effort strip of common AsciiDoc inline noise for tag-aware grounding."""
    out = s
    # [#norm:...]#...# wrappers (non-greedy inner)
    out = re.sub(r"\[#[^\]]+\]#([^#]*)#", r"\1", out)
    # _italics_ and *bold*
    out = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", out)
    out = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"\1", out)
    # `monospace`
    out = re.sub(r"`([^`]+)`", r"\1", out)
    # <<xrefs>>
    out = re.sub(r"<<[^>]+>>", "", out)
    return out


def _load_schema_store() -> tuple[dict[str, Any], dict[str, Any]]:
    store: dict[str, Any] = {}
    for path in SCHEMA_DIR.glob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        store[path.name] = doc
        store[f"{path.name}#"] = doc
        sid = doc.get("$id")
        if isinstance(sid, str):
            store[sid] = doc
    schema = json.loads((SCHEMA_DIR / "param_schema.json").read_text(encoding="utf-8"))
    return schema, store


def validate_schema(doc: dict[str, Any], schema: dict[str, Any], store: dict[str, Any]) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft7Validator(schema, resolver=resolver)
    errors: list[str] = []
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"{loc}: {err.message}")
    return errors


def quote_in_source(quote: str, source: str, mode: str) -> bool:
    q = _ws_norm(quote)
    if not q:
        return False
    if mode == "naive":
        return q in _ws_norm(source)
    # tag-aware: compare with markup stripped on both sides
    return _ws_norm(_strip_asciidoc_markup(q)) in _ws_norm(_strip_asciidoc_markup(source))


def trigger_near_quote(source: str, quote: str, window: int = DEFAULT_TRIGGER_WINDOW) -> bool:
    """True if an optionality trigger appears within ±window chars of the quote."""
    if not quote or quote not in source:
        # fall back to whitespace-normalized search
        sn, qn = _ws_norm(source), _ws_norm(quote)
        pos = sn.find(qn)
        if pos < 0:
            return False
        lo = max(0, pos - window)
        hi = min(len(sn), pos + len(qn) + window)
        return TRIGGER_RE.search(sn[lo:hi]) is not None
    pos = source.find(quote)
    lo = max(0, pos - window)
    hi = min(len(source), pos + len(quote) + window)
    return TRIGGER_RE.search(source[lo:hi]) is not None


def check_param_file(
    yaml_path: Path,
    schema: dict[str, Any],
    store: dict[str, Any],
    grounding_mode: str,
    *,
    check_triggers: bool = False,
    strict_triggers: bool = False,
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    try:
        doc = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"parse: {exc}"], warnings

    if not isinstance(doc, dict):
        return ["document is not a mapping"], warnings

    errors.extend(validate_schema(doc, schema, store))

    name = doc.get("name")
    if not isinstance(name, str) or not PARAM_NAME_RE.match(name):
        errors.append(f"name: must match {PARAM_NAME_RE.pattern} (got {name!r})")

    # <stem>.evidence.json next to <stem>.yaml
    evidence_file = yaml_path.parent / f"{yaml_path.stem}.evidence.json"
    if not evidence_file.is_file():
        errors.append(f"missing evidence file: {evidence_file.name}")
        return errors, warnings

    try:
        evidence = json.loads(evidence_file.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"evidence parse: {exc}")
        return errors, warnings

    quote = evidence.get("quote")
    snippet_name = evidence.get("snippet")
    if not isinstance(quote, str) or not quote.strip():
        errors.append("evidence.quote missing or empty")
    if not isinstance(snippet_name, str) or not snippet_name.strip():
        errors.append("evidence.snippet missing or empty")
        return errors, warnings

    snippet_path = SNIPPETS_DIR / snippet_name
    if not snippet_path.is_file():
        alt = CHALLENGE_ROOT / snippet_name
        snippet_path = alt if alt.is_file() else snippet_path
    if not snippet_path.is_file():
        errors.append(f"snippet not found: {snippet_name}")
        return errors, warnings

    source = snippet_path.read_text(encoding="utf-8")
    if isinstance(quote, str) and not quote_in_source(quote, source, grounding_mode):
        errors.append(
            f"quote for {name!r} not found ({grounding_mode}) in {snippet_name} "
            f"(possible hallucination): {quote[:120]!r}..."
        )
    elif (
        check_triggers
        and isinstance(quote, str)
        and quote.strip()
        and not trigger_near_quote(source, quote)
    ):
        msg = (
            f"no optionality trigger within ±{DEFAULT_TRIGGER_WINDOW} chars of quote "
            f"for {name!r} (possible mis-attribution; human review)"
        )
        if strict_triggers:
            errors.append(msg)
        else:
            warnings.append(msg)

    if isinstance(name, str) and evidence.get("name") not in (None, name):
        errors.append(f"evidence.name {evidence.get('name')!r} != yaml name {name!r}")

    return errors, warnings


def iter_yaml_params(results_dir: Path) -> list[Path]:
    return sorted(p for p in results_dir.rglob("*.yaml") if p.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed challenge validator")
    parser.add_argument(
        "--results",
        type=Path,
        required=True,
        help="Directory tree of param YAML + evidence JSON",
    )
    parser.add_argument(
        "--grounding",
        choices=("naive", "tag-aware"),
        default="naive",
        help="Grounding mode for quote checks (default: naive)",
    )
    parser.add_argument(
        "--expect-fail",
        action="store_true",
        help="Invert success: exit 0 only if at least one error is found (bad fixtures)",
    )
    parser.add_argument(
        "--check-triggers",
        action="store_true",
        help="Warn (or fail with --strict-triggers) if no optionality trigger near quote",
    )
    parser.add_argument(
        "--strict-triggers",
        action="store_true",
        help="Treat missing nearby optionality trigger as FAIL (implies --check-triggers)",
    )
    args = parser.parse_args(argv)
    check_triggers = args.check_triggers or args.strict_triggers

    results_dir = args.results
    if not results_dir.is_dir():
        print(f"ERROR: not a directory: {results_dir}", file=sys.stderr)
        return 2

    schema, store = _load_schema_store()
    yaml_files = iter_yaml_params(results_dir)
    if not yaml_files:
        print(f"ERROR: no .yaml files under {results_dir}", file=sys.stderr)
        return 2

    total_errors = 0
    total_warns = 0
    for path in yaml_files:
        errs, warns = check_param_file(
            path,
            schema,
            store,
            args.grounding,
            check_triggers=check_triggers,
            strict_triggers=args.strict_triggers,
        )
        total_errors += len(errs)
        total_warns += len(warns)
        if errs:
            print(f"[FAIL] {path}")
            for e in errs:
                print(f"    - {e}")
        else:
            print(f"[OK]   {path}")
        for w in warns:
            print(f"    ! WARN: {w}")

    print(
        f"\n{len(yaml_files)} file(s) checked, {total_errors} error(s), "
        f"{total_warns} warning(s) (grounding={args.grounding})"
    )

    if args.expect_fail:
        if total_errors > 0:
            print("expect-fail: failures observed (good)")
            return 0
        print("expect-fail: expected failures but none found", file=sys.stderr)
        return 1

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
