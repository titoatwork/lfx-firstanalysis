#!/usr/bin/env python3
"""Build baseline and treatment prompts for each holdout case; record hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "holdout_cases.yaml"
TEMPLATE = ROOT / "prompts" / "holdout_v1.md"
OUT_DIR = ROOT / "prompts" / "built"


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_template() -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    if "```text" in text:
        return text.split("```text", 1)[1].split("```", 1)[0].strip()
    return text.strip()


def render(
    template: str,
    source: str,
    context: str | None,
    definedby_guidance: str,
) -> str:
    body = template.replace("{{SOURCE}}", source.strip())
    body = body.replace(
        "{{DEFINEDBY_GUIDANCE}}",
        (definedby_guidance or "Infer definedBy only from SOURCE; do not invent extensions.").strip(),
    )
    if context:
        ctx_block = (
            "\n\nCSR/FIELD CONTEXT (leakage-audited; may be incomplete):\n"
            "-----\n"
            f"{context.strip()}\n"
            "-----\n"
        )
        body = body.replace("{{CONTEXT_BLOCK}}", ctx_block)
    else:
        body = body.replace("{{CONTEXT_BLOCK}}", "")
    return body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    template = load_template()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    cases = list(manifest["positives"]) + list(manifest["negatives"])

    for case in cases:
        src_path = ROOT / case["source_path"]
        source = src_path.read_text(encoding="utf-8")
        source_hash = sha256_text(source)
        dbg = case.get("definedby_guidance") or "Infer definedBy only from SOURCE; do not invent extensions."

        base = render(template, source, None, dbg)
        base_path = args.out_dir / f"{case['id']}_baseline.txt"
        base_path.write_text(base + "\n", encoding="utf-8")

        ctx_parts: list[str] = []
        ctx_hashes: list[str] = []
        for cid in case.get("csr_context_ids") or []:
            cpath = ROOT / "contexts" / f"{cid}.txt"
            if cpath.is_file():
                ctext = cpath.read_text(encoding="utf-8")
                ctx_parts.append(ctext)
                ctx_hashes.append(sha256_text(ctext))
        context = "\n".join(ctx_parts) if ctx_parts else None
        treat = render(template, source, context, dbg)
        treat_path = args.out_dir / f"{case['id']}_treatment.txt"
        treat_path.write_text(treat + "\n", encoding="utf-8")

        records.append(
            {
                "id": case["id"],
                "name": case.get("name"),
                "source_path": case["source_path"],
                "source_sha256": source_hash,
                "definedby_guidance": dbg,
                "context_ids": case.get("csr_context_ids") or [],
                "context_sha256": ctx_hashes,
                "baseline_prompt_sha256": sha256_text(base),
                "treatment_prompt_sha256": sha256_text(treat),
                "baseline_path": str(base_path.relative_to(ROOT)).replace("\\", "/"),
                "treatment_path": str(treat_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )
        print(f"built {case['id']}")

    meta = {
        "prompt_version": manifest.get("pins", {}).get("prompt_version"),
        "template_sha256": sha256_text(template),
        "cases": records,
    }
    meta_path = args.out_dir / "PROMPT_HASHES.json"
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {meta_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
