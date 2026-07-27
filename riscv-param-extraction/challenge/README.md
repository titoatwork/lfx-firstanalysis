# RISC-V Architectural Parameter Extraction — Coding Challenge

[![ci](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml/badge.svg)](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml)

**Monorepo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · package `riscv-param-extraction/`  
**Author:** Ibteshamul Haque · `titoatwork`  
**Project:** LFX Fall 2026. AI-assisted extraction of architectural parameters (Parameter SIG / [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db))

This directory is the **shared coding-challenge surface** (two ISA snippets, optionality language, anti-hallucination, schema-shaped YAML). It lives **inside** the monorepo next to full-corpus science, one public home, not a second product repo.

**Spring credit:** Part I pipeline and committed results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765–#1832. This work **reproduces and extends**; it does **not** claim Spring authorship.

---

## 60-second mentor view

| Control | Count / result | Where |
|---------|----------------|--------|
| Challenge snippets | 2 (CMO + CSR zero) | `snippets/` |
| Prompt iteration | v1 → v2 → v3 | `prompts/` |
| Fail-closed bad fixtures | **4** (must fail) | `tests/bad_examples/` |
| Hard negatives | **4** (must extract zero) | `negative_controls/` |
| Markup robustness | 3 cases · naive vs tag-aware | `robustness/` |
| Known-param bench | **n=15** · caveat-first | `benchmark/` |
| Live multi-model (snippets) | **10** models · honest CSR fails | `results/live/MANIFEST.md` |
| Offline multi-strategy matrix | keyword vs closed-world | `scripts/score_strategies.py` |
| Temporal holdout harness | locked exploratory null (v1.2) | [`temporal_holdout/`](./temporal_holdout/) · [PR #1](https://github.com/titoatwork/lfx-firstanalysis/pull/1) |
| One-command CI gate | green | `python challenge/scripts/ci_check.py` |

**Same shared exam as other public challenge kits; denser offline controls; broader live matrix; plus Path B corpus science in-repo.**

---

## Task (shared bar)

Write prompts that extract architectural parameters from ISA Manual excerpts, where a parameter is signaled by optionality language (`may`/`might`/`should`, `optional`/`optionally`, `implementation-defined`/`implementation-specific`), deal explicitly with hallucination, and produce schema-shaped YAML.

| Snippet | Source | Expected shape |
|---------|--------|----------------|
| `snippets/cmo_cache_block.txt` | Priv **19.3.1** CMO | Parameters present |
| `snippets/csr_address_mapping.txt` | Priv **2.1** CSR mapping | **Zero** parameters (negative control) |

---

## 1. Prompt design and anti-hallucination

Three versions in `prompts/`, each fixing a concrete failure class:

| Version | Intent |
|---------|--------|
| **v1 naive** | Direct extract, over-triggers on “sounds technical” |
| **v2 keyword-anchored** | Optionality phrases + **verbatim quote** required |
| **v3 schema-constrained** | UDB `param_schema` shape, empty list allowed, few-shot discipline |

**Mechanical grounding:** `scripts/validate.py` checks every result YAML has a sibling evidence quote present in the cited snippet (whitespace-normalized; optional tag-aware mode).

**Fail-closed fixtures** (`tests/bad_examples/` — **4**):

| Fixture | Why it must fail |
|---------|------------------|
| `HALLUCINATED_QUOTE` | Quote not in source |
| `SCHEMA_INVALID` | Missing description + bad name |
| `CSR_FALSE_POSITIVE` | Fake quote / false CSR param |
| `WRONG_NAME_PATTERN` | Not `UPPER_SNAKE_CASE` |

---

## 2. Results on the two challenge snippets

### CMO cache blocks (Priv 19.3.1)

Curated CI gold (`results/curated/`):

| Name | Type | Notes |
|------|------|--------|
| `CACHE_BLOCK_SIZE` | integer | Exists upstream; max omitted (no upper bound in snippet) |
| `CACHE_CAPACITY` | integer | Independent axis; review gating |
| `CACHE_ORGANIZATION` | string | Opaque; SIG scoping candidate |

Capacity / organization / block size are modeled as **independent** parameters when the text treats them as independent (same modeling discipline as maintainer feedback that split over-broad parameters, e.g. discussion around PMLEN-style bundling in UDB review culture).

### CSR address mapping (Priv 2.1)

**Zero** parameters, fixed encoding convention, not optionality.  
See `results/curated/csr_address_mapping.NO_PARAMETERS_FOUND.txt`.

---

## 3. Live multi-model (same two snippets)

**10 live models** (2026-07-26): OpenAI ×2 + free Google/Groq/OpenRouter mix. **Not** Sonnet/Opus/GLM. Full matrix and caveats: [`results/live/MANIFEST.md`](./results/live/MANIFEST.md).

| Pattern | Models |
|---------|--------|
| Full CMO (3) + clean CSR | e.g. Nemotron Ultra free, Ling free, Gemini free |
| Under-extract CMO | gpt-4o, gpt-4o-mini, several free mid models |
| CSR false positives | Llama 70B free, mini, Laguna, Gemma free |

**Design implication:** model choice is largely a **recall** decision; disagreement and over-triggering argue for **human/SIG review gates**, not single-model trust. Curated `results/curated/` remains CI gold, live dirs are comparative evidence only.

---

## 4. Known-parameter benchmark (n=15)

`benchmark/` re-pairs **15** already-merged UDB parameters with source prose and checks existence + type fidelity.

```bash
python challenge/benchmark/scripts/score_recall.py
```

**Read carefully, not a blind benchmark.** Cases are public UDB params a frontier model may have seen. This scores **pipeline mechanics** (does extract recognize a parameter is warranted; does type match), not generalization equal to Spring corpus adjusted recall (72.9% / 36.8%-class numbers). Pretraining leakage is stated first in the scorer output.

---

## 5. Hard negatives and markup robustness

**Hard negatives (4):** optionality-ish words (`should`/`may`) that are **software advice** or **non-configurable** normative text, must extract **zero** parameters.

**Markup robustness (3):** raw AsciiDoc where **naive** quote match fails and **tag-aware** strip recovers, same failure class discussed around Spring markup handling (e.g. PR #1832 discussion).

---

## 6. Temporal holdout harness (method extension)

Beyond the shared 2-snippet challenge: a **preregistered** vertical pilot with leakage-audited CSR context, frozen model pin, immutable run directory, and published scores.

| Item | Value |
|------|--------|
| Primary run | `20260726T164713Z_gpt-4o-mini-2024-07-18` · **26/26** |
| Name / WARL recall | **0/10** and **0/5** both arms |
| Claim level | **Exploratory null / harness demo**. V1.2 had guidance limitations (see write-up) |

Details: [`temporal_holdout/results/PRIMARY_RESULTS.md`](./temporal_holdout/results/PRIMARY_RESULTS.md) · PR: [titoatwork/lfx-firstanalysis#1](https://github.com/titoatwork/lfx-firstanalysis/pull/1).

**Do not** claim this as clean temporal-holdout proof of CSR-context success.

---

## 7. Scale and cost

Snippet work is demo-scale. Manual-scale estimates and measured corpus costs live in:

- Challenge scale notes: [`docs/scale_and_cost.md`](./docs/scale_and_cost.md)  
- **Measured** 60-chunk Artifact A / pilot / WARL ablation: [`../docs/metrics.md`](../docs/metrics.md)

---

## How to run (local = CI)

```bash
cd riscv-param-extraction
pip install -r requirements.txt
python challenge/scripts/ci_check.py

# Offline strategies + live multi-model disagreement table
python challenge/scripts/score.py
```

That gate runs: curated validate · bad fixtures expect-fail · hard negatives · markup modes · strategy matrix · n=15 score · live matrix re-score · score.py · temporal holdout tests + leak_scan · export unit tests.

Optional live extract (requires key; no API by default):

```bash
python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt
python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt --live --model gpt-4o-mini-2024-07-18
```

---

## Path B — Full-corpus science (challenge-only kits usually lack this)

Authoritative numbers: [`../docs/metrics.md`](../docs/metrics.md)

| Track | Headline | Caveat |
|-------|----------|--------|
| GT remeasure | Claude adj **72.9%** (GT185), **64.2%** (GT223); WARL **50%** | Credit Spring Part I |
| Multi-model corpus | mini **32.2%** vs Claude **72.9%**; Jaccard **3.8%** | 60 chunks, not 2 snippets |
| Export B | **83/83** + **20/20** schema-valid | Structural only |
| WARL prompt ablation | WARL **worse** (3/24→2/24) | Honest null |

**Do not** claim challenge n=2 or known-param re-derive scores beat Spring corpus recall on equal footing.

---

## Layout

```
challenge/
  snippets/            two challenge excerpts (+ raw markup)
  prompts/             v1 → v2 → v3
  schema/              vendored UDB param schema
  scripts/             validate, ci_check, extract, strategies
  results/curated/     CI gold
  results/live/        multi-model matrix
  tests/bad_examples/  fail-closed (4)
  negative_controls/   hard negatives (4)
  robustness/          tag-aware grounding
  benchmark/           n=15 known-param (caveat-first)
  temporal_holdout/    preregistered CSR-context pilot
  docs/
```

---

## Honesty checklist

- Curated ≠ live API scores  
- Known-param bench ≠ blind corpus recall  
- Live matrix has real CSR failures, reported  
- Holdout v1.2 = exploratory null with documented prompt limitations  
- Spring authorship = @ishaan-arora-1 / #1765–#1832  
