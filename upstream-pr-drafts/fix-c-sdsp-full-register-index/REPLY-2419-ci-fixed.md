This is fixed. #2455 landed at 2026-08-11 01:53 UTC, and `regress-pre-commit` passed at 02:46 UTC on #2395, whose head I pushed at 02:41 UTC. `regress.yml` runs on `pull_request` and `actions/checkout` takes `refs/pull/N/merge`, so the corrected `.mise.toml` arrives from `main` without a rebase. A re-run should be enough here.

Correcting my note above: the remedy I suggested was wrong. The failure is a node version, not the prek version.

```
npm error EBADDEVENGINES Invalid semver version "24.18.0" does not match "v22.23.1" for "runtime"
npm error EBADDEVENGINES   current:  { name: 'node', version: 'v22.23.1' }
npm error EBADDEVENGINES   required: { name: 'node', version: '24.18.0', onFail: 'download' }
```

The `prettier` hook declares `devEngines` requiring node 24.18.0 and the runner had 22.23.1. What settles it is that the passing run still uses **prek 0.4.13**, the same version as every failing run; what changed is that mise now installs node 24.18.0. So pinning `prek-version` through to the action would not have helped. The 0.4.12 to 0.4.13 timing was a real signal, but prek was the trigger rather than the thing to change.

The rest of that note holds: the last green `regress-pre-commit` was 2026-08-10 08:53 UTC and the first red was 09:47 UTC on `main`, and the action does run its own prek ahead of the `0.4.11` pin in `.mise.toml`. Neither was the cause.

The failing runs here are from 2026-08-10 20:52 UTC, before the fix. Could you re-run them and re-enable auto-merge when you get a chance?
