# Discussion on PR/Issue #1793

## Issue comments (1)

### @codecov[bot] (2026-04-15T16:55:46Z)

## [Codecov](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1793?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) Report
:white_check_mark: All modified and coverable lines are covered by tests.
:white_check_mark: Project coverage is 72.52%. Comparing base ([`ba151af`](https://app.codecov.io/gh/riscv/riscv-unified-db/commit/ba151afcb205e7366d3ae50f4d0eb3e2c11e5d85?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv)) to head ([`457c52f`](https://app.codecov.io/gh/riscv/riscv-unified-db/commit/457c52f5ad2a34193009de2a9f8cf061bb7b3f98?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv)).
:warning: Report is 48 commits behind head on main.

<details><summary>Additional details and impacted files</summary>



```diff
@@            Coverage Diff             @@
##             main    #1793      +/-   ##
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

| [Flag](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1793/flags?src=pr&el=flags&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | Coverage Δ | |
|---|---|---|
| [idlc](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1793/flags?src=pr&el=flag&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | `76.08% <ø> (+0.11%)` | :arrow_up: |
| [udb](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1793/flags?src=pr&el=flag&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | `67.15% <ø> (+1.35%)` | :arrow_up: |

Flags with carried forward coverage won't be shown. [Click here](https://docs.codecov.io/docs/carryforward-flags?utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv#carryforward-flags-in-the-pull-request-comment) to find out more.
</details>

[:umbrella: View full report in Codecov by Sentry](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1793?dropdown=coverage&src=pr&el=continue&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv).   
:loudspeaker: Have feedback on the report? [Share it here](https://about.codecov.io/codecov-pr-comment-feedback/?utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv).
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
- :package: [JS Bundle Analysis](https://docs.codecov.com/docs/javascript-bundle-analysis): Save yourself from yourself by tracking and limiting bundle sizes in JS merges.
</details>

## Review line comments (1)

### @miguelcsx on param_extraction/scripts/run_prompt.py:141

```suggestion
        "Analyze the following specification text and extract all architectural parameters.",
        "Use overlap text only as context; avoid re-extracting a parameter when its defining sentence appears entirely in a previous chunk.",
        "Include line numbers relative to the original file (starting from "
        f"line {meta['start_line']}).",
```

