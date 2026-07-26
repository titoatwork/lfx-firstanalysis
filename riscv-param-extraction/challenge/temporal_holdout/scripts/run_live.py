#!/usr/bin/env python3
"""
Run frozen-model baseline and treatment for the holdout pilot.

Requires OPENAI_API_KEY and explicit --live. Estimates cost first with --estimate.

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
    n = len(cases(manifest)) * 2  # baseline + treatment
    # rough: 1.5k in / 400 out tokens per call for mini
    in_tok = n * 1500
    out_tok = n * 400
    # gpt-4o-mini list prices approx $0.15/1M in $0.60/1M out (order-of-magnitude)
    cost = in_tok / 1e6 * 0.15 + out_tok / 1e6 * 0.60
    print(f"cases: {len(cases(manifest))} × 2 conditions = {n} calls")
    print(f"est tokens: ~{in_tok} in / ~{out_tok} out")
    print(f"est cost gpt-4o-mini: ~${cost:.3f} (order-of-magnitude)")
    print("Requires explicit --live + OPENAI_API_KEY. No retries.")


def call_openai(model: str, prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""


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
    meta = {
        "model": args.model,
        "temperature": 0,
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "calls": [],
    }

    for case in cases(manifest):
        for cond in ("baseline", "treatment"):
            prompt_path = BUILT / f"{case['id']}_{cond}.txt"
            if not prompt_path.is_file():
                print(f"missing prompt {prompt_path}", file=sys.stderr)
                return 2
            prompt = prompt_path.read_text(encoding="utf-8")
            print(f"calling {case['id']} {cond} ...", flush=True)
            try:
                text = call_openai(args.model, prompt)
                err = None
            except Exception as exc:  # noqa: BLE001
                text = ""
                err = str(exc)
                print(f"  FAIL: {err}", file=sys.stderr)

            raw_path = RAW / f"{case['id']}__{cond}__{args.model}.txt"
            raw_path.write_text(text if text else f"# ERROR: {err}\n", encoding="utf-8")
            parsed_dir = PARSED / cond
            parsed_dir.mkdir(parents=True, exist_ok=True)
            (parsed_dir / f"{case['id']}.txt").write_text(text, encoding="utf-8")
            meta["calls"].append(
                {
                    "id": case["id"],
                    "condition": cond,
                    "ok": err is None,
                    "error": err,
                    "raw": str(raw_path.relative_to(ROOT)),
                    "chars": len(text),
                }
            )

    meta_path = RAW / "RUN_META.json"
    meta["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {meta_path}")
    print("Next: python score_holdout.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
