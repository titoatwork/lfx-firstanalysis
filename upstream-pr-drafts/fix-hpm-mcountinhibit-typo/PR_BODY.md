# PR body (not filed) — HPM_COUNTER_EN mcountinhibit spelling

**Outcome:** not filed as a standalone PR. Subsumed by the HPM_EVENTS candidate / upstream ownership of #2046.

Draft below is historical.

---

## Summary

Fixes a misspelled CSR name in `spec/std/isa/param/HPM_COUNTER_EN.yaml`:

| Was (wrong) | Should be |
|-------------|-----------|
| `mhmpcountinhibit` | `mcountinhibit` |

Also replaces placeholder `long_name: TODO` with a real short title.

## Why it mattered

- Param YAML should not name a non-existent CSR.
- One file, reviewable in minutes — but not worth a race against owned HPM work.

## Minimal change

```diff
-  The first three entries *must* be false (as they correspond to CY, IR, TM in, _e.g._ `mhmpcountinhibit`)
+  The first three entries *must* be false (as they correspond to CY, IR, TM in, _e.g._ `mcountinhibit`)
- long_name: TODO
+ long_name: Enabled hardware performance monitors
```

## Non-goals

- Not a bulk param extraction dump
- Not changing HPM_COUNTER_EN value schema
