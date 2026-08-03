# Workflow slice: review and export path

**Purpose:** Convert monorepo measurement depth into maintainer-usable artifacts without bulk PRs or model spam.

| Track | Path | Goal |
|-------|------|------|
| Adversarial eval for skill PR [#2097](https://github.com/riscv/riscv-unified-db/pull/2097) | `eval_2097/` | Frozen fixtures + checks for upstream review |
| 5% vertical slice | `vertical_5pct/` | evidence → review envelope → optional clean UDB YAML |
| Invariant sweep | `scripts/sweep_invariants.py` | Structural defect scan of param YAML + schemas |

## One-command reproduction

```bash
cd riscv-param-extraction
python workflow_slice/scripts/ci_slice_check.py
```

## Invariant sweep

Machine scan of UDB `param/` + `schemas/` for structural defects (pow2 enums, twin bounds, dups, definedBy, required-field census). Does **not** open GitHub issues.

```bash
# Always compare against upstream main, not a local fix branch:
python workflow_slice/scripts/sweep_invariants.py --git-ref origin/main
```

Outputs: `workflow_slice/findings/SWEEP_FINDINGS.md`, `sweep_invariants.json`, `TRIAGE_FOR_CLAUDE.md` (triage notes; filename is historical).

## Rules

- No new paid model runs required for the eval pack (rule-level adversarial fixtures).
- Review metadata **never** mixed into UDB-valid param YAML.
- Zero racing or bulk upstream PRs from this tree.
- Claims: raw fixtures + validator exit codes only.

## Upstream use

- Prefer contributing fixtures/validator when #2097 authors and maintainers engage.
- Small constructive review comments; no pings.
- Historical MTVEC/`0xfff` path resolved via review on [#2090](https://github.com/riscv/riscv-unified-db/pull/2090).
