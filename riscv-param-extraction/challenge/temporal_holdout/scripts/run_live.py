#!/usr/bin/env python3
"""
Run frozen-model baseline and treatment for the holdout pilot.

Requires OPENAI_API_KEY and explicit --live. Estimates cost first with --estimate.

Integrity: API / transport failures are recorded as INFRA_ERROR and are NOT
written as empty model extractions for scoring.

Usage:
  python run_live.py --estimate
  python run_live.py --live --model gpt-4o-mini-2024-07-18
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "holdout_cases.yaml"
BUILT = ROOT / "prompts" / "built"
RAW = ROOT / "results" / "raw"
PARSED = ROOT / "results" / "parsed"


def cases(manifest: dict) -> list[dict]:
    return list(manifest["positives"]) + list(manifest["negatives"])


def estimate(manifest: dict) -> None:
    n = len(cases(manifest)) * 2
    in_tok = n * 1500
    out_tok = n * 400
    cost = in_tok / 1e6 * 0.15 + out_tok / 1e6 * 0.60
    print(f"cases: {len(cases(manifest))} × 2 conditions = {n} calls")
    print(f"est tokens: ~{in_tok} in / ~{out_tok} out")
    print(f"est cost gpt-4o-mini: ~${cost:.3f} (order-of-magnitude)")
    print("Requires explicit --live + OPENAI_API_KEY. No retries.")
    print("Dependency: openai (see requirements.txt).")


def call_openai(model: str, prompt: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "openai package not installed. pip install -r requirements.txt"
        ) from exc

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""


def write_infra_error(parsed_path: Path, raw_path: Path, err: str, case_id: str, cond: str) -> None:
    """Record infrastructure failure; scorer must exclude these from model metrics."""
    body = f"# INFRA_ERROR: {err}\n# case={case_id} condition={cond}\n"
    raw_path.write_text(body, encoding="utf-8")
    parsed_path.write_text(body, encoding="utf-8")
    status = {
        "ok": False,
        "status": "infra_error",
        "error": err,
        "case": case_id,
        "condition": cond,
    }
    parsed_path.with_suffix(parsed_path.suffix + ".status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )
    raw_path.with_suffix(raw_path.suffix + ".status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )


def write_success(parsed_path: Path, raw_path: Path, text: str, case_id: str, cond: str) -> None:
    raw_path.write_text(text, encoding="utf-8")
    parsed_path.write_text(text, encoding="utf-8")
    status = {"ok": True, "status": "ok", "case": case_id, "condition": cond, "chars": len(text)}
    parsed_path.with_suffix(parsed_path.suffix + ".status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    parser.add_argument("--retries", type=int, default=0)
    args = parser.parse_args()

    if args.retries != 0:
        print("Refusing non-zero retries.", file=sys.stderr)
        return 2

    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    if args.estimate and not args.live:
        estimate(manifest)
        return 0

    if not args.live:
        print("Dry-run. Pass --estimate or --live.", file=sys.stderr)
        return 2

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set", file=sys.stderr)
        return 2

    pin_model = (manifest.get("pins") or {}).get("model_id")
    if args.model != pin_model:
        print(
            f"WARNING: model {args.model} != preregistered pin {pin_model}",
            file=sys.stderr,
        )

    RAW.mkdir(parents=True, exist_ok=True)
    PARSED.mkdir(parents=True, exist_ok=True)
    meta: dict = {
        "model": args.model,
        "temperature": 0,
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "calls": [],
    }
    failures = 0

    for case in cases(manifest):
        for cond in ("baseline", "treatment"):
            prompt_path = BUILT / f"{case['id']}_{cond}.txt"
            if not prompt_path.is_file():
                print(f"missing prompt {prompt_path}", file=sys.stderr)
                return 2
            prompt = prompt_path.read_text(encoding="utf-8")
            print(f"calling {case['id']} {cond} ...", flush=True)
            raw_path = RAW / f"{case['id']}__{cond}__{args.model}.txt"
            parsed_dir = PARSED / cond
            parsed_dir.mkdir(parents=True, exist_ok=True)
            parsed_path = parsed_dir / f"{case['id']}.txt"

            try:
                text = call_openai(args.model, prompt)
                write_success(parsed_path, raw_path, text, case["id"], cond)
                err = None
            except Exception as exc:  # noqa: BLE001
                err = f"{type(exc).__name__}: {exc}"
                print(f"  INFRA_ERROR: {err}", file=sys.stderr)
                write_infra_error(parsed_path, raw_path, err, case["id"], cond)
                failures += 1

            meta["calls"].append(
                {
                    "id": case["id"],
                    "condition": cond,
                    "ok": err is None,
                    "status": "ok" if err is None else "infra_error",
                    "error": err,
                    "raw": str(raw_path.relative_to(ROOT)),
                    "chars": 0 if err else len(text),
                }
            )

    meta["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    meta["failures"] = failures
    meta_path = RAW / "RUN_META.json"
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {meta_path}")
    print(f"failures (infra): {failures}")
    print("Next: python score_holdout.py  # infra cases excluded from model metrics")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
