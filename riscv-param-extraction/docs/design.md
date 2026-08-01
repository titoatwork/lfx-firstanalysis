# Design notes

## Relation to Part I

Part I (Spring LFX, PR branches `lfx-1765`…`lfx-1832`, author [@ishaan-arora-1](https://github.com/ishaan-arora-1)) built:

- ground-truth export from UDB param YAML
- taxonomy + v2 extraction prompts
- multi-chunk LLM extract (`extract.py`)
- metrics (`analyze.py`)
- spreadsheet (`parameters.csv`)
- optional `[#param:…]` tagging

**Gaps this package targets (Part II extension):**

| Gap | Artifact | Status |
|-----|----------|--------|
| Multi-model matrix unfinished | **A** | **Done**. Gpt-4o-mini v2 vs Claude; honest worse recall; metrics §5 |
| Spreadsheet → UDB YAML path | **B** | **Done**. 83+20 schema-valid drafts; metrics §7 |
| Reproducible run records | **manifests/** | Pilot + A + v3 |
| WARL quality scar | prompt **v3** ablation | **Done null**. WARL worse; metrics §6 |
| CSR-field grounded WARL | Original **C** | Apparatus under `artifact_c/`; primary four-arm result is noise-limited (see PRIMARY_RESULTS) |

Part I code remains upstream; this monorepo does not re-host the full UDB tree.

## Artifact B decisions

1. **Input** is Part I `parameters.csv`, not raw LLM JSON, matching the spreadsheet review surface.
2. **`named=yes` first** — **87** rows / **83** unique names; **all 83 already exist** under `spec/std/isa/param/`. Export is a schema-valid draft generator + provenance path, not “invent 83 new params.”
3. **New drafts** (`--mode new --limit 20`) target high-confidence `named=no` names **absent** from UDB.
4. **`definedBy`:** copy from existing UDB YAML when `--udb-root` is set; otherwise conservative adoc→extension map.
5. **`schema` field:** map Part I `value_type` without inventing enum members or range bounds. Incomplete domains labeled DRAFT.
6. **Validation:** vendored UDB `param_schema.json` + `schema_defs.json` + draft-07. No silent failures.
7. **additionalProperties: false** → provenance in YAML comments + description NOTE + `$source`.
8. **Non-goal:** unsolicited bulk PR into `riscv/riscv-unified-db`. Coordinate on **sig-parameters** first.

**Schema-valid ≠ architecturally correct.** Structural pass only.

## Artifact A (completed)

Upstream `extract.py` on local UDB (`lfx-1832`), **PROMPT_VERSION=v2**, model **gpt-4o-mini**, 60 param-bearing chunks. Agreement + proposed-new overlap vs committed Claude v2. Mini **underperforms** Claude on adjusted recall. See `docs/metrics.md` §5 and `manifests/artifact-a-gpt-4o-mini.md`.

## Prompt v3 WARL ablation (completed null)

Same model/chunks with structural WARL prompt section only. Overall adj recall ticked up; **matched WARL fell**. Do not present as a successful WARL fix. See metrics §6 and `manifests/stretch-c-v3-warl.md`.

## Artifact C / CSR context

Leakage-audited CSR-field context apparatus lives under `artifact_c/`. Four arms × dual run; primary finding is that within-arm noise exceeds the designed effects (see `artifact_c/results/PRIMARY_RESULTS.md`). Unregistered exploratory finding: most adjusted-recall credit is inexact alignment, which is also where variance concentrates.

## Quality bar

Domain vocabulary (param, WARL, adjusted recall, provenance). Numbers recompute from committed reports via monorepo `./verify.sh`. No invented multi-model metrics.
