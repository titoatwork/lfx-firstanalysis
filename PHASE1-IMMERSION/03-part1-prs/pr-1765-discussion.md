# Discussion on PR/Issue #1765

## Issue comments (1)

### @codecov[bot] (2026-03-26T00:30:48Z)

## [Codecov](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1765?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) Report
:white_check_mark: All modified and coverable lines are covered by tests.
:white_check_mark: Project coverage is 71.95%. Comparing base ([`de41e7b`](https://app.codecov.io/gh/riscv/riscv-unified-db/commit/de41e7b9a9e0148d284e4c6c3b8bfe5ad5f3bb73?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv)) to head ([`9381f19`](https://app.codecov.io/gh/riscv/riscv-unified-db/commit/9381f19fcae6dcf3c49669f66a7df4a6c3c75394?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv)).

<details><summary>Additional details and impacted files</summary>



```diff
@@            Coverage Diff             @@
##             main    #1765      +/-   ##
==========================================
- Coverage   71.96%   71.95%   -0.01%     
==========================================
  Files          54       54              
  Lines       27976    27976              
  Branches     6183     6183              
==========================================
- Hits        20132    20131       -1     
- Misses       7844     7845       +1     
```

| [Flag](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1765/flags?src=pr&el=flags&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | Coverage Δ | |
|---|---|---|
| [idlc](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1765/flags?src=pr&el=flag&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | `75.90% <ø> (ø)` | |
| [udb](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1765/flags?src=pr&el=flag&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv) | `65.84% <ø> (-0.01%)` | :arrow_down: |

Flags with carried forward coverage won't be shown. [Click here](https://docs.codecov.io/docs/carryforward-flags?utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv#carryforward-flags-in-the-pull-request-comment) to find out more.
</details>

[:umbrella: View full report in Codecov by Sentry](https://app.codecov.io/gh/riscv/riscv-unified-db/pull/1765?dropdown=coverage&src=pr&el=continue&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv).   
:loudspeaker: Have feedback on the report? [Share it here](https://about.codecov.io/codecov-pr-comment-feedback/?utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=riscv).
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
- :package: [JS Bundle Analysis](https://docs.codecov.com/docs/javascript-bundle-analysis): Save yourself from yourself by tracking and limiting bundle sizes in JS merges.
</details>

## Review line comments (2)

### @miguelcsx on param_extraction/scripts/generate_report.py:91

```suggestion
    if not rows:
        return

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
```

### @miguelcsx on param_extraction/scripts/generate_report.py:

```suggestion
    with open(names_path, "w", encoding="utf-8") as f:
```

