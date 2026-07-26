#!/usr/bin/env python3
"""
Optional live extract runner for challenge snippets.

Default: print rendered v3 prompt (no network).
Live: --live with a provider key (never commit keys).

Providers:
  openai      OPENAI_API_KEY
  anthropic   ANTHROPIC_API_KEY
  openrouter  OPENROUTER_API_KEY
  groq        GROQ_API_KEY

Usage:
  python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt
  python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt \\
      --live --provider anthropic --model claude-sonnet-4-20250514
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_V3 = (ROOT / "prompts" / "v3_schema_constrained.md").read_text(encoding="utf-8")


def render_prompt(snippet_text: str) -> str:
    if "```text" in PROMPT_V3:
        body = PROMPT_V3.split("```text", 1)[1].split("```", 1)[0].strip()
    else:
        body = PROMPT_V3
    return body.replace("{{SNIPPET}}", snippet_text.strip())


def call_openai(model: str, prompt: str, base_url: str | None = None, api_key: str | None = None) -> str:
    from openai import OpenAI

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    kwargs = {"api_key": key}
    if base_url:
        kwargs["base_url"] = base_url
    client = OpenAI(**kwargs)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content or ""


def call_anthropic(model: str, prompt: str) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError("pip install anthropic") from exc
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    parts = []
    for block in msg.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "".join(parts)


def live_call(provider: str, model: str, prompt: str) -> str:
    p = provider.lower()
    if p == "openai":
        return call_openai(model, prompt)
    if p == "anthropic":
        return call_anthropic(model, prompt)
    if p == "openrouter":
        key = os.environ.get("OPENROUTER_API_KEY")
        return call_openai(
            model,
            prompt,
            base_url="https://openrouter.ai/api/v1",
            api_key=key,
        )
    if p == "groq":
        key = os.environ.get("GROQ_API_KEY")
        return call_openai(
            model,
            prompt,
            base_url="https://api.groq.com/openai/v1",
            api_key=key,
        )
    raise RuntimeError(f"unknown provider {provider!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snippet", type=Path, required=True)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--provider", default="openai", help="openai|anthropic|openrouter|groq")
    parser.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument("--out", type=Path, default=None, help="Write raw response to file")
    args = parser.parse_args()

    if args.retries != 0:
        print("Refusing non-zero retries (campaign rule --retries 0).", file=sys.stderr)
        return 2

    snippet_path = args.snippet
    if not snippet_path.is_file():
        snippet_path = ROOT / args.snippet
    if not snippet_path.is_file():
        print(f"snippet not found: {args.snippet}", file=sys.stderr)
        return 2

    text = snippet_path.read_text(encoding="utf-8")
    prompt = render_prompt(text)

    if not args.live:
        print(prompt)
        print(
            "\n# Dry-run. Re-run with --live and a provider key "
            "(OPENAI_API_KEY / ANTHROPIC_API_KEY / OPENROUTER_API_KEY / GROQ_API_KEY).",
            file=sys.stderr,
        )
        return 0

    try:
        out = live_call(args.provider, args.model, prompt)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(out, encoding="utf-8")
        print(f"wrote {args.out}", file=sys.stderr)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
