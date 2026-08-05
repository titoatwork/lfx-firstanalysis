#!/usr/bin/env python3
"""Fail if a pinned measurement is described as if it came from live UDB.

Twice now a number measured against one repository state has been published as
a statement about the repository:

  FLEN   labelled documented-only evidence, true at corpus pin `c184e313` and
         false on `main` since `e9be82db` (2026-05-08)
  GT223  described as "live UDB", when 223 is the corpus-pin parameter count
         and `main` carried 227 on the day the claim was posted

Both were locally true and globally wrong. The shared cause is a claim about a
pinned tree written without naming the pin, so this checks the wording rather
than trusting anyone to remember. `.udb-corpus` forked from `main` at
`ba151afc` (2026-04-02) and is hundreds of commits behind it, so "live" and
"current" are never safe words for a figure derived from it.

Scope: documents only. It cannot know which number came from which tree, so it
bans the phrasings that assert currency and leaves the numbers alone.

Exit 0 = no banned phrasing. Exit 1 = something asserts currency it cannot have.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (pattern, why it is banned). Case-insensitive, matched per line.
BANNED = [
    (r"live\s+UDB",
     "223 is the corpus-pin count; main had 227 when this was first published"),
    (r"live\s+GT\s*223",
     "GT223 is the corpus-pin gold, not a live one"),
    (r"current\s+UDB\s+parameter\s+count",
     "say which commit, or say 'at pin <sha>'"),
    # The two above only catch the exact phrasings that were wrong the first time.
    # docs/FAQ.md then said "223 live ones", which is the same claim in words
    # neither pattern matched. Adjacency only, deliberately: a wider window flags
    # the sentence that does the correcting ("223 ... not a live figure"), and a
    # rule that punishes the correction is worse than the gap it closes.
    (r"\b223\s+live\b",
     "223 is the corpus-pin count; name the pin instead of calling it live"),
    (r"\blive\s+223\b",
     "223 is the corpus-pin count; name the pin instead of calling it live"),
]

# Historical records of things already said in public. Correcting these would
# falsify the archive; the correction belongs in the thread, not in the copy.
EXEMPT_DIRS = {"upstream-pr-drafts"}
# check_pinned_wording.py holds the patterns; test_gates.py holds the fixtures that
# prove they fire. Both must contain the banned phrasings to do their job.
EXEMPT_FILES = {"check_pinned_wording.py", "test_gates.py"}

SEARCH_GLOBS = ("*.md", "*.py")


def tracked_docs() -> list[Path]:
    out = []
    for pat in SEARCH_GLOBS:
        for p in ROOT.rglob(pat):
            parts = set(p.relative_to(ROOT).parts)
            if parts & EXEMPT_DIRS or p.name in EXEMPT_FILES:
                continue
            if ".git" in parts or "node_modules" in parts or "__pycache__" in parts:
                continue
            out.append(p)
    return sorted(out)


def main() -> int:
    hits = []
    for path in tracked_docs():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            # A line that is itself explaining the ban is not a violation.
            if "NEVER call this" in line or "was the wrong description" in line:
                continue
            for pat, why in BANNED:
                if re.search(pat, line, re.I):
                    hits.append((path.relative_to(ROOT), n, line.strip()[:90], why))

    if hits:
        print("pinned-wording check FAILED:")
        for rel, n, snippet, why in hits:
            print(f"  {rel}:{n}")
            print(f"    {snippet}")
            print(f"    why: {why}")
        print("\nName the commit the figure was measured at, or drop the word.")
        return 1

    print(f"ok  no figure claims currency it cannot have "
          f"({len(tracked_docs())} files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
