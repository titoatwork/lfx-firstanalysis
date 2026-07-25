#!/usr/bin/env python3
"""
Optional live extract runner for challenge snippets.

Does NOT call any API unless OPENAI_API_KEY (or future providers) is set and
the user passes --live. Default mode prints the rendered v3 prompt for paste.

Usage:
  python scripts/extract.py --snippet snippets/cmo_cache_block.txt
  python scripts/extract.py --snippet snippets/cmo_cache_block.txt --live --model gpt-4o-mini
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_V3 = (ROOT / "prompts" / "v3_schema_constrained.md").read_text(encoding="utf-8")


def render_prompt(snippet_text: str) -> str:
    # Extract fenced template body if present
    if "```text" in PROMPT_V3:
        body = PROMPT_V3.split("```text", 1)[1].split("```", 1)[0].strip()
    else:
        body = PROMPT_V3
    return body.replace("{{SNIPPET}}", snippet_text.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snippet", type=Path, required=True)
    parser.add_argument("--live", action="store_true", help="Call OpenAI API (requires key)")
    parser.add_argument("--model", default="gpt-4o-mini-2024-07-18")
    parser.add_argument("--retries", type=int, default=0)
    args = parser.parse_args()

    if args.retries != 0:
        print("Refusing non-zero retries (campaign rule --retries 0).", file=sys.stderr)
        return 2

    snippet_path = args.snippet
    if not snippet_path.is_file():
        snippet_path = ROOT / args.snippet
    text = snippet_path.read_text(encoding="utf-8")
    prompt = render_prompt(text)

    if not args.live:
        print(prompt)
        print("\n# Dry-run only. Re-run with --live and OPENAI_API_KEY to call the API.", file=sys.stderr)
        return 0

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set", file=sys.stderr)
        return 2

    try:
        from openai import OpenAI
    except ImportError:
        print("pip install openai", file=sys.stderr)
        return 2

    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    print(resp.choices[0].message.content or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
