"""Unit tests for the two publication gates (no API, no network).

Both gates were extended after they let a defect through, and both were checked
by hand at the time by breaking the document on purpose. These tests make that
permanent, against fixture text rather than the live documents, so they keep
testing the rule after the real counts move.

  check_census.py         the census table and the reviewer summary must agree
  check_pinned_wording.py 223 may not be described as a live count
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_census  # noqa: E402
import check_pinned_wording  # noqa: E402


def summary_line(merged: int, open_: int, issues: int) -> str:
    return (f"| **What was contributed** | **{merged} merged** upstream PRs, "
            f"**{open_}** open, **{issues}** issues filed, review comments |")


def census_table(merged: int, open_: int, issues: int) -> str:
    return (f"| Merged PRs authored | **{merged}** |\n"
            f"| Open PRs authored | **{open_}** |\n"
            f"| Issues authored | **{issues}** |\n")


class CensusSummaryTests(unittest.TestCase):
    """The drift that went unnoticed: summary said 8/5/13, table said 8/6/14."""

    def test_summary_counts_are_read(self) -> None:
        found = check_census.SUMMARY.findall(summary_line(8, 6, 14))
        self.assertEqual(found, [("8", "6", "14")])

    def test_table_counts_are_read(self) -> None:
        text = census_table(9, 5, 14)
        got = {k: int(p.findall(text)[0]) for k, p in check_census.COUNT_ROWS.items()}
        self.assertEqual(got, {"merged": 9, "open": 5, "issues": 14})

    def test_the_historical_drift_is_detectable(self) -> None:
        table = {k: int(p.findall(census_table(8, 6, 14))[0])
                 for k, p in check_census.COUNT_ROWS.items()}
        merged, open_, issues = check_census.SUMMARY.findall(summary_line(8, 5, 13))[0]
        summary = {"merged": int(merged), "open": int(open_), "issues": int(issues)}
        disagreeing = [k for k in table if table[k] != summary[k]]
        self.assertEqual(sorted(disagreeing), ["issues", "open"])

    def test_agreement_produces_no_disagreement(self) -> None:
        table = {k: int(p.findall(census_table(8, 6, 14))[0])
                 for k, p in check_census.COUNT_ROWS.items()}
        merged, open_, issues = check_census.SUMMARY.findall(summary_line(8, 6, 14))[0]
        summary = {"merged": int(merged), "open": int(open_), "issues": int(issues)}
        self.assertEqual([k for k in table if table[k] != summary[k]], [])


class CensusIssueStateTests(unittest.TestCase):
    """2.3 carried #2364 as open for a day after #2384 closed it."""

    FIXTURE = (
        "### 2.3 Issues filed by titoatwork (2)\n\n"
        "| Issue | State | Topic |\n"
        "|-------|-------|--------|\n"
        "| [#2137](https://example/issues/2137) | closed | schema defect |\n"
        "| [#2364](https://example/issues/2364) | open | senvcfg length |\n\n"
        "### 2.4 Something else\n"
    )

    def test_states_are_parsed_with_their_numbers(self) -> None:
        self.assertEqual(check_census.claimed_issue_states(self.FIXTURE),
                         [(2137, "closed"), (2364, "open")])

    def test_a_stale_state_is_a_mismatch(self) -> None:
        claimed = dict(check_census.claimed_issue_states(self.FIXTURE))
        live = {2137: "closed", 2364: "closed"}
        wrong = [n for n, c in claimed.items() if live[n] != c]
        self.assertEqual(wrong, [2364])

    def test_no_2_3_section_is_not_a_crash(self) -> None:
        self.assertEqual(check_census.claimed_issue_states("# nothing here\n"), [])


class PinnedWordingTests(unittest.TestCase):
    """223 is the corpus-pin count. docs/FAQ.md called it live and passed."""

    def banned_hits(self, line: str) -> list[str]:
        return [why for pat, why in check_pinned_wording.BANNED
                if re.search(pat, line, re.I)]

    def test_the_phrasing_that_slipped_through_is_caught(self) -> None:
        self.assertTrue(self.banned_hits("grew from 185 pinned parameters to 223 live ones."))

    def test_reversed_order_is_caught(self) -> None:
        self.assertTrue(self.banned_hits("the live 223 parameter set"))

    def test_the_original_two_patterns_still_fire(self) -> None:
        self.assertTrue(self.banned_hits("measured against live UDB"))
        self.assertTrue(self.banned_hits("scored against live GT223"))

    def test_naming_the_pin_is_allowed(self) -> None:
        self.assertEqual(
            self.banned_hits("the **223** UDB carried at corpus pin `c184e313`"), [])

    def test_the_sentence_that_states_the_correction_is_allowed(self) -> None:
        # A wider window than adjacency flags this, which would make the
        # correction unstateable. Guarding against that regression.
        self.assertEqual(
            self.banned_hits("223 is the count at that pin and not a live figure"), [])


if __name__ == "__main__":
    unittest.main()
