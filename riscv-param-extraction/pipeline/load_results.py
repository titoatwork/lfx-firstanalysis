"""Load Part I extraction outputs (merged or deduped) and UDB name sets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1, "": 0}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def deduplicate_params(params: list[dict]) -> list[dict]:
    """Keep highest-confidence instance per parameter_name (Part I style)."""
    by_name: dict[str, dict] = {}
    for p in params:
        name = p.get("parameter_name")
        if not name:
            continue
        prev = by_name.get(name)
        if prev is None:
            by_name[name] = p
            continue
        prev_rank = CONFIDENCE_RANK.get(str(prev.get("confidence", "")).lower(), 0)
        cur_rank = CONFIDENCE_RANK.get(str(p.get("confidence", "")).lower(), 0)
        if cur_rank > prev_rank:
            by_name[name] = p
    return [by_name[k] for k in sorted(by_name)]


def load_param_list(path: Path) -> list[dict]:
    """Load a unique parameter list from merged or deduped JSON.

    Accepted shapes:
    - deduped: ``{"parameters": [ ... ]}``
    - merged:  ``{"results": [ {"parameters": [ ... ]}, ... ]}``
    - bare list of param dicts
    """
    data = load_json(path)
    if isinstance(data, list):
        return deduplicate_params(data)
    if not isinstance(data, dict):
        raise ValueError(f"Unsupported result file shape: {path}")

    if "parameters" in data and isinstance(data["parameters"], list):
        # Already deduped (or single blob)
        params = data["parameters"]
        # If these already look unique, still re-dedupe for safety
        return deduplicate_params(params)

    if "results" in data and isinstance(data["results"], list):
        flat: list[dict] = []
        for result in data["results"]:
            if not isinstance(result, dict):
                continue
            if result.get("error"):
                continue
            flat.extend(result.get("parameters") or [])
        return deduplicate_params(flat)

    raise ValueError(
        f"No parameters/results list in {path}; keys={list(data.keys())[:12]}"
    )


def load_udb_names(path: Path) -> set[str]:
    """Load UDB parameter names from ground_truth.json or a plain JSON list/set file.

    ground_truth shape: ``{"parameters": [{"name": ...}, ...]}``
    """
    data = load_json(path)
    if isinstance(data, list):
        names: set[str] = set()
        for item in data:
            if isinstance(item, str):
                names.add(item)
            elif isinstance(item, dict) and item.get("name"):
                names.add(str(item["name"]))
            elif isinstance(item, dict) and item.get("parameter_name"):
                names.add(str(item["parameter_name"]))
        return names
    if isinstance(data, dict):
        if "parameters" in data:
            return {
                str(p["name"])
                for p in data["parameters"]
                if isinstance(p, dict) and p.get("name")
            }
        if "names" in data and isinstance(data["names"], list):
            return {str(n) for n in data["names"]}
    raise ValueError(f"Cannot parse UDB names from {path}")


def load_udb_names_from_yaml_dir(param_dir: Path) -> set[str]:
    """Names from ``spec/std/isa/param/*.yaml`` stems."""
    if not param_dir.is_dir():
        raise FileNotFoundError(param_dir)
    return {p.stem for p in param_dir.glob("*.yaml")}
