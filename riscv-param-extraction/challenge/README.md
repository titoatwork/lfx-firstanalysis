# RISC-V Architectural Parameter Extraction — Coding Challenge

**Monorepo home:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · package `riscv-param-extraction/`  
**Author:** Ibteshamul Haque · GitHub `titoatwork`  
**Project:** LFX Fall 2026 — AI-assisted extraction of architectural parameters from RISC-V specifications (Parameter SIG / [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db))

This pack is the **shared coding-challenge surface** (two ISA snippets, optionality language, anti-hallucination, schema-shaped YAML). It lives **inside** the monorepo next to full-corpus science — not as a second product repo.

**Spring credit:** Part I pipeline and committed results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765–#1832. This work reproduces and extends; it does not claim Spring authorship.

---

## Task (shared bar)

Write prompts that extract architectural parameters from ISA Manual excerpts, where a parameter is signaled by optionality language (`may`/`might`/`should`, `optional`/`optionally`, `implementation-defined`/`implementation-specific`), deal explicitly with hallucination, and produce schema-shaped YAML.

| Snippet | Source | Expected shape |
|---------|--------|----------------|
| `snippets/cmo_cache_block.txt` | Priv **19.3.1** CMO | Parameters present |
| `snippets/csr_address_mapping.txt` | Priv **2.1** CSR mapping | **Zero** parameters (negative control) |

---

## Path A — Challenge (this directory)

| Item | Location |
|------|----------|
| Prompts v1→v2→v3 | `prompts/` |
| Curated grounded results | `results/curated/` (3 CMO params + CSR zero file) |
| Fail-closed validator | `scripts/validate.py` |
| Bad fixtures (must fail) | `tests/bad_examples/` (**4** cases) |
| Hard negatives (**4**) | `negative_controls/` |
| Markup robustness | `robustness/` (naive vs tag-aware) |
| Multi-strategy matrix | `scripts/score_strategies.py` (offline controls) |
| Known-param bench **n=15** | `benchmark/` (pretraining caveat first) |
| Modeling notes | `docs/modeling-notes.md` |
| Scale/cost | `docs/scale_and_cost.md` |
| Live multi-model how-to | `docs/LIVE_MULTI_MODEL.md` |
| **Live multi-model results** | `results/live/` — OpenAI + Gemini free + Groq Llama 70B free (see `MANIFEST.md`) |
| Optional live extract | `scripts/extract.py` (no API unless `--live` + key) |

### How to run (local / CI)

```bash
cd riscv-param-extraction
pip install -r requirements.txt

# Good results must pass
python challenge/scripts/validate.py --results challenge/results/curated

# Bad fixtures must fail (exit 0 only with --expect-fail when errors exist)
python challenge/scripts/validate.py --results challenge/tests/bad_examples --expect-fail

python challenge/scripts/check_negatives.py
python challenge/scripts/check_grounding_modes.py
python challenge/scripts/score_strategies.py
python challenge/benchmark/scripts/score_recall.py

# One-shot gate (also runs export unit tests)
python challenge/scripts/ci_check.py
```

### Curated CMO results (reference)

| Name | Type | Notes |
|------|------|--------|
| `CACHE_BLOCK_SIZE` | integer | Exists upstream in UDB; max omitted (no upper bound in snippet) |
| `CACHE_CAPACITY` | integer | Independent axis; review gating |
| `CACHE_ORGANIZATION` | string | Opaque; SIG scoping candidate |

CSR snippet: see `results/curated/csr_address_mapping.NO_PARAMETERS_FOUND.txt`.

### Live multi-model (2026-07-26)

**OpenAI + Google free + Groq free (open-weight).** Not Sonnet/Opus/GLM. Details: [`results/live/MANIFEST.md`](./results/live/MANIFEST.md).

| Model | CMO | CSR negative control |
|-------|-----|----------------------|
| `gemini-3.6-flash` (free) | **3** | **PASS** zero |
| `llama-3.3-70b-versatile` (Groq free) | **3** | **FAIL** 5 false positives |
| `gpt-4o-mini-2024-07-18` | 1 | **FAIL** 1 false positive |
| `gpt-4o-2024-11-20` | 1 | **PASS** zero |
| curated (CI gold, not live) | 3 | PASS |

```bash
python challenge/scripts/validate.py --results challenge/results/live/gemini-3.6-flash
python challenge/scripts/validate.py --results challenge/results/live/llama-3.3-70b-versatile
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-2024-11-20
python challenge/scripts/validate.py --results challenge/results/live/gpt-4o-mini-2024-07-18
```

### Fail-closed fixtures

| Fixture | Why it must fail |
|---------|------------------|
| `HALLUCINATED_QUOTE` | Quote not in source |
| `SCHEMA_INVALID` | Missing description + bad name |
| `CSR_FALSE_POSITIVE` | Fake quote / false CSR param |
| `WRONG_NAME_PATTERN` | Not `UPPER_SNAKE_CASE` |

### Hard negatives

Four cases where optionality-ish language appears but **parameters must be []**:
spurious MTIP software advice, branch-prediction compiler advice, shall-only constraint, by-convention encoding.

### Markup robustness

Raw AsciiDoc cases where **naive** quote match can fail and **tag-aware** strip recovers — same failure class as Spring markup issues (e.g. PR #1832 discussion).

---

## Path B — Full-corpus science (monorepo; challenge kits usually lack this)

Authoritative numbers: [`../docs/metrics.md`](../docs/metrics.md)

| Track | Scope | Headline | Caveat |
|-------|--------|----------|--------|
| GT remeasure | Live **223** / pinned **185** | 100%/91% keyword; Claude adj **72.9%** (GT185), **64.2%** (GT223); WARL **50%** | Credit Spring Part I results |
| Multi-model corpus | **60** chunks | mini adj **32.2%** vs Claude **72.9%**; name Jaccard **3.8%** | Not a 2-snippet demo |
| Dual-new review queue | high-conf both models | **9** candidates | Not confirmed params |
| Export | named + new | **83/83** + **20/20** schema-valid | Structural only — not merge approval |
| WARL prompt ablation | v3 mini | WARL **8.3%** (worse than v2) | **Honest null** — do not claim success |
| Challenge snippets | 2 | CSR=0; 3 CMO candidates | Demo scale only |

**Do not** claim challenge n=2 or known-param re-derive scores beat Spring corpus recall on equal footing.

---

## FAQ

**Is the coding challenge an official LFX file attachment?**  
Treat the shared 2-snippet task as the field standard for this project. Confirm wording on the LFX project/apply page when logged in.

**Why is this not a separate GitHub repo?**  
Single public campaign home: `lfx-firstanalysis`. Challenge + corpus + export stay together.

**Are curated results the same as multi-model API runs?**  
No. Curated results are schema-valid, quote-grounded references for CI. Live multi-model runs (2026-07-26 OpenAI mini + gpt-4o) live under `results/live/` with `MANIFEST.md` — see honest under-extract / mini CSR false-positive.

---

## Layout

```
challenge/
  snippets/     two challenge excerpts (+ raw markup)
  prompts/      v1 naive → v2 anchored → v3 schema
  schema/       vendored UDB param schema
  scripts/      validate, negatives, grounding, ci_check, extract
  results/      curated (+ optional live)
  tests/        bad_examples (fail closed)
  negative_controls/
  robustness/
  docs/
  manifests/
```
