Sorry for the churn, I force-pushed to drop a stray trailer from the commit message. The resulting tree is byte-identical to the autofix commit it replaced, so there is nothing new to review. That cleared the auto-merge, could you re-enable it when you get a chance?

Separately, and not caused by this PR: `regress-pre-commit` has failed on every run in the repository since 2026-08-10 09:47 UTC, starting on `main` itself. The last success was 2026-08-10 08:53 UTC. `prek` dies before any hook runs:

```
error: Failed to install hook `prettier`
  caused by: Failed to pack Node hook repository
  caused by: Command `npm pack --global=false ...` exited with an error
```

The passing run used prek 0.4.12 and the first failing run used 0.4.13. `.mise.toml` pins `prek = "0.4.11"`, but `.github/workflows/regress.yml:60` calls `j178/prek-action` without a `prek-version`, so it resolves `latest` and overrides the pin. Passing the mise version through to the action looks like the fix, though I have not verified that 0.4.11 itself is unaffected.
