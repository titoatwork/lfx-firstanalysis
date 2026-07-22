# Discussion on PR/Issue #1792

## Issue comments (1)

### @codecov[bot] (2026-04-15T16:53:54Z)

## [Codecov](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1792?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) Report
:white_check_mark: All modified and coverable lines are covered by tests.
:white_check_mark: Project coverage is 72.52%. Comparing base ([`ba151af`](https://app.codecov.io/gh/riscv/riscv-unified-db/commit/ba151afcb205e7366d3ae50f4d0eb3e2c11e5d85?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv)) to head ([`99f9dad`](https://app.codecov.io/gh/riscv/riscv-unified-db/commit/99f9dad81c7d58e7dcb43739c0828bc396ed2d86?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv)).
:warning: Report is 48 commits behind head on main.

<details><summary>Additional details and impacted files</summary>



```diff
@@            Coverage Diff             @@
##             main    #1792      +/-   ##
==========================================
+ Coverage   71.95%   72.52%   +0.57%     
==========================================
  Files          55       53       -2     
  Lines       28085    27947     -138     
  Branches     6172     6031     -141     
==========================================
+ Hits        20209    20269      +60     
+ Misses       7876     7678     -198     
```

| [Flag](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1792/flags?src=pr&el=flags&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | Coverage Δ | |
|---|---|---|
| [idlc](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1792/flags?src=pr&el=flag&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | `76.08% <ø> (+0.11%)` | :arrow_up: |
| [udb](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1792/flags?src=pr&el=flag&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | `67.15% <ø> (+1.35%)` | :arrow_up: |

Flags with carried forward coverage won't be shown. [Click here](https://docs.codecov.io/docs/carryforward-flags?utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv#carryforward-flags-in-the-pull-request-comment) to find out more.
</details>

[:umbrella: View full report in Codecov by Sentry](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1792?dropdown=coverage&src=pr&el=continue&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv).   
:loudspeaker: Have feedback on the report? [Share it here](https://about.codecov.io/codecov-pr-comment-feedback/?utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv).
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
- :package: [JS Bundle Analysis](https://docs.codecov.com/docs/javascript-bundle-analysis): Save yourself from yourself by tracking and limiting bundle sizes in JS merges.
</details>

## Review line comments (2)

### @miguelcsx on param_extraction/scripts/analyze.py:

```suggestion
    already_aligned_llm = {a.llm_name for a in alignments if a.match_type != "none"}
    unmatched_udb = udb_names - matched_udb
    unmatched_llm = [p for p in deduped if p["parameter_name"] not in already_aligned_llm]
```

### @miguelcsx on param_extraction/scripts/analyze.py:

```suggestion
        if best_llm_name and best_score >= 0.4 and len(group_members) == 1:
            member = group_members[0]
            udb_info = udb_by_name[member]
            alignments.append(
                AlignmentEntry(
                    llm_name=best_llm_name,
                    udb_name=member,
                    match_type="concept_group",
                    match_score=round(best_score, 3),
                    llm_class=llm_by_name.get(best_llm_name, {}).get("class", ""),
                    udb_class=udb_info.get("classification"),
                    class_match=None,
                )
            )
            matched_udb.add(member)
```

