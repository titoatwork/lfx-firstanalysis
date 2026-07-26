#!/usr/bin/env python3
"""
Score baseline/treatment extractions against preregistered gold.

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

DOC_SPLIT = re.compile(r"(?m)^---\s*$")
NAME_RE = re.compile(r"(?m)^name:\s*([A-Za-z0-9_]+)\s*$")


def load_yaml_docs(text: str) -> list[dict[str, Any]]:
    """Parse one or more YAML docs from model output (tolerant)."""
    docs: list[dict[str, Any]] = []
    # strip markdown fences
    cleaned = re.sub(r"```(?:yaml|yml)?", "", text)
    cleaned = cleaned.replace("```", "")
    chunks = [c.strip() for c in DOC_SPLIT.split(cleaned) if c.strip()]
    if not chunks:
        chunks = [cleaned.strip()] if cleaned.strip() else []
    for chunk in chunks:
        if "kind: parameter" not in chunk and not NAME_RE.search(chunk):
            # try JSON evidence-only skip
            if chunk.strip().startswith("{"):
                continue
            # still try parse
            pass
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
    # fallback: find name: lines only
    if not docs:
        for m in NAME_RE.finditer(cleaned):
            docs.append({"name": m.group(1), "kind": "parameter", "schema": {}})
    return docs


def schema_valid(doc: dict[str, Any]) -> bool:
    if not doc.get("name"):
        return False
    schema = doc.get("schema")
    if isinstance(schema, dict) and schema.get("type"):
        return True
    return False


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


def quote_grounded(raw_text: str, source: str, context: str) -> bool | None:
    """Return True/False if a quote is found; None if no quote field present."""
    # look for "quote": "..."
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
    class_hits = 0
    class_den = 0
    type_hits = 0
    type_den = 0
    schema_ok_docs = 0
    schema_docs = 0
    grounded = 0
    grounded_den = 0
    warl_hits = 0
    neg_fp = 0
    review: list[dict[str, Any]] = []

    for case in positives:
        cid = case["id"]
        path = results_dir / condition / f"{cid}.txt"
        raw = path.read_text(encoding="utf-8") if path.is_file() else ""
        docs = load_yaml_docs(raw) if raw else []
        schema_docs += len(docs)
        schema_ok_docs += sum(1 for d in docs if schema_valid(d))

        gold_path = ROOT / case["gold_path"]
        gold = yaml.safe_load(gold_path.read_text(encoding="utf-8"))
        hit_doc = name_hit(docs, case["name"], case.get("aliases") or [])
        hit = hit_doc is not None
        if hit:
            name_hits += 1
            if case["id"] in warl_ids:
                warl_hits += 1
            class_den += 1
            pred_class = hit_doc.get("class") if hit_doc else None
            if class_match(str(pred_class) if pred_class else None, case["class"]):
                class_hits += 1
            gold_type = (gold.get("schema") or {}).get("type")
            if gold_type is not None and hit_doc is not None:
                type_den += 1
                if type_of(hit_doc) == gold_type:
                    type_hits += 1
                else:
                    review.append({"id": cid, "reason": "type_mismatch", "got": type_of(hit_doc), "want": gold_type})
        else:
            if docs:
                review.append({"id": cid, "reason": "name_miss_with_extractions", "names": [d.get("name") for d in docs]})

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
                "name_hit": hit,
                "n_extracted": len(docs),
                "missing_result_file": not path.is_file(),
            }
        )

    for case in negatives:
        cid = case["id"]
        path = results_dir / condition / f"{cid}.txt"
        raw = path.read_text(encoding="utf-8") if path.is_file() else ""
        docs = load_yaml_docs(raw) if raw else []
        fp = len(docs) > 0
        if fp:
            neg_fp += 1
            review.append({"id": cid, "reason": "negative_fp", "names": [d.get("name") for d in docs]})
        rows.append(
            {
                "id": cid,
                "name": case["name"],
                "class": "NEGATIVE",
                "name_hit": False,
                "fp": fp,
                "n_extracted": len(docs),
                "missing_result_file": not path.is_file(),
            }
        )

    n_pos = len(positives)
    n_warl = len(warl_ids)
    summary = {
        "condition": condition,
        "n_positives": n_pos,
        "exact_or_alias_name_recall": f"{name_hits}/{n_pos}",
        "exact_or_alias_name_recall_frac": name_hits / n_pos if n_pos else 0.0,
        "warl_recall": f"{warl_hits}/{n_warl}",
        "warl_recall_frac": warl_hits / n_warl if n_warl else 0.0,
        "classification_accuracy": f"{class_hits}/{class_den}" if class_den else "0/0",
        "type_fidelity": f"{type_hits}/{type_den}" if type_den else "0/0",
        "schema_validity_docs": f"{schema_ok_docs}/{schema_docs}" if schema_docs else "0/0",
        "quote_grounding": f"{grounded}/{grounded_den}" if grounded_den else "0/0",
        "negative_control_fp": f"{neg_fp}/{len(negatives)}",
        "rows": rows,
        "review_queue": review,
    }
    return summary


def print_table(summaries: list[dict[str, Any]]) -> None:
    print("\n### Compact scores (raw counts; n=10 positives + 3 negatives)\n")
    hdr = (
        f"{'condition':12} {'name_recall':12} {'WARL':10} {'class':10} "
        f"{'type':10} {'schema':12} {'ground':10} {'neg_FP':10}"
    )
    print(hdr)
    print("-" * len(hdr))
    for s in summaries:
        print(
            f"{s['condition']:12} {s['exact_or_alias_name_recall']:12} "
            f"{s['warl_recall']:10} {s['classification_accuracy']:10} "
            f"{s['type_fidelity']:10} {s['schema_validity_docs']:12} "
            f"{s['quote_grounding']:10} {s['negative_control_fp']:10}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results" / "parsed")
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "scored" / "scores.json")
    args = parser.parse_args()

    sys.path.insert(0, str(Path(__file__).resolve().parent))

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    summaries = []
    for cond in ("baseline", "treatment"):
        summaries.append(score_condition(manifest, cond, args.results_dir))

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
        json.dumps(
            {s["condition"]: s["review_queue"] for s in summaries},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {args.out}")
    print(f"wrote {review_path}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
