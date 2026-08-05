"""The published unique-thread count must equal the threads actually listed.

The census figure went wrong once by being counted by hand: EVIDENCE.md said 41
while the GitHub API said 43 and the tables on the same page enumerated 38. Three
numbers, no two agreeing, and nothing in the build noticed.

GitHub is the source of truth for the count, and refreshing it is a network job
documented in EVIDENCE.md 2.6. What runs here is the part that needs no network
and would still have caught that: the headline in EVIDENCE.md, the census row in
README.md, and the union of thread numbers listed in EVIDENCE.md 2.1-2.5 must be
the same number. A hand-typed count cannot survive that unless it is right.

  python check_census.py            offline consistency (what CI runs)
  python check_census.py --online   also diff the tables against the API

Exit 0 consistent, 1 mismatch, 2 could not parse.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs" / "EVIDENCE.md"
README = ROOT / "README.md"
REPO = "riscv/riscv-unified-db"

# "### 2.4 ..." opens a census table section; 2.6 is the how-to and holds no rows.
SECTION = re.compile(r"^###\s+2\.(\d)\b")
# First cell of a table row, e.g. "| [#2317](https://.../issues/2317) | ..."
ROW = re.compile(r"^\|\s*\[#(\d{3,6})\]")
HEADLINE = re.compile(r"\*\*(\d+)\*\*\s+unique issues\+PRs")
README_ROW = re.compile(r"\|\s*Unique issues and PRs involving this author\s*\|\s*\*\*(\d+)\*\*\s*\|")

# The census table in README.md carries the three authored counts one per row.
COUNT_ROWS = {
    "merged": re.compile(r"\|\s*Merged PRs authored\s*\|\s*\*\*(\d+)\*\*\s*\|"),
    "open": re.compile(r"\|\s*Open PRs authored\s*\|\s*\*\*(\d+)\*\*\s*\|"),
    "issues": re.compile(r"\|\s*Issues authored\s*\|\s*\*\*(\d+)\*\*\s*\|"),
}
# The reviewer summary at the top of README.md restates the same three numbers in
# prose. It drifted to "8 merged, 5 open, 13 issues" against a table saying 8/6/14,
# because nothing compared them. This is that comparison.
SUMMARY = re.compile(
    r"\*\*(\d+) merged\*\* upstream PRs, \*\*(\d+)\*\* open, \*\*(\d+)\*\* issues filed"
)


def listed_threads(text: str) -> tuple[set[int], dict[int, list[str]]]:
    """Thread numbers in the first column of the 2.1-2.5 tables, with their sections."""
    threads: set[int] = set()
    where: dict[int, list[str]] = {}
    section: str | None = None
    for line in text.splitlines():
        m = SECTION.match(line)
        if m:
            section = f"2.{m.group(1)}" if m.group(1) in "12345" else None
            continue
        if line.startswith("## "):
            section = None
            continue
        if section is None:
            continue
        m = ROW.match(line)
        if m:
            n = int(m.group(1))
            threads.add(n)
            where.setdefault(n, []).append(section)
    return threads, where


def one(pattern: re.Pattern[str], text: str, label: str) -> int:
    found = pattern.findall(text)
    if len(found) != 1:
        print(f"could not read {label}: {len(found)} matches, expected 1")
        raise SystemExit(2)
    return int(found[0])


def claimed_issue_states(text: str) -> list[tuple[int, str]]:
    """(number, state) from the second column of the 2.3 table."""
    m = re.search(r"^### 2\.3\b(.*?)(?=^### )", text, re.S | re.M)
    if not m:
        return []
    return [(int(n), s.lower())
            for n, s in re.findall(r"^\|\s*\[#(\d+)\]\([^)]*\)\s*\|\s*(\w+)\s*\|", m.group(1), re.M)]


def api_states(numbers: list[int]) -> dict[int, str] | None:
    """Live open/closed for each number. None if gh is unavailable."""
    if not shutil.which("gh") or not numbers:
        return None
    fields = " ".join(
        f"n{n}: issueOrPullRequest(number:{n}) "
        f"{{... on Issue {{state}} ... on PullRequest {{state}}}}" for n in numbers)
    query = f'{{repository(owner:"riscv",name:"riscv-unified-db"){{{fields}}}}}'
    try:
        out = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"],
                             capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"gh graphql failed: {exc}")
        return None
    if out.returncode != 0:
        print(f"gh graphql failed: {out.stderr.strip()}")
        return None
    try:
        node = json.loads(out.stdout)["data"]["repository"]
    except (ValueError, KeyError) as exc:
        print(f"could not parse gh graphql response: {exc}")
        return None
    return {int(k[1:]): v["state"].lower() for k, v in node.items() if v}


def api_threads() -> set[int] | None:
    """Unique threads per GitHub. None if gh is unavailable or the query fails."""
    if not shutil.which("gh"):
        return None
    nums: set[int] = set()
    for kind in ("issues", "prs"):
        cmd = ["gh", "search", kind, "--involves=titoatwork", f"--repo={REPO}",
               "--limit", "200", "--json", "number", "--jq", ".[].number"]
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"gh search {kind} failed: {exc}")
            return None
        if out.returncode != 0:
            print(f"gh search {kind} failed: {out.stderr.strip()}")
            return None
        nums |= {int(x) for x in out.stdout.split()}
    return nums


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--online", action="store_true",
                    help="also diff the listed threads against the GitHub API")
    args = ap.parse_args()

    evidence = EVIDENCE.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    listed, where = listed_threads(evidence)
    headline = one(HEADLINE, evidence, "the EVIDENCE.md census headline")
    readme_count = one(README_ROW, readme, "the README.md census row")

    print(f"EVIDENCE.md headline      {headline}")
    print(f"README.md census row      {readme_count}")
    print(f"threads listed in 2.1-2.5 {len(listed)}")

    dupes = {n: s for n, s in where.items() if len(s) > 1}
    if dupes:
        # Not an error: 2.3 and 2.5 legitimately list the same authored issue.
        print("  (listed twice, counted once: "
              + ", ".join(f"#{n} in {'+'.join(s)}" for n, s in sorted(dupes.items())) + ")")

    table = {k: one(p, readme, f"the README.md '{k}' census row") for k, p in COUNT_ROWS.items()}
    s = SUMMARY.findall(readme)
    if len(s) != 1:
        print(f"could not read the README.md reviewer summary counts: "
              f"{len(s)} matches, expected 1")
        raise SystemExit(2)
    summary = dict(zip(("merged", "open", "issues"), (int(x) for x in s[0])))

    print(f"README.md census table    merged {table['merged']}, "
          f"open {table['open']}, issues {table['issues']}")
    print(f"README.md reviewer summary merged {summary['merged']}, "
          f"open {summary['open']}, issues {summary['issues']}")

    bad = 0
    if headline != len(listed):
        print(f"\nMISMATCH  headline says {headline}, 2.1-2.5 list {len(listed)}")
        bad = 1
    if readme_count != headline:
        print(f"\nMISMATCH  README says {readme_count}, EVIDENCE.md says {headline}")
        bad = 1
    for k in ("merged", "open", "issues"):
        if table[k] != summary[k]:
            print(f"\nMISMATCH  README census table says {table[k]} {k}, "
                  f"the reviewer summary says {summary[k]}")
            bad = 1

    if args.online:
        live = api_threads()
        if live is None:
            print("\nonline check skipped: gh unavailable or query failed")
            return bad or 1
        missing = sorted(live - listed)
        extra = sorted(listed - live)
        print(f"\nGitHub API                {len(live)}")
        if missing:
            print("  listed nowhere: " + ", ".join(f"#{n}" for n in missing))
        if extra:
            print("  listed but not returned: " + ", ".join(f"#{n}" for n in extra))
        if missing or extra:
            bad = 1

        # A state column goes stale silently: #2364 read "open" for a day after
        # #2384 merged and closed it. Counts were unaffected, so nothing caught it.
        claimed = claimed_issue_states(evidence)
        live_states = api_states([n for n, _ in claimed])
        if live_states is None:
            print("  issue-state check skipped: gh graphql unavailable")
        else:
            wrong = [(n, c, live_states[n]) for n, c in claimed
                     if n in live_states and c != live_states[n]]
            print(f"\n2.3 issue states checked   {len(claimed)}")
            for n, c, live in wrong:
                print(f"  #{n} listed {c}, GitHub says {live}")
            if wrong:
                bad = 1

    print("\n" + ("FAIL  the census disagrees with itself" if bad
                  else "ok  every published census figure equals the threads listed"))
    return bad


if __name__ == "__main__":
    raise SystemExit(main())
