#!/usr/bin/env python3
"""
Four-arm runner for Artifact C. See ../PREREGISTRATION.md.

Arms vary two binary factors and nothing else:

    arm  name list  CSR context   purpose
    A    yes        no            reproduces the published condition (control)
    B    no         no            discovery recall, the unmeasured number
    C    yes        yes           the originally registered context question
    D    no         yes           does context substitute for the catalogue

The baseline user message is assembled from the Part I corpus's own helpers so
arm A is byte-identical to the published runs. Removing the name list is the
only difference in B, and context is appended after the chunk in C and D.

Retention is a gate, not a convenience (PREREGISTRATION §6b). Every call writes
its raw response before parsing. A run that cannot write its artifacts aborts.

Nothing is sent anywhere without --live. --dry-run resolves and writes prompts
so the arms can be diffed without spending anything.

Usage:
  python run_arms.py --dry-run --udb-root ../../../.udb-corpus
  python run_arms.py --live --model gpt-4o-mini-2024-07-18 --arms A B
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTEXT_DIR = ROOT / "contexts"
RUNS_DIR = ROOT / "runs"

ARMS = {
    "A": {"names": True, "context": False, "label": "names, no context (control)"},
    "B": {"names": False, "context": False, "label": "no names, no context (discovery)"},
    "C": {"names": True, "context": True, "label": "names + context"},
    "D": {"names": False, "context": True, "label": "no names + context"},
}

# Pinned snapshots. Recorded into every run manifest.
MODELS = {
    "gpt-4o-2024-11-20": {"provider": "openai", "env": "OPENAI_API_KEY"},
    "gpt-4o-mini-2024-07-18": {"provider": "openai", "env": "OPENAI_API_KEY"},
    "gemini-3.6-flash": {"provider": "google", "env": "GEMINI_API_KEY"},
    "nvidia/nemotron-3-ultra-550b-a55b:free": {"provider": "openrouter", "env": "OPENROUTER_API_KEY"},
    "inclusionai/ling-3.0-flash:free": {"provider": "openrouter", "env": "OPENROUTER_API_KEY"},
}


@dataclass
class CallRecord:
    chunk_id: str
    arm: str
    model: str
    ok: bool
    error: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: int = 0
    n_parsed: int = 0
    parse_failed: bool = False
    refused: bool = False


def load_corpus_helpers(udb: Path):
    """Use the Part I corpus's own prompt assembly so arm A matches published runs.

    extract.py is the production builder: build_user_message() there joins
    examples + param names + _format_chunk() with "\\n\\n---\\n\\n". We reuse the
    same pieces so arm A differs from the published prompt in nothing.
    """
    scripts = udb / "param_extraction" / "scripts"
    if not scripts.exists():
        raise SystemExit(f"corpus scripts not found: {scripts}")
    sys.path.insert(0, str(scripts))
    import run_prompt as rp  # noqa: E402
    import extract as ex  # noqa: E402
    return rp, ex


def load_chunk_meta(udb: Path) -> dict[str, dict]:
    """Real per-chunk metadata from stored run records, not model output."""
    out: dict[str, dict] = {}
    res = udb / "param_extraction" / "results" / "v2" / "claude-sonnet-4"
    for f in sorted(res.glob("chunk_*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        out[d["chunk_id"]] = {
            "source_file": d.get("source_file", ""),
            "start_line": d.get("start_line", 0),
            "end_line": d.get("end_line", 0),
            "content_start_line": d.get("content_start_line", d.get("start_line", 0)),
        }
    return out


def build_user_message(rp, ex, chunk_text: str, meta: dict, include_names: bool,
                       context: str | None) -> str:
    parts = [rp.format_examples_section(rp.load_examples())]
    if include_names:
        parts.append(rp.format_param_names_section(rp.load_udb_param_names()))
    parts.append(ex._format_chunk(chunk_text, meta))
    if context:
        parts.append(context)
    return "\n\n---\n\n".join(parts)


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def parse_params(raw: str) -> tuple[list, bool]:
    """Extract the parameters list. Returns (params, parse_failed)."""
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.S)
    blob = m.group(1) if m else raw
    try:
        d = json.loads(blob)
    except Exception:
        start = blob.find("{")
        end = blob.rfind("}")
        if start < 0 or end <= start:
            return [], True
        try:
            d = json.loads(blob[start:end + 1])
        except Exception:
            return [], True
    if not isinstance(d, dict):
        return [], True
    return d.get("parameters") or [], False


def call_openai(model: str, system: str, user: str) -> dict:
    from openai import OpenAI
    client = OpenAI()
    t0 = time.time()
    r = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return {
        "text": r.choices[0].message.content or "",
        "in": r.usage.prompt_tokens,
        "out": r.usage.completion_tokens,
        "ms": int((time.time() - t0) * 1000),
    }


DISPATCH = {"openai": call_openai}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--udb-root", type=Path, default=Path("../../../.udb-corpus"))
    ap.add_argument("--arms", nargs="+", default=list(ARMS), choices=list(ARMS))
    ap.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    ap.add_argument("--limit", type=int, default=0, help="first N chunks only (smoke test)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--live", action="store_true")
    args = ap.parse_args()

    udb = args.udb_root.resolve()
    rp, ex = load_corpus_helpers(udb)
    system = rp.load_system_prompt()
    metas = load_chunk_meta(udb)

    inv = json.loads((ROOT.parent / "results" / "artifact_a_chunk_inventory.json")
                     .read_text(encoding="utf-8"))
    scored = [c["chunk_id"] for c in inv["chunks"]]
    if args.limit:
        scored = scored[: args.limit]

    if args.model not in MODELS:
        print(f"unknown model {args.model}", file=sys.stderr)
        return 2
    spec = MODELS[args.model]

    if args.live:
        if not os.environ.get(spec["env"]):
            print(f"{spec['env']} not set in the environment. Refusing to run.", file=sys.stderr)
            print("Set it in your shell, do not paste it into a transcript.", file=sys.stderr)
            return 2
        if spec["provider"] not in DISPATCH:
            print(f"provider {spec['provider']} not wired yet", file=sys.stderr)
            return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS_DIR / f"{stamp}_{args.model.replace('/', '_').replace(':', '_')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": run_dir.name,
        "started_utc": stamp,
        "mode": "live" if args.live else "dry-run",
        "model": args.model,
        "provider": spec["provider"],
        "temperature": 0,
        "arms": {a: ARMS[a] for a in args.arms},
        "corpus_chunks": len(scored),
        "udb_root": str(udb),
        "system_prompt_sha": sha(system),
        "preregistration": "../PREREGISTRATION.md",
    }

    records: list[CallRecord] = []
    for arm in args.arms:
        cfg = ARMS[arm]
        arm_dir = run_dir / f"arm_{arm}"
        (arm_dir / "raw").mkdir(parents=True, exist_ok=True)
        (arm_dir / "parsed").mkdir(parents=True, exist_ok=True)
        first_prompt_written = False

        for cid in scored:
            cpath = udb / "param_extraction" / "chunks" / f"{cid}.txt"
            if not cpath.exists():
                records.append(CallRecord(cid, arm, args.model, False, "chunk missing"))
                continue
            ctext = cpath.read_text(encoding="utf-8", errors="replace")

            context = None
            if cfg["context"]:
                cf = CONTEXT_DIR / f"{cid}.md"
                context = cf.read_text(encoding="utf-8") if cf.exists() else None

            meta = metas.get(cid)
            if meta is None:
                records.append(CallRecord(cid, arm, args.model, False, "no chunk metadata"))
                continue
            user = build_user_message(rp, ex, ctext, meta, cfg["names"], context)

            # retention: one fully resolved prompt per arm, so arms can be diffed later
            if not first_prompt_written:
                (arm_dir / "RESOLVED_PROMPT_SAMPLE.txt").write_text(
                    f"### chunk {cid}\n### arm {arm}: {cfg['label']}\n"
                    f"### system sha {sha(system)}\n### user sha {sha(user)}\n\n"
                    f"=== SYSTEM ===\n{system}\n\n=== USER ===\n{user}",
                    encoding="utf-8")
                first_prompt_written = True

            if args.dry_run:
                records.append(CallRecord(cid, arm, args.model, True,
                                          input_tokens=len(user) // 4))
                continue

            try:
                res = DISPATCH[spec["provider"]](args.model, system, user)
            except Exception as e:  # retention before anything else
                (arm_dir / "raw" / f"{cid}.ERROR.txt").write_text(str(e), encoding="utf-8")
                records.append(CallRecord(cid, arm, args.model, False, str(e)[:300]))
                continue

            (arm_dir / "raw" / f"{cid}.txt").write_text(res["text"], encoding="utf-8")
            params, failed = parse_params(res["text"])
            (arm_dir / "parsed" / f"{cid}.json").write_text(
                json.dumps({"chunk_id": cid, "arm": arm, "model": args.model,
                            "parameters": params}, indent=2), encoding="utf-8")
            records.append(CallRecord(
                cid, arm, args.model, True, "", res["in"], res["out"], res["ms"],
                len(params), failed,
                refused=bool(re.search(r"\bI (?:can't|cannot|won't)\b", res["text"][:400], re.I)),
            ))
            print(f"  {arm} {cid}: {len(params)} params, {res['in']}+{res['out']} tok")

    manifest["calls"] = [asdict(r) for r in records]
    manifest["totals"] = {
        "calls": len(records),
        "ok": sum(1 for r in records if r.ok),
        "failed": sum(1 for r in records if not r.ok),
        "parse_failures": sum(1 for r in records if r.parse_failed),
        "refusals": sum(1 for r in records if r.refused),
        "input_tokens": sum(r.input_tokens for r in records),
        "output_tokens": sum(r.output_tokens for r in records),
    }
    (run_dir / "RUN_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\nrun dir: {run_dir}")
    for k, v in manifest["totals"].items():
        print(f"  {k:<16} {v}")
    if args.dry_run:
        print("\ndry run. no API calls were made, no key was read.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
