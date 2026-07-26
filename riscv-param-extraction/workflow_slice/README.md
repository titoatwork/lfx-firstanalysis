# Workflow slice — review/export (≈5% vertical path)

**Purpose:** Convert monorepo depth into **maintainer-usable** artifacts without bulk PRs or model spam.

| Track | Path | Goal |
|-------|------|------|
| Adversarial eval for skill PR #2097 | `eval_2097/` | Frozen fixtures + checks; feed upstream review |
| 5% vertical slice | `vertical_5pct/` | evidence → review envelope → optional clean UDB YAML |

## One-command reproduction

```bash
cd riscv-param-extraction
python workflow_slice/scripts/ci_slice_check.py
```

## Hard rules

- No new paid model runs required for the eval pack (rule-level adversarial fixtures).
- Review metadata **never** mixed into UDB-valid param YAML.
- Zero racing/bulk upstream PRs from this tree.
- Claims: raw fixtures + validator exit codes only.

## Upstream use

- Prefer contributing fixtures/validator **if** #2097 author/maintainers engage.
- One constructive review comment on #2097; no pings.
- MTVEC/`0xfff` stays on #2090 wait path (not this package).
