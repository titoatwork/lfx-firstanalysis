# Design notes

## Relation to Part I

Part I (Spring LFX, PR branches `lfx-1765`…`lfx-1832`) built:

- ground-truth export from UDB param YAML  
- taxonomy + v2 extraction prompts  
- multi-chunk LLM extract (`extract.py`)  
- metrics (`analyze.py`)  
- spreadsheet (`parameters.csv`)  
- optional `[#param:…]` tagging  

**Gaps this repo targets (Part II / pre-apply):**

| Gap | Artifact |
|-----|----------|
| Multi-model matrix unfinished | **A** (blocked on API in this workspace) |
| Spreadsheet → UDB YAML path | **B** (`export/`) |
| Reproducible run records | **manifests/** (Obj 3) |

Part I code remains upstream; this repo does not re-host the full UDB tree.

## Artifact B decisions

1. **Input** is Part I `parameters.csv`, not raw LLM JSON — same surface mentors already review in the spreadsheet phase.  
2. **`named=yes` first** — on the measured freeze that is **87 rows / 83 unique names**, and **all 83 already exist** under `spec/std/isa/param/`. Export is still useful as a *schema-valid draft generator + provenance packing* path, not as “invent 83 new params.”  
3. **New drafts** (`--mode new --limit 20`) target high-confidence `named=no` names **absent** from UDB.  
4. **`definedBy`:** copy from existing UDB YAML when `--udb-root` is set; otherwise conservative adoc→extension map (`export/adoc_extension.py`) with source tags in the file header.  
5. **`schema` field:** map Part I `value_type` without inventing enum members or range bounds (`export/value_type_map.py`). Incomplete domains are labeled DRAFT in the schema description.  
6. **Validation:** vendored UDB `param_schema.json` + `schema_defs.json` + draft-07 under `export/schemas/`. No silent failures — report JSON lists every error.  
7. **additionalProperties: false** on param schema → provenance lives in YAML comments + description NOTE + `$source`, not ad-hoc keys.  
8. **Non-goal:** unsolicited bulk PR into `riscv/riscv-unified-db`. Ask on **sig-parameters** first.

## Artifact A (when API exists)

Use upstream `extract.py` on the local UDB clone (`lfx-1832`), v2 prompts, second model alias (`gpt4o` or `gemini`). Deliver honest tables even if worse than Claude. Manifest every run.

## Quality bar

Domain vocabulary (param, WARL, adjusted recall, provenance). No generic chatbot README. Mentors should recompute tables from committed reports.
