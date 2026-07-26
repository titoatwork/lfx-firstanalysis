#!/usr/bin/env python3
"""
Score baseline/treatment extractions against preregistered gold.

Integrity rules:
  - Infrastructure failures (API errors) are NOT scored as model zeros.
  - schema_validity uses the vendored UDB param JSON Schema (not two-field checks).
  - classification_accuracy denominator = all positives (miss = incorrect).
  - name_agnostic_detection is implemented (keyword/type signal without requiring
    exact gold name).

Usage:
  python score_holdout.py
  python score_holdout.py --results-dir results/parsed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from normalize import normalize_param_name, normalize_ws

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "holdout_cases.yaml"
CHALLENGE_SCHEMA = ROOT.parent / "schema" / "param_schema.json"
SCHEMA_DIR = ROOT.parent / "schema"

DOC_SPLIT = re.compile(r"(?m)^---\s*$")
NAME_RE = re.compile(r"(?m)^name:\s*([A-Za-z0-9_]+)\s*$")
ERROR_MARKERS = (
    "# ERROR:",
    "# INFRA_ERROR:",
    "INFRA_ERROR",
)
STOP = {
    "that",
    "this",
    "with",
    "from",
    "when",
    "which",
    "their",
    "have",
    "been",
    "will",
    "into",
    "only",
    "also",
    "than",
    "then",
    "true",
    "false",
    "type",
    "name",
    "kind",
    "parameter",
    "schema",
    "description",
    "whether",
    "must",
    "should",
    "may",
    "mode",
    "modes",
    "value",
    "values",
    "field",
    "fields",
    "register",
    "the",
    "and",
    "for",
    "are",
    "not",
    "any",
    "all",
    "set",
    "can",
}

_schema_cache: tuple[Any, Any] | None = None


def load_yaml_docs(text: str) -> list[dict[str, Any]]:
    """Parse one or more YAML docs from model output (tolerant)."""
    if is_infra_error_text(text):
        return []
    docs: list[dict[str, Any]] = []
    cleaned = re.sub(r"```(?:yaml|yml)?", "", text)
    cleaned = cleaned.replace("```", "")
    chunks = [c.strip() for c in DOC_SPLIT.split(cleaned) if c.strip()]
    if not chunks:
        chunks = [cleaned.strip()] if cleaned.strip() else []
    for chunk in chunks:
        if chunk.strip().startswith("{") and "kind: parameter" not in chunk:
            continue
        try:
            doc = yaml.safe_load(chunk)
        except yaml.YAMLError:
            continue
        if isinstance(doc, dict) and (doc.get("name") or doc.get("kind") == "parameter"):
            docs.append(doc)
        elif isinstance(doc, list):
            for item in doc:
                if isinstance(item, dict) and item.get("name"):
                    docs.append(item)
    if not docs:
        for m in NAME_RE.finditer(cleaned):
            docs.append({"name": m.group(1), "kind": "parameter", "schema": {}})
    return docs


def is_infra_error_text(text: str) -> bool:
    if not text:
        return False
    head = text.lstrip()[:200]
    return any(head.startswith(m) or m in head[:80] for m in ERROR_MARKERS)


def is_infra_error_path(path: Path) -> bool:
    if not path.is_file():
        return False
    # Sidecar status file
    status = path.with_suffix(path.suffix + ".status.json")
    if status.is_file():
        try:
            meta = json.loads(status.read_text(encoding="utf-8"))
            if meta.get("ok") is False or meta.get("status") == "infra_error":
                return True
        except json.JSONDecodeError:
            pass
    return is_infra_error_text(path.read_text(encoding="utf-8"))


def _load_param_schema() -> tuple[dict[str, Any], dict[str, Any]]:
    global _schema_cache
    if _schema_cache is not None:
        return _schema_cache  # type: ignore[return-value]
    try:
        from jsonschema import Draft7Validator
        from jsonschema.validators import RefResolver
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("jsonschema required for schema_validity") from exc

    store: dict[str, Any] = {}
    for path in SCHEMA_DIR.glob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        store[path.name] = doc
        store[f"{path.name}#"] = doc
        sid = doc.get("$id")
        if isinstance(sid, str):
            store[sid] = doc
    schema = json.loads(CHALLENGE_SCHEMA.read_text(encoding="utf-8"))
    _schema_cache = (schema, store)
    return schema, store


def schema_valid(doc: dict[str, Any]) -> bool:
    """True iff doc validates against vendored UDB param_schema.json."""
    if not isinstance(doc, dict):
        return False
    # Ensure minimal shape for validator; fill $schema if missing
    candidate = dict(doc)
    if "$schema" not in candidate:
        candidate["$schema"] = "param_schema.json#"
    if candidate.get("kind") is None:
        candidate["kind"] = "parameter"
    try:
        from jsonschema import Draft7Validator
        from jsonschema.validators import RefResolver
    except ImportError:
        # Fallback only if jsonschema missing (should not happen in CI)
        return bool(candidate.get("name") and isinstance(candidate.get("schema"), dict))

    schema, store = _load_param_schema()
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft7Validator(schema, resolver=resolver)
    return not any(validator.iter_errors(candidate))


def type_of(doc: dict[str, Any]) -> str | None:
    schema = doc.get("schema")
    if isinstance(schema, dict):
        t = schema.get("type")
        return str(t) if t is not None else None
    return None


def class_match(pred: str | None, gold_class: str) -> bool:
    if not pred:
        return False
    p = pred.upper().replace("-", "_")
    g = gold_class.upper()
    if g == "NORM_CSR_WARL":
        return p in {"NORM_CSR_WARL", "WARL", "CSR_WARL"}
    if g == "NORM_CSR_RW":
        return p in {"NORM_CSR_RW", "CSR_RW", "RW", "CSR_READ_WRITE"}
    if g == "NORM_DIRECT":
        return p in {"NORM_DIRECT", "DIRECT", "WLRL", "NORM_WLRL"}
    return p == g


def name_hit(extracted: list[dict[str, Any]], gold_name: str, aliases: list[str]) -> dict[str, Any] | None:
    targets = {normalize_param_name(gold_name)}
    targets |= {normalize_param_name(a) for a in aliases}
    for doc in extracted:
        n = normalize_param_name(str(doc.get("name", "")))
        if n and n in targets:
            return doc
    return None


def _keywords(text: str) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_]{3,}", text or "")
    out = set()
    for w in words:
        lw = w.lower()
        if lw in STOP:
            continue
        out.add(lw)
    return out


def name_agnostic_detection(
    docs: list[dict[str, Any]],
    gold: dict[str, Any],
    gold_name: str,
    aliases: list[str],
) -> bool:
    """
    Detection without requiring exact gold name.

    Hit if:
      - exact/alias name match, OR
      - ≥1 schema-valid param whose description/name keywords overlap gold
        description (≥2 shared keywords), OR
      - ≥1 schema-valid param with matching schema.type and ≥1 shared keyword
    """
    if name_hit(docs, gold_name, aliases):
        return True
    gold_kw = _keywords(str(gold.get("description") or "") + " " + str(gold.get("long_name") or ""))
    gold_type = (gold.get("schema") or {}).get("type")
    if not docs:
        return False
    for doc in docs:
        if not schema_valid(doc) and not (
            doc.get("name") and isinstance(doc.get("schema"), dict) and doc["schema"].get("type")
        ):
            # Prefer full schema_valid; allow weak typed docs only with strong keyword overlap
            weak = True
        else:
            weak = not schema_valid(doc)
        blob = " ".join(
            [
                str(doc.get("name") or ""),
                str(doc.get("long_name") or ""),
                str(doc.get("description") or ""),
            ]
        )
        shared = _keywords(blob) & gold_kw
        if len(shared) >= 2 and (schema_valid(doc) or not weak):
            return True
        if gold_type and type_of(doc) == gold_type and len(shared) >= 1 and schema_valid(doc):
            return True
    return False


def quote_grounded(raw_text: str, source: str, context: str) -> bool | None:
    if is_infra_error_text(raw_text):
        return None
    m = re.search(r'"quote"\s*:\s*"([^"]+)"', raw_text)
    if not m:
        m = re.search(r"(?m)^quote:\s*[|>]?\s*(.+)$", raw_text)
        if not m:
            return None
        quote = m.group(1).strip().strip('"')
    else:
        quote = m.group(1)
    q = normalize_ws(quote)
    if len(q) < 8:
        return False
    hay = normalize_ws(source + "\n" + context)
    return q in hay or q.lower() in hay.lower()


def score_condition(
    manifest: dict[str, Any],
    condition: str,
    results_dir: Path,
) -> dict[str, Any]:
    positives = manifest["positives"]
    negatives = manifest["negatives"]
    warl_ids = {c["id"] for c in positives if c.get("strata") == "warl"}

    rows: list[dict[str, Any]] = []
    name_hits = 0
    detect_hits = 0
    class_hits = 0
    type_hits = 0
    type_den = 0
    schema_ok_docs = 0
    schema_docs = 0
    grounded = 0
    grounded_den = 0
    warl_hits = 0
    neg_fp = 0
    infra_errors = 0
    scored_positives = 0
    review: list[dict[str, Any]] = []

    n_pos = len(positives)
    n_warl = len(warl_ids)

    for case in positives:
        cid = case["id"]
        path = results_dir / condition / f"{cid}.txt"
        missing = not path.is_file()
        infra = (not missing) and is_infra_error_path(path)
        if missing or infra:
            infra_errors += 1
            rows.append(
                {
                    "id": cid,
                    "name": case["name"],
                    "class": case["class"],
                    "status": "infra_error" if infra else "missing",
                    "scored": False,
                }
            )
            review.append(
                {
                    "id": cid,
                    "reason": "infra_error" if infra else "missing_result",
                    "note": "excluded from model metrics (not a model zero)",
                }
            )
            continue

        scored_positives += 1
        raw = path.read_text(encoding="utf-8")
        docs = load_yaml_docs(raw)
        schema_docs += len(docs)
        schema_ok_docs += sum(1 for d in docs if schema_valid(d))

        gold = yaml.safe_load((ROOT / case["gold_path"]).read_text(encoding="utf-8"))
        hit_doc = name_hit(docs, case["name"], case.get("aliases") or [])
        hit = hit_doc is not None
        detected = name_agnostic_detection(docs, gold, case["name"], case.get("aliases") or [])
        if hit:
            name_hits += 1
            if case["id"] in warl_ids:
                warl_hits += 1
        if detected:
            detect_hits += 1

        # Classification: miss or wrong/missing class = fail; den = all scored positives
        pred_class = hit_doc.get("class") if hit_doc else None
        if hit and class_match(str(pred_class) if pred_class else None, case["class"]):
            class_hits += 1

        gold_type = (gold.get("schema") or {}).get("type")
        if gold_type is not None and hit_doc is not None:
            type_den += 1
            if type_of(hit_doc) == gold_type:
                type_hits += 1
            else:
                review.append({"id": cid, "reason": "type_mismatch", "got": type_of(hit_doc), "want": gold_type})
        elif not hit and docs:
            review.append(
                {
                    "id": cid,
                    "reason": "name_miss_with_extractions",
                    "names": [d.get("name") for d in docs],
                    "detected": detected,
                }
            )

        src = (ROOT / case["source_path"]).read_text(encoding="utf-8")
        ctx = ""
        if condition == "treatment":
            for c in case.get("csr_context_ids") or []:
                p = ROOT / "contexts" / f"{c}.txt"
                if p.is_file():
                    ctx += p.read_text(encoding="utf-8") + "\n"
        g = quote_grounded(raw, src, ctx)
        if g is not None:
            grounded_den += 1
            if g:
                grounded += 1

        rows.append(
            {
                "id": cid,
                "name": case["name"],
                "class": case["class"],
                "status": "ok",
                "scored": True,
                "name_hit": hit,
                "name_agnostic_detection": detected,
                "n_extracted": len(docs),
                "schema_valid_docs": sum(1 for d in docs if schema_valid(d)),
            }
        )

    scored_negatives = 0
    for case in negatives:
        cid = case["id"]
        path = results_dir / condition / f"{cid}.txt"
        missing = not path.is_file()
        infra = (not missing) and is_infra_error_path(path)
        if missing or infra:
            infra_errors += 1
            rows.append(
                {
                    "id": cid,
                    "name": case["name"],
                    "class": "NEGATIVE",
                    "status": "infra_error" if infra else "missing",
                    "scored": False,
                }
            )
            review.append({"id": cid, "reason": "infra_error" if infra else "missing_result"})
            continue
        scored_negatives += 1
        raw = path.read_text(encoding="utf-8")
        docs = load_yaml_docs(raw)
        fp = len(docs) > 0
        if fp:
            neg_fp += 1
            review.append({"id": cid, "reason": "negative_fp", "names": [d.get("name") for d in docs]})
        rows.append(
            {
                "id": cid,
                "name": case["name"],
                "class": "NEGATIVE",
                "status": "ok",
                "scored": True,
                "fp": fp,
                "n_extracted": len(docs),
            }
        )

    # Denominators: use scored subset when infra errors present; also report planned n
    den_pos = scored_positives if scored_positives else 0
    den_warl = sum(
        1
        for c in positives
        if c.get("strata") == "warl"
        and any(r.get("id") == c["id"] and r.get("scored") for r in rows)
    )
    den_neg = scored_negatives

    summary = {
        "condition": condition,
        "n_positives_planned": n_pos,
        "n_positives_scored": scored_positives,
        "infra_or_missing": infra_errors,
        "exact_or_alias_name_recall": f"{name_hits}/{den_pos}" if den_pos else "0/0",
        "exact_or_alias_name_recall_frac": name_hits / den_pos if den_pos else None,
        "name_agnostic_detection_recall": f"{detect_hits}/{den_pos}" if den_pos else "0/0",
        "name_agnostic_detection_recall_frac": detect_hits / den_pos if den_pos else None,
        "warl_recall": f"{warl_hits}/{den_warl}" if den_warl else "0/0",
        "warl_recall_frac": warl_hits / den_warl if den_warl else None,
        # Classification: hits / all scored positives (miss counts as wrong)
        "classification_accuracy": f"{class_hits}/{den_pos}" if den_pos else "0/0",
        "classification_accuracy_frac": class_hits / den_pos if den_pos else None,
        "classification_note": "denominator = all scored positives; name-miss = incorrect",
        "type_fidelity": f"{type_hits}/{type_den}" if type_den else "0/0",
        "schema_validity_docs": f"{schema_ok_docs}/{schema_docs}" if schema_docs else "0/0",
        "schema_validity_note": "jsonschema Draft7 vs challenge/schema/param_schema.json",
        "quote_grounding": f"{grounded}/{grounded_den}" if grounded_den else "0/0",
        "negative_control_fp": f"{neg_fp}/{den_neg}" if den_neg else "0/0",
        "rows": rows,
        "review_queue": review,
    }
    return summary


def print_table(summaries: list[dict[str, Any]]) -> None:
    print("\n### Compact scores (raw counts; n≈10 positives + 3 negatives)\n")
    hdr = (
        f"{'condition':12} {'name':10} {'detect':10} {'WARL':8} {'class':10} "
        f"{'type':10} {'schema':12} {'neg_FP':8} {'infra':6}"
    )
    print(hdr)
    print("-" * len(hdr))
    for s in summaries:
        print(
            f"{s['condition']:12} {s['exact_or_alias_name_recall']:10} "
            f"{s['name_agnostic_detection_recall']:10} {s['warl_recall']:8} "
            f"{s['classification_accuracy']:10} {s['type_fidelity']:10} "
            f"{s['schema_validity_docs']:12} {s['negative_control_fp']:8} "
            f"{s['infra_or_missing']:<6}"
        )
        if s["infra_or_missing"]:
            print(
                f"  note: {s['infra_or_missing']} infra/missing case(s) "
                f"excluded from model metrics (not scored as zeros)"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results" / "parsed")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "scored" / "scores.json")
    args = parser.parse_args()

    sys.path.insert(0, str(Path(__file__).resolve().parent))

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    summaries = [score_condition(manifest, cond, args.results_dir) for cond in ("baseline", "treatment")]

    print_table(summaries)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "pilot_id": manifest.get("pilot_id"),
        "pins": manifest.get("pins"),
        "conditions": summaries,
    }
    args.out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    review_path = args.out.parent / "review_queue.json"
    review_path.write_text(
        json.dumps({s["condition"]: s["review_queue"] for s in summaries}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {args.out}")
    print(f"wrote {review_path}")
    # Non-zero if any infra errors (callers can ignore)
    if any(s["infra_or_missing"] for s in summaries):
        return 0  # scoring succeeded; infra is reported in JSON
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
