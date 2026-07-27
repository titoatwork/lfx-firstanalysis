# Design notes

## Relation to Part I

Part I (Spring LFX, PR branches `lfx-1765`…`lfx-1832`, mentee @ishaan-arora-1) built:

- ground-truth export from UDB param YAML  
- taxonomy + v2 extraction prompts  
- multi-chunk LLM extract (`extract.py`)  
- metrics (`analyze.py`)  
- spreadsheet (`parameters.csv`)  
- optional `[#param:…]` tagging  

**Gaps this package targets (Part II / pre-apply):**

| Gap | Artifact | Status |
|-----|----------|--------|
| Multi-model matrix unfinished | **A** | **Done**. Gpt-4o-mini v2 vs Claude; honest worse recall; metrics §5 |
| Spreadsheet → UDB YAML path | **B** | **Done**. 83+20 schema-valid drafts; metrics §7 |
| Reproducible run records | **manifests/** | Pilot + A + v3 |
| WARL quality scar | prompt **v3** ablation | **Done null**. WARL worse; metrics §6 |
| CSR-field grounded WARL | Original **C** | **Not run**. Deferred post-apply with leakage audit |

Part I code remains upstream; this repo does not re-host the full UDB tree.

## Artifact B decisions

1. **Input** is Part I `parameters.csv`, not raw LLM JSON, same surface mentors already review in the spreadsheet phase.  
2. **`named=yes` first** — **87** rows / **83** unique names; **all 83 already exist** under `spec/std/isa/param/`. Export is a *schema-valid draft generator + provenance packing* path, not “invent 83 new params.”  
3. **New drafts** (`--mode new --limit 20`) target high-confidence `named=no` names **absent** from UDB.  
4. **`definedBy`:** copy from existing UDB YAML when `--udb-root` is set; otherwise conservative adoc→extension map.  
5. **`schema` field:** map Part I `value_type` without inventing enum members or range bounds. Incomplete domains labeled DRAFT.  
6. **Validation:** vendored UDB `param_schema.json` + `schema_defs.json` + draft-07. No silent failures.  
7. **additionalProperties: false** → provenance in YAML comments + description NOTE + `$source`.  
8. **Non-goal:** unsolicited bulk PR into `riscv/riscv-unified-db`. Ask on **sig-parameters** first.

**Schema-valid ≠ architecturally correct.** Structural pass only.

## Artifact A (completed)

Upstream `extract.py` on local UDB (`lfx-1832`), **PROMPT_VERSION=v2**, model **gpt-4o-mini**, 60 param-bearing chunks. Agreement + hallucination-overlap vs committed Claude v2. Honest tables: mini **underperforms** Claude on adjusted recall. See `docs/metrics.md` §5 and `manifests/artifact-a-gpt-4o-mini.md`.

## Prompt v3 WARL ablation (completed null)

Same model/chunks with structural WARL prompt section only. Overall adj recall ticked up; **matched WARL fell**. Do not present as successful Stretch C. See metrics §6 and `manifests/stretch-c-v3-warl.md`.

## Original Artifact C (deferred)

CSR-field / UDB auxiliary context with **leakage audit** before any API. Not required for apply; describe as future work in the application.

## Quality bar

Domain vocabulary (param, WARL, adjusted recall, provenance). No generic chatbot README. Mentors should recompute tables from committed reports.
