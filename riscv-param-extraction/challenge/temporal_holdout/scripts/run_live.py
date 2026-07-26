#!/usr/bin/env python3
"""
Run frozen-model baseline and treatment for the holdout pilot.

Requires OPENAI_API_KEY and explicit --live.

Integrity:
  - Fail closed if --model != preregistered pin (no calls).
  - Refuse to overwrite an existing run directory.
  - Primary comparison requires 26/26 successful calls; failures retained
    under the run tree but run is marked incomplete.

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
RUNS = ROOT / "results" / "runs"
PRIMARY_POINTER = ROOT / "results" / "PRIMARY_RUN.json"


def cases(manifest: dict) -> list[dict]:
    return list(manifest["positives"]) + list(manifest["negatives"])


def expected_calls(manifest: dict) -> int:
    return len(cases(manifest)) * 2


def estimate(manifest: dict) -> None:
    n = expected_calls(manifest)
    in_tok = n * 1500
    out_tok = n * 400
    cost = in_tok / 1e6 * 0.15 + out_tok / 1e6 * 0.60
    print(f"cases: {len(cases(manifest))} × 2 conditions = {n} calls")
    print(f"est tokens: ~{in_tok} in / ~{out_tok} out")
    print(f"est cost gpt-4o-mini: ~${cost:.3f} (order-of-magnitude)")
    print("Requires explicit --live + OPENAI_API_KEY. No retries.")
    print("Dependency: openai (see requirements.txt).")
    print(f"Primary comparison requires {n}/{n} successful calls.")


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


def write_status(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--estimate", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run id; default UTC timestamp + model",
    )
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
            f"FAIL-CLOSED: model {args.model!r} != preregistered pin {pin_model!r}. "
            f"No API calls made.",
            file=sys.stderr,
        )
        return 2

    n_expected = expected_calls(manifest)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_id = args.run_id or f"{stamp}_{args.model}"
    run_dir = RUNS / run_id
    if run_dir.exists():
        print(
            f"FAIL-CLOSED: run directory already exists (refuse overwrite): {run_dir}",
            file=sys.stderr,
        )
        return 2

    raw_dir = run_dir / "raw"
    parsed_dir = run_dir / "parsed"
    failed_dir = run_dir / "failed_attempts"
    for d in (raw_dir, parsed_dir / "baseline", parsed_dir / "treatment", failed_dir):
        d.mkdir(parents=True, exist_ok=True)

    meta: dict = {
        "run_id": run_id,
        "model": args.model,
        "pin_model": pin_model,
        "temperature": 0,
        "expected_calls": n_expected,
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "calls": [],
        "complete": False,
        "primary_comparison_eligible": False,
    }
    successes = 0
    failures = 0

    for case in cases(manifest):
        for cond in ("baseline", "treatment"):
            prompt_path = BUILT / f"{case['id']}_{cond}.txt"
            if not prompt_path.is_file():
                print(f"missing prompt {prompt_path}", file=sys.stderr)
                return 2
            prompt = prompt_path.read_text(encoding="utf-8")
            print(f"calling {case['id']} {cond} ...", flush=True)
            raw_path = raw_dir / f"{case['id']}__{cond}.txt"
            parsed_path = parsed_dir / cond / f"{case['id']}.txt"

            try:
                text = call_openai(args.model, prompt)
                raw_path.write_text(text, encoding="utf-8")
                parsed_path.write_text(text, encoding="utf-8")
                status = {
                    "ok": True,
                    "status": "ok",
                    "case": case["id"],
                    "condition": cond,
                    "chars": len(text),
                }
                write_status(raw_path.with_suffix(".txt.status.json"), status)
                write_status(parsed_path.with_suffix(".txt.status.json"), status)
                err = None
                successes += 1
            except Exception as exc:  # noqa: BLE001
                err = f"{type(exc).__name__}: {exc}"
                print(f"  INFRA_ERROR: {err}", file=sys.stderr)
                body = f"# INFRA_ERROR: {err}\n# case={case['id']} condition={cond}\n"
                fail_path = failed_dir / f"{case['id']}__{cond}.txt"
                fail_path.write_text(body, encoding="utf-8")
                # Do NOT write success-shaped empty outputs into parsed/
                status = {
                    "ok": False,
                    "status": "infra_error",
                    "error": err,
                    "case": case["id"],
                    "condition": cond,
                    "failed_attempt": str(fail_path.relative_to(run_dir)),
                }
                write_status(fail_path.with_suffix(".txt.status.json"), status)
                # marker in parsed so missing vs failed is explicit
                marker = parsed_dir / cond / f"{case['id']}.INFRA_ERROR.txt"
                marker.write_text(body, encoding="utf-8")
                write_status(marker.with_suffix(".txt.status.json"), status)
                failures += 1

            meta["calls"].append(
                {
                    "id": case["id"],
                    "condition": cond,
                    "ok": err is None,
                    "status": "ok" if err is None else "infra_error",
                    "error": err,
                    "raw": str(raw_path.relative_to(run_dir)) if err is None else None,
                }
            )

    meta["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    meta["successful_calls"] = successes
    meta["failures"] = failures
    meta["complete"] = successes == n_expected and failures == 0
    meta["primary_comparison_eligible"] = meta["complete"]
    write_status(run_dir / "RUN_META.json", meta)

    if meta["complete"]:
        write_status(
            PRIMARY_POINTER,
            {
                "run_id": run_id,
                "run_dir": str(run_dir.relative_to(ROOT)),
                "model": args.model,
                "expected_calls": n_expected,
                "successful_calls": successes,
            },
        )
        print(f"PRIMARY comparison eligible: {run_dir}")
        print(f"wrote {PRIMARY_POINTER}")
    else:
        print(
            f"INCOMPLETE: {successes}/{n_expected} succeeded, {failures} failed. "
            f"Not eligible for primary baseline-vs-treatment comparison.",
            file=sys.stderr,
        )
        print(f"Failed attempts retained under: {failed_dir}")

    print(f"wrote {run_dir / 'RUN_META.json'}")
    print("Next: python score_holdout.py  # uses PRIMARY_RUN if complete")
    return 0 if meta["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
