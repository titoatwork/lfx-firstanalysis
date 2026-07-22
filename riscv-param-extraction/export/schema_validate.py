"""
Validate draft param YAML documents against UDB `param_schema.json`.

Uses a local copy of UDB schemas under export/schemas/ so this repo is
auditable without requiring the full UDB tree at validation time.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

try:
    from jsonschema import Draft7Validator
    from jsonschema.validators import RefResolver
except ImportError:  # pragma: no cover
    Draft7Validator = None  # type: ignore
    RefResolver = None  # type: ignore


SCHEMAS_DIR = Path(__file__).resolve().parent / "schemas"
PARAM_SCHEMA_PATH = SCHEMAS_DIR / "param_schema.json"


@dataclass
class ValidationResult:
    path: Path
    ok: bool
    errors: list[str] = field(default_factory=list)


def _load_store() -> dict[str, Any]:
    store: dict[str, Any] = {}
    for path in SCHEMAS_DIR.glob("*.json"):
        with path.open(encoding="utf-8") as f:
            doc = json.load(f)
        # Register under common $id / filename keys used by $ref.
        store[path.name] = doc
        store[f"{path.name}#"] = doc
        sid = doc.get("$id")
        if isinstance(sid, str):
            store[sid] = doc
    return store


def load_param_schema() -> dict[str, Any]:
    with PARAM_SCHEMA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def validate_param_dict(doc: dict[str, Any]) -> list[str]:
    """Return a list of validation error strings (empty if valid)."""
    if Draft7Validator is None or RefResolver is None:
        return [
            "jsonschema not installed; run: pip install jsonschema PyYAML"
        ]

    schema = load_param_schema()
    store = _load_store()
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft7Validator(schema, resolver=resolver)
    errors: list[str] = []
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"{loc}: {err.message}")
    return errors


def validate_yaml_file(path: Path) -> ValidationResult:
    try:
        raw = path.read_text(encoding="utf-8")
        doc = yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001 — report parse failures as validation
        return ValidationResult(path=path, ok=False, errors=[f"parse: {exc}"])

    if not isinstance(doc, dict):
        return ValidationResult(
            path=path, ok=False, errors=["document is not a YAML mapping"]
        )

    errors = validate_param_dict(doc)
    return ValidationResult(path=path, ok=not errors, errors=errors)


def validate_dir(directory: Path) -> list[ValidationResult]:
    paths = sorted(directory.glob("*.yaml"))
    return [validate_yaml_file(p) for p in paths]
