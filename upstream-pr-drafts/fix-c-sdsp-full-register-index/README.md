# c.sdsp register index — post-filing thread management

The defect, the sweep and the original filing live in
[`../fix-c-sdsp-register-index/`](../fix-c-sdsp-register-index/). This directory
holds only what was posted to the PR after it was opened.

Issue: https://github.com/riscv/riscv-unified-db/issues/2418
PR:    https://github.com/riscv/riscv-unified-db/pull/2419

## Branch state

Three commits on `fix/c-sdsp-full-register-index`, branched from `7ad0966e`.

| Commit | Change |
|---|---|
| `d4d229ce` | the fix: `c.sdsp` uses its full 5-bit register index |
| `85bda00d` | `rs2` -> `xs2` in the description |
| `4eac34bc` | `autofix-ci[bot]` golden-file regeneration, cherry-picked |

`85bda00d` replaced `bbcc681b`, which had been pushed with a
`Co-Authored-By: Claude Opus 5` trailer. That was amended out and force-pushed
within minutes. The force-push was rejected first because `autofix-ci[bot]` had
pushed `4baad916` in the meantime; resolved by fetching, cherry-picking the bot
commit onto the amended commit, verifying the trees were identical (`f79e121a`),
then `--force-with-lease`.

## Posted here

| File | Where | Status |
|---|---|---|
| `REPLY-2419-automerge.md` | `issuecomment-5246156110`, 2026-08-10 21:18 UTC | **contains a wrong claim, see below** |
| `REPLY-2419-ci-fixed.md` | `issuecomment-5248514545`, 2026-08-11 03:03 UTC | the correction |

Both files are kept verbatim as the record of what was actually posted. The
first is not edited to hide the error.

## The wrong claim, and what was actually true

`REPLY-2419-automerge.md` reported the repo-wide `regress-pre-commit` failure and
named a root cause: `j178/prek-action` is called without `prek-version`, so it
resolves `latest` and overrides the `prek = "0.4.11"` pin in `.mise.toml`. It
suggested passing the mise version through to the action.

**That remedy was wrong.** The failure was a node version. The `prettier` hook
declares `devEngines` requiring node 24.18.0 and the runner had 22.23.1:

```
npm error EBADDEVENGINES Invalid semver version "24.18.0" does not match "v22.23.1" for "runtime"
```

Fixed upstream by #2455 (jordancarlin), merged 2026-08-11 01:53 UTC, one line in
`.mise.toml`: `idiomatic_version_file_enable_tools = ["node"]`.

**What settles it:** the passing run still uses **prek 0.4.13**, the same version
as every failing run. Only node changed. That single query would have disproved
the diagnosis before it was posted, and was not run.

| Claim in the original note | Verdict |
|---|---|
| Last green `regress-pre-commit` 2026-08-10 08:53 UTC | correct (job-level, `gh-readonly-queue/main/pr-2450`) |
| First red 2026-08-10 09:47 UTC, on `main` | correct (job-level; the run-level conclusion reads `cancelled` and misleads) |
| Error text quoted from the log | correct, verbatim |
| Last green ran prek 0.4.12, first red ran 0.4.13 | correct, and irrelevant |
| `.mise.toml` pins `prek = "0.4.11"` | correct |
| The action runs its own prek ahead of that pin | correct |
| **Passing the mise version through is the fix** | **wrong** |

The lesson recorded in the handoff: a correlation in a version number is not a
cause, and a root cause is not publishable until the remedy has been tested.

## Still outstanding

Auto-merge is off, revoked by the force-push. Re-enable was asked for at
2026-08-10 21:18 UTC and again at 2026-08-11 03:03 UTC. The PR is approved three
times over; its red CI is stale, from a run that predates the fix, and needs a
re-run rather than a rebase.
