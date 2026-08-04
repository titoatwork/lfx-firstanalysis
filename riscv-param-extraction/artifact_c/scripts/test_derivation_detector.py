#!/usr/bin/env python3
"""Check the IDL derivation detector against both repository states.

The H5 rubric records an evidence type per label, and an evidence type is only
meaningful with a commit attached: `.udb-corpus` is a fork pinned at `c184e313`
that predates upstream changes to the very derivations being labelled. This
test asserts the claims written into ../PREREGISTRATION.md and
../../docs/metrics.md rather than leaving them as prose:

  at corpus pin c184e313   FLEN is `U32 FLEN = 64;`, a literal-valued global,
                           so NOT executable evidence
  on origin/main           FLEN is `U32 FLEN = implemented?(...) ? ... : ...;`,
                           so executable evidence
  both states              IALIGN is a function; ILEN has no declaration at all

It also pins the defect that prompted the fix: the previous detector read
`globals.isa` alone and matched `function <name>` alone, so it reported FLEN as
non-executable on main, where the answer is executable.

Needs a `riscv-unified-db` clone beside this repository, since it reads history
via `git show`. Without one it SKIPS and says so; it never passes silently.

Exit 0 = every claim holds.
Exit 1 = a claim in the documents disagrees with the repository.
Exit 3 = skipped, no UDB clone. Callers must report this as skipped, not passed.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_h5 import UDB_MAIN, idl_derivation  # noqa: E402

CORPUS_PIN = "c184e3135ea60fe73d6bcec56cef2c3ac09ca18d"
ISA = "spec/std/isa/isa"
# globals.isa and every file it includes, as of both revisions under test.
FILES = ("globals.isa", "builtin_functions.idl", "interrupts.idl",
         "fetch.idl", "util.idl", "fp.idl", "vec.idl")

EXPECTED = {
    CORPUS_PIN: {"IALIGN": "function", "FLEN": "constant", "ILEN": None},
    "origin/main": {"IALIGN": "function", "FLEN": "global", "ILEN": None},
}


def show(rev: str, path: str) -> str | None:
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=UDB_MAIN,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return r.stdout if r.returncode == 0 else None


def tree_at(rev: str) -> str:
    return "\n".join(s for f in FILES if (s := show(rev, f"{ISA}/{f}")) is not None)


def old_detector(name: str, globals_src: str) -> bool:
    """The detector as it was before 2026-08-05: one file, one form."""
    return bool(re.search(r"function\s+" + re.escape(name.lower()) + r"\s*\{",
                          globals_src))


def main() -> int:
    if not (UDB_MAIN / ".git").exists():
        print(f"SKIP  no riscv-unified-db clone at {UDB_MAIN}")
        print("      this check reads UDB history; it is not run here, and is")
        print("      reported as skipped rather than counted as a pass")
        return 3
    if show(CORPUS_PIN, f"{ISA}/globals.isa") is None:
        print(f"SKIP  clone does not contain corpus pin {CORPUS_PIN[:8]}")
        return 3

    fails: list[str] = []
    for rev, want in EXPECTED.items():
        src = tree_at(rev)
        label = "corpus pin c184e313" if rev == CORPUS_PIN else "origin/main"
        print(f"{label}:")
        for name, expect in sorted(want.items()):
            got = idl_derivation(name, src)
            executable = got in ("function", "global")
            ok = got == expect
            print(f"  {name:<8} {str(got):<10} "
                  f"{'executable' if executable else 'TODO-human':<12}"
                  f"{'' if ok else '  MISMATCH, documents say ' + str(expect)}")
            if not ok:
                fails.append(f"{label}: {name} is {got}, documents say {expect}")

    # The recorded labels were produced at the pin. If FLEN ever reads as
    # executable there, the committed labels move and the amendment is wrong.
    if idl_derivation("FLEN", tree_at(CORPUS_PIN)) in ("function", "global"):
        fails.append("FLEN reads as executable at the pin; recorded labels would move")

    g_main = show("origin/main", f"{ISA}/globals.isa") or ""
    if old_detector("FLEN", g_main):
        fails.append("old detector finds FLEN on main; the stated defect is not real")
    if idl_derivation("FLEN", tree_at("origin/main")) not in ("function", "global"):
        fails.append("new detector misses FLEN on main; the fix does not work")

    if fails:
        print("\nFAILED:")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("\nok  evidence types match the repository at both pinned states,")
    print("    and the fixed detector finds on main what the old one missed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
