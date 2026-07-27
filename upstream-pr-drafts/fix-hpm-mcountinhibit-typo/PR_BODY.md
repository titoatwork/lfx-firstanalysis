# Draft PR — fix typo in HPM_COUNTER_EN description

**Target:** `riscv/riscv-unified-db` · branch off `main`  
**Status:** SUPERSEDED for opening, prefer **`fix-hpm-events-dup-index`** (includes this typo + #2046).  
**Author intent:** Ibteshamul Haque · `titoatwork`

## Summary

Fixes a misspelled CSR name in `spec/std/isa/param/HPM_COUNTER_EN.yaml`:

| Was (wrong) | Should be |
|-------------|-----------|
| `mhmpcountinhibit` | `mcountinhibit` |

Also replaces placeholder `long_name: TODO` with a real short title so the
parameter is not left incomplete in the human-facing field.

## Why this matters

- Mentors and implementers reading param YAML should not see a non-existent CSR name.
- Same quality class as small param-data correctness fixes (cf. public PR #1967 style: fix param data, not bulk dumps).
- One file, reviewable in minutes.

## Diff (apply on origin/main)

See `HPM_COUNTER_EN.yaml` in this folder (full file as it should appear after the fix).

Minimal change:

```diff
-  The first three entries *must* be false (as they correspond to CY, IR, TM in, _e.g._ `mhmpcountinhibit`)
+  The first three entries *must* be false (as they correspond to CY, IR, TM in, _e.g._ `mcountinhibit`)
- long_name: TODO
+ long_name: Enabled hardware performance monitors
```

## Test plan

- [ ] Visual review of description against Privileged Spec count-inhibit naming
- [ ] Schema still validates (no schema shape change)
- [ ] No other files touched

## Non-goals

- Not a bulk param extraction dump
- Not changing HPM_COUNTER_EN value schema
- Not related to LFX coding-challenge YAML

## Suggested commit message

```
fix(param): correct mcountinhibit spelling in HPM_COUNTER_EN

The description referenced a non-existent `mhmpcountinhibit` CSR name.
Use `mcountinhibit` and fill long_name instead of TODO.
```
