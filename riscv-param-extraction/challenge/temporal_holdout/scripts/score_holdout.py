#!/usr/bin/env python3
"""
Score baseline/treatment extractions against preregistered gold.

Integrity:
  - Validate *untouched* UDB param docs (no injection of $schema/kind).
  - class lives in eval metadata JSON, not in param YAML.
  - Grounding is per extracted parameter; missing quote = not grounded.
  - Primary comparison requires a complete 26/26 run (same case set both conditions).

Usage:
  python score_holdout.py
  python score_holdout.py --results-dir results/runs/<id>/parsed
  python score_holdout.py --allow-incomplete   # debug only; not primary claim
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
PRIMARY_POINTER = ROOT / "results" / "PRIMARY_RUN.json"
RUNS = ROOT / "results" / "runs"

DOC_SPLIT = re.compile(r"(?m)^---\s*$")
NAME_RE = re.compile(r"(?m)^name:\s*([A-Za-z0-9_]+)\s*$")
STOP = {
    "that", "this", "with", "from", "when", "which", "their", "have", "been",
    "will", "into", "only", "also", "than", "then", "true", "false", "type",
    "name", "kind", "parameter", "schema", "description", "whether", "must",
    "should", "may", "mode", "modes", "value", "values", "field", "fields",
    "register", "the", "and", "for", "are", "not", "any", "all", "set", "can",
}

_schema_cache: tuple[Any, Any] | None = None


def is_infra_marker_path(path: Path) -> bool:
    if path.name.endswith(".INFRA_ERROR.txt"):
        return True
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    head = text.lstrip()[:120]
    return head.startswith("# INFRA_ERROR:") or head.startswith("# ERROR:")


def parse_model_output(text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Return (param_docs, eval_items).

    param_docs: YAML mappings intended as UDB parameters (untouched).
    eval_items: list of {name, class?, quote?} from eval metadata JSON.
    """
    if not text:
        return [], []
    if text.lstrip().startswith("# INFRA_ERROR") or text.lstrip().startswith("# ERROR"):
        return [], []

    cleaned = re.sub(r"```(?:yaml|yml|json)?", "", text)
    cleaned = cleaned.replace("```", "")

    param_docs: list[dict[str, Any]] = []
    eval_items: list[dict[str, Any]] = []

    # Extract JSON objects first (eval metadata / evidence), then strip them
    # so YAML loading is not poisoned by trailing JSON.
    json_blobs = list(re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", cleaned, re.S))
    for m in json_blobs:
        blob = m.group(0)
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("eval") is True and isinstance(obj.get("items"), list):
            for it in obj["items"]:
                if isinstance(it, dict):
                    eval_items.append(it)
        elif "quote" in obj and obj.get("name"):
            eval_items.append(obj)

    yaml_only = cleaned
    for m in reversed(json_blobs):
        try:
            json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        yaml_only = yaml_only[: m.start()] + "\n" + yaml_only[m.end() :]

    # YAML parameter documents
    chunks = [c.strip() for c in DOC_SPLIT.split(yaml_only) if c.strip()]
    if not chunks:
        chunks = [yaml_only.strip()] if yaml_only.strip() else []
    for chunk in chunks:
        if chunk.lstrip().startswith("{"):
            continue
        try:
            doc = yaml.safe_load(chunk)
        except yaml.YAMLError:
            continue
        if isinstance(doc, dict) and doc.get("kind") == "parameter":
            param_docs.append(doc)
        elif isinstance(doc, dict) and doc.get("name") and "schema" in doc and doc.get("eval") is not True:
            if "quote" not in doc:
                param_docs.append(doc)
        elif isinstance(doc, list):
            for item in doc:
                if isinstance(item, dict) and (item.get("kind") == "parameter" or item.get("name")):
                    param_docs.append(item)

    return param_docs, eval_items


def eval_for_name(eval_items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    target = normalize_param_name(name)
    for it in eval_items:
        if normalize_param_name(str(it.get("name", ""))) == target:
            return it
    return None


def _load_param_schema() -> tuple[dict[str, Any], dict[str, Any]]:
    global _schema_cache
    if _schema_cache is not None:
        return _schema_cache  # type: ignore[return-value]
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
    """Validate the document as-is (no field injection)."""
    if not isinstance(doc, dict):
        return False
    try:
        from jsonschema import Draft7Validator
        from jsonschema.validators import RefResolver
    except ImportError:
        return False
    schema, store = _load_param_schema()
    resolver = RefResolver.from_schema(schema, store=store)
    validator = Draft7Validator(schema, resolver=resolver)
    return not any(validator.iter_errors(doc))


def type_of(doc: dict[str, Any]) -> str | None:
    schema = doc.get("schema")
    if isinstance(schema, dict) and schema.get("type") is not None:
        return str(schema["type"])
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
    return {w.lower() for w in words if w.lower() not in STOP}


def name_agnostic_detection(
    docs: list[dict[str, Any]],
    gold: dict[str, Any],
    gold_name: str,
    aliases: list[str],
) -> bool:
    if name_hit(docs, gold_name, aliases):
        return True
    gold_kw = _keywords(str(gold.get("description") or "") + " " + str(gold.get("long_name") or ""))
    gold_type = (gold.get("schema") or {}).get("type")
    for doc in docs:
        if not schema_valid(doc):
            continue
        blob = " ".join(
            [str(doc.get("name") or ""), str(doc.get("long_name") or ""), str(doc.get("description") or "")]
        )
        shared = _keywords(blob) & gold_kw
        if len(shared) >= 2:
            return True
        if gold_type and type_of(doc) == gold_type and len(shared) >= 1:
            return True
    return False


def quote_grounded(quote: str | None, source: str, context: str) -> bool:
    """Missing/empty quote = not grounded (failure)."""
    if not quote or not str(quote).strip():
        return False
    q = normalize_ws(str(quote))
    if len(q) < 8:
        return False
    hay = normalize_ws(source + "\n" + context)
    return q in hay or q.lower() in hay.lower()


def load_case_result(results_dir: Path, condition: str, case_id: str) -> tuple[str | None, str]:
    """
    Return (text_or_none, status) where status is ok|missing|infra_error.
    """
    parsed = results_dir / condition / f"{case_id}.txt"
    infra = results_dir / condition / f"{case_id}.INFRA_ERROR.txt"
    if infra.is_file() or (parsed.is_file() and is_infra_marker_path(parsed)):
        return None, "infra_error"
    if not parsed.is_file():
        return None, "missing"
    return parsed.read_text(encoding="utf-8"), "ok"


def _run_dir_from_parsed(parsed: Path) -> Path | None:
    """If parsed is .../runs/<id>/parsed, return run dir."""
    if parsed.name == "parsed" and parsed.parent.parent.name == "runs":
        return parsed.parent
    if (parsed / "RUN_META.json").is_file():
        return parsed
    if (parsed.parent / "RUN_META.json").is_file():
        return parsed.parent
    return None


def resolve_results_dir(cli: Path | None) -> tuple[Path, dict[str, Any] | None, Path | None]:
    """
    Returns (parsed_dir, run_meta_or_none, run_dir_or_none).

    Primary scoring always requires adjacent RUN_META.json (never file-count alone).
    """
    if cli is not None:
        parsed = cli
        run_dir = _run_dir_from_parsed(parsed.resolve())
        meta = None
        if run_dir and (run_dir / "RUN_META.json").is_file():
            meta = json.loads((run_dir / "RUN_META.json").read_text(encoding="utf-8"))
        elif (parsed / "RUN_META.json").is_file():
            meta = json.loads((parsed / "RUN_META.json").read_text(encoding="utf-8"))
            run_dir = parsed
        return parsed, meta, run_dir

    if PRIMARY_POINTER.is_file():
        ptr = json.loads(PRIMARY_POINTER.read_text(encoding="utf-8"))
        run_dir = ROOT / ptr["run_dir"]
        meta_path = run_dir / "RUN_META.json"
        if not meta_path.is_file():
            return run_dir / "parsed", None, run_dir
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return run_dir / "parsed", meta, run_dir

    legacy = ROOT / "results" / "parsed"
    return legacy, None, None


def validate_primary_meta(
    meta: dict[str, Any] | None,
    manifest: dict[str, Any],
    results_dir: Path,
) -> list[str]:
    """Hard requirements for primary comparison claims."""
    errs: list[str] = []
    if meta is None:
        errs.append("RUN_META.json required for primary score (file presence alone is insufficient)")
        return errs

    pins = manifest.get("pins") or {}
    pin_model = pins.get("model_id")
    n_expected = (len(manifest["positives"]) + len(manifest["negatives"])) * 2
    case_ids = [c["id"] for c in manifest["positives"] + manifest["negatives"]]

    if meta.get("model") != pin_model:
        errs.append(f"model {meta.get('model')!r} != pin {pin_model!r}")
    if meta.get("pin_model") not in (None, pin_model) and meta.get("pin_model") != pin_model:
        errs.append(f"pin_model field {meta.get('pin_model')!r} != pin {pin_model!r}")
    if meta.get("failures", 0) != 0:
        errs.append(f"failures={meta.get('failures')} (must be 0)")
    if meta.get("successful_calls") != n_expected:
        errs.append(
            f"successful_calls={meta.get('successful_calls')} != expected {n_expected}"
        )
    if meta.get("expected_calls") != n_expected:
        errs.append(f"expected_calls={meta.get('expected_calls')} != {n_expected}")
    if not meta.get("complete"):
        errs.append("complete != true")
    if not meta.get("primary_comparison_eligible"):
        errs.append("primary_comparison_eligible != true (debug or incomplete run)")
    if meta.get("debug_run"):
        errs.append("debug_run=true cannot be primary")

    # Prompt pin
    prompt_version = pins.get("prompt_version")
    if meta.get("prompt_version") != prompt_version:
        errs.append(
            f"prompt_version {meta.get('prompt_version')!r} != pin {prompt_version!r}"
        )
    hashes_path = ROOT / "prompts" / "built" / "PROMPT_HASHES.json"
    if hashes_path.is_file():
        ph = json.loads(hashes_path.read_text(encoding="utf-8"))
        if meta.get("template_sha256") and meta.get("template_sha256") != ph.get("template_sha256"):
            errs.append("template_sha256 mismatch vs PROMPT_HASHES.json")
        if ph.get("prompt_version") != prompt_version:
            errs.append("PROMPT_HASHES.json prompt_version mismatch vs manifest pin")

    # Exact call set: 26 unique successful (case, condition)
    calls = meta.get("calls") or []
    ok_pairs = {(c.get("id"), c.get("condition")) for c in calls if c.get("ok")}
    expected_pairs = {(cid, cond) for cid in case_ids for cond in ("baseline", "treatment")}
    if ok_pairs != expected_pairs:
        missing = sorted(expected_pairs - ok_pairs)
        extra = sorted(ok_pairs - expected_pairs)
        errs.append(f"call set mismatch: missing={missing[:5]}… extra={extra[:5]}…")
    if len(ok_pairs) != n_expected:
        errs.append(f"unique successful pairs={len(ok_pairs)} != {n_expected}")

    # Files must exist for every pair
    for cid, cond in expected_pairs:
        _raw, st = load_case_result(results_dir, cond, cid)
        if st != "ok":
            errs.append(f"parsed result not ok for {cid}/{cond}: {st}")

    return errs


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
    grounded_ok = 0
    grounded_den = 0
    warl_hits = 0
    neg_fp = 0
    status_counts = {"ok": 0, "missing": 0, "infra_error": 0}
    review: list[dict[str, Any]] = []

    for case in positives:
        cid = case["id"]
        raw, status = load_case_result(results_dir, condition, cid)
        status_counts[status] = status_counts.get(status, 0) + 1
        if status != "ok" or raw is None:
            rows.append(
                {
                    "id": cid,
                    "name": case["name"],
                    "class": case["class"],
                    "status": status,
                    "scored": False,
                }
            )
            review.append({"id": cid, "reason": status, "note": "not in primary model metrics"})
            continue

        docs, eval_items = parse_model_output(raw)
        schema_docs += len(docs)
        schema_ok_docs += sum(1 for d in docs if schema_valid(d))

        # Per-parameter grounding
        src = (ROOT / case["source_path"]).read_text(encoding="utf-8")
        ctx = ""
        if condition == "treatment":
            for c in case.get("csr_context_ids") or []:
                p = ROOT / "contexts" / f"{c}.txt"
                if p.is_file():
                    ctx += p.read_text(encoding="utf-8") + "\n"
        for doc in docs:
            grounded_den += 1
            ev = eval_for_name(eval_items, str(doc.get("name", "")))
            quote = (ev or {}).get("quote") if ev else None
            # also allow quote only in eval list
            if quote_grounded(quote if isinstance(quote, str) else None, src, ctx):
                grounded_ok += 1
            else:
                review.append(
                    {
                        "id": cid,
                        "reason": "ungrounded_param",
                        "param": doc.get("name"),
                        "has_eval": ev is not None,
                        "has_quote": bool(quote),
                    }
                )

        gold = yaml.safe_load((ROOT / case["gold_path"]).read_text(encoding="utf-8"))
        hit_doc = name_hit(docs, case["name"], case.get("aliases") or [])
        hit = hit_doc is not None
        detected = name_agnostic_detection(docs, gold, case["name"], case.get("aliases") or [])
        if hit:
            name_hits += 1
            if cid in warl_ids:
                warl_hits += 1
        if detected:
            detect_hits += 1

        # class from eval metadata, not param YAML
        pred_class = None
        if hit_doc is not None:
            ev = eval_for_name(eval_items, str(hit_doc.get("name", "")))
            if ev:
                pred_class = ev.get("class")
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
                "pred_class": pred_class,
            }
        )

    for case in negatives:
        cid = case["id"]
        raw, status = load_case_result(results_dir, condition, cid)
        status_counts[status] = status_counts.get(status, 0) + 1
        if status != "ok" or raw is None:
            rows.append(
                {
                    "id": cid,
                    "name": case["name"],
                    "class": "NEGATIVE",
                    "status": status,
                    "scored": False,
                }
            )
            review.append({"id": cid, "reason": status})
            continue
        docs, eval_items = parse_model_output(raw)
        # Schema totals include negative-case extractions (all extracted docs)
        schema_docs += len(docs)
        schema_ok_docs += sum(1 for d in docs if schema_valid(d))
        src = (ROOT / case["source_path"]).read_text(encoding="utf-8")
        for doc in docs:
            grounded_den += 1
            ev = eval_for_name(eval_items, str(doc.get("name", "")))
            quote = (ev or {}).get("quote") if ev else None
            if quote_grounded(quote if isinstance(quote, str) else None, src, ""):
                grounded_ok += 1
            else:
                review.append(
                    {
                        "id": cid,
                        "reason": "ungrounded_param",
                        "param": doc.get("name"),
                        "negative": True,
                    }
                )
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
                "schema_valid_docs": sum(1 for d in docs if schema_valid(d)),
            }
        )

    n_pos = len(positives)
    scored_pos = sum(1 for r in rows if r.get("class") != "NEGATIVE" and r.get("scored"))
    scored_neg = sum(1 for r in rows if r.get("class") == "NEGATIVE" and r.get("scored"))
    den_warl = sum(
        1
        for c in positives
        if c.get("strata") == "warl" and any(r.get("id") == c["id"] and r.get("scored") for r in rows)
    )

    return {
        "condition": condition,
        "n_positives_planned": n_pos,
        "n_positives_scored": scored_pos,
        "status_counts": status_counts,
        "exact_or_alias_name_recall": f"{name_hits}/{scored_pos}" if scored_pos else "0/0",
        "exact_or_alias_name_recall_frac": name_hits / scored_pos if scored_pos else None,
        "name_agnostic_detection_recall": f"{detect_hits}/{scored_pos}" if scored_pos else "0/0",
        "name_agnostic_detection_recall_frac": detect_hits / scored_pos if scored_pos else None,
        "warl_recall": f"{warl_hits}/{den_warl}" if den_warl else "0/0",
        "warl_recall_frac": warl_hits / den_warl if den_warl else None,
        "classification_accuracy": f"{class_hits}/{scored_pos}" if scored_pos else "0/0",
        "classification_accuracy_frac": class_hits / scored_pos if scored_pos else None,
        "classification_note": "class from eval metadata JSON; den=all scored positives",
        "type_fidelity": f"{type_hits}/{type_den}" if type_den else "0/0",
        "schema_validity_docs": f"{schema_ok_docs}/{schema_docs}" if schema_docs else "0/0",
        "schema_validity_note": "untouched docs; all extracted docs incl. negatives; no field injection",
        "quote_grounding": f"{grounded_ok}/{grounded_den}" if grounded_den else "0/0",
        "quote_grounding_note": "per extracted param; missing quote = fail",
        "negative_control_fp": f"{neg_fp}/{scored_neg}" if scored_neg else "0/0",
        "rows": rows,
        "review_queue": review,
    }


def print_table(summaries: list[dict[str, Any]]) -> None:
    print("\n### Compact scores (raw counts)\n")
    hdr = (
        f"{'condition':12} {'name':10} {'detect':10} {'WARL':8} {'class':10} "
        f"{'schema':12} {'ground':10} {'neg_FP':8}"
    )
    print(hdr)
    print("-" * len(hdr))
    for s in summaries:
        print(
            f"{s['condition']:12} {s['exact_or_alias_name_recall']:10} "
            f"{s['name_agnostic_detection_recall']:10} {s['warl_recall']:8} "
            f"{s['classification_accuracy']:10} {s['schema_validity_docs']:12} "
            f"{s['quote_grounding']:10} {s['negative_control_fp']:8}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--results-dir", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "scored" / "scores.json")
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="Score even if run is incomplete (not for primary claims)",
    )
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parent))

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    n_expected = (len(manifest["positives"]) + len(manifest["negatives"])) * 2

    results_dir, meta, run_dir = resolve_results_dir(args.results_dir)
    if not results_dir.is_dir():
        print(f"ERROR: results dir missing: {results_dir}", file=sys.stderr)
        print("Run live first, or pass --results-dir pointing at runs/<id>/parsed.", file=sys.stderr)
        return 2

    primary_errs = validate_primary_meta(meta, manifest, results_dir)
    primary_ok = len(primary_errs) == 0

    if not primary_ok and not args.allow_incomplete:
        print(
            f"REFUSE primary score: RUN_META validation failed "
            f"(need complete 26/26 pinned run with eligible flag).",
            file=sys.stderr,
        )
        for e in primary_errs:
            print(f"  - {e}", file=sys.stderr)
        print("Use --allow-incomplete only for debug (not primary claims).", file=sys.stderr)
        return 2

    if args.allow_incomplete and not primary_ok:
        print("WARNING: scoring with --allow-incomplete; not a primary comparison.", file=sys.stderr)
        for e in primary_errs:
            print(f"  - {e}", file=sys.stderr)

    summaries = [score_condition(manifest, cond, results_dir) for cond in ("baseline", "treatment")]
    if primary_ok:
        for s in summaries:
            if s["n_positives_scored"] != len(manifest["positives"]):
                print(
                    f"REFUSE: condition {s['condition']} scored "
                    f"{s['n_positives_scored']}/{len(manifest['positives'])} positives "
                    f"(asymmetric / incomplete case set).",
                    file=sys.stderr,
                )
                if not args.allow_incomplete:
                    return 2

    print_table(summaries)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "pilot_id": manifest.get("pilot_id"),
        "pins": manifest.get("pins"),
        "primary_comparison": primary_ok and not args.allow_incomplete,
        "allow_incomplete": args.allow_incomplete,
        "primary_validation_errors": primary_errs,
        "run_meta": meta,
        "run_dir": str(run_dir) if run_dir else None,
        "results_dir": str(results_dir),
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
    print(f"primary_comparison={payload['primary_comparison']}")
    return 0



if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
