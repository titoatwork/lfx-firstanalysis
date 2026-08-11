"""The coding-challenge model figures must equal what the raw outputs say.

`coding-challenge/LLM-DETAILS.md` and `SUBMISSION.md` publish three numbers about
ten models on two snippets: how many hallucinated on the CSR negative control,
how many under-extracted the CMO snippet, and how many got both fully right.
Until 2026-08-11 those numbers were prose. The pack shipped no raw outputs and no
scorer, so a reader had to take the matrix on trust, which is exactly what the
rest of this repository refuses to ask for.

This re-derives all three from `challenge/results/live/`, the raw per-model
responses, and holds the published prose to them. It needs no network and no API
key: the model calls happened once, on 2026-07-26, and their outputs are
committed.

One number is deliberately not equal. The scorer counts a model that returned no
output for the CSR snippet as passing the control, giving 4 fully right.
LLM-DETAILS.md publishes 3, on the rule that emitting nothing is not the same as
answering zero. Both are correct under their own rule; this script checks that
the stricter published figure differs from the scorer by exactly the caveat rows
and no others, so the two can never drift apart silently.

  python check_challenge_matrix.py

Exit 0 agree, 1 mismatch, 2 could not parse, 3 artifacts absent.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "riscv-param-extraction" / "challenge" / "results" / "live"
SCORER_DIR = ROOT / "riscv-param-extraction" / "challenge" / "scripts"
DETAILS = ROOT / "coding-challenge" / "LLM-DETAILS.md"
SUBMISSION = ROOT / "coding-challenge" / "SUBMISSION.md"

# "**Totals: 4 of 10 hallucinated on the CSR snippet. 5 of 10 under-extracted the
#  CMO snippet. 3 of 10 got both fully right.**"
TOTALS = re.compile(
    r"(\d+) of (\d+) hallucinated on the CSR snippet\.\s*"
    r"(\d+) of \d+ under-extracted the\s*\n?\s*CMO snippet\.\s*"
    r"(\d+) of \d+ got both fully right",
    re.S,
)
# SUBMISSION.md restates the CSR figure twice, in prose and in the anti-hallucination list.
SUB_CSR = re.compile(r"\*\*(\d+) of 10 models invented at least one parameter")
SUB_CSR2 = re.compile(r"then measured: (\d+) of 10 models fail it")


def die(msg: str, code: int) -> None:
    print(msg)
    raise SystemExit(code)


def main() -> int:
    if not LIVE.is_dir():
        die(f"challenge artifacts not found at {LIVE}", 3)

    sys.path.insert(0, str(SCORER_DIR))
    try:
        from score_live_matrix import score_model_dir  # type: ignore
    except Exception as exc:  # pragma: no cover
        die(f"could not import the scorer: {exc}", 2)

    rows = [
        score_model_dir(d)
        for d in sorted(LIVE.iterdir())
        if d.is_dir() and not d.name.startswith("_")
    ]
    if not rows:
        die("no model directories scored", 3)

    scored = len(rows)
    csr_fail = [r for r in rows if r["csr_pass"] is False]
    under = [r for r in rows if r["cmo_count"] < 3]
    strong = [r for r in rows if r["cmo_count"] >= 3 and r["csr_pass"] is True]

    # A caveat row passed the control by returning nothing rather than by answering
    # zero. The curated directory cannot show this: it writes the same
    # NO_PARAMETERS_FOUND marker either way. The distinction is only in the raw
    # capture, where such a run reads "(No output)" while a real refusal carries
    # the model's reasoning. Directory names drop the vendor prefix that the raw
    # filenames carry, so match on a normalized form.
    def key(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", s.lower())

    raws = [(key(p.name[: -len("__csr.txt")]), p) for p in (LIVE / "_raw").glob("*__csr.txt")]
    caveat = []
    for r in strong:
        k = key(r["model"])
        hits = [p for rk, p in raws if k in rk]
        if len(hits) != 1:
            die(f"raw CSR capture for {r['model']}: {len(hits)} matches, expected 1", 3)
        if hits[0].read_text(encoding="utf8", errors="ignore").strip().lower().startswith("(no output"):
            caveat.append(r)

    text = DETAILS.read_text(encoding="utf8")
    m = TOTALS.search(text)
    if not m:
        die("could not parse the totals line in LLM-DETAILS.md", 2)
    pub_csr, pub_n, pub_under, pub_strong = (int(g) for g in m.groups())

    sub = SUBMISSION.read_text(encoding="utf8")
    subs = [p.search(sub) for p in (SUB_CSR, SUB_CSR2)]
    if not all(subs):
        die("could not parse the CSR figures in SUBMISSION.md", 2)
    sub_csr = {int(s.group(1)) for s in subs}  # type: ignore[union-attr]

    print(f"models scored from raw outputs   {scored}")
    print(f"  hallucinated on CSR control    {len(csr_fail)}  {[r['model'] for r in csr_fail]}")
    print(f"  under-extracted CMO            {len(under)}")
    print(f"  fully right, scorer rule       {len(strong)}")
    print(f"  ...of which caveat rows        {len(caveat)}  {[r['model'] for r in caveat]}")
    print(f"  fully right, published rule    {len(strong) - len(caveat)}")
    print()
    print(f"LLM-DETAILS.md publishes         {pub_csr} / {pub_under} / {pub_strong} of {pub_n}")
    print(f"SUBMISSION.md CSR figure         {sorted(sub_csr)}")
    print()

    bad = []
    if pub_n != scored:
        bad.append(f"model count: page says {pub_n}, artifacts have {scored}")
    if pub_csr != len(csr_fail):
        bad.append(f"CSR hallucinations: page says {pub_csr}, artifacts say {len(csr_fail)}")
    if pub_under != len(under):
        bad.append(f"under-extraction: page says {pub_under}, artifacts say {len(under)}")
    if pub_strong != len(strong) - len(caveat):
        bad.append(
            f"fully right: page says {pub_strong}, artifacts say "
            f"{len(strong)} minus {len(caveat)} caveat = {len(strong) - len(caveat)}"
        )
    if sub_csr != {len(csr_fail)}:
        bad.append(f"SUBMISSION.md CSR figure {sorted(sub_csr)} != {len(csr_fail)}")

    if bad:
        for b in bad:
            print(f"  {b}")
        print("\nFAIL  the published matrix disagrees with the raw outputs")
        return 1

    print("ok  every published model figure re-derives from the committed raw outputs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
