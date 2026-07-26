# Measured claim ledger — Part II application

**Purpose:** Every public or application claim must map to a source.  
**Date:** 2026-07-26  
**Primary sources:** `riscv-param-extraction/docs/metrics.md`, manifests, monorepo results JSON  
**Credit:** Spring Part I pipeline and committed Claude results — [@ishaan-arora-1](https://github.com/ishaan-arora-1) / PRs #1765–#1832. This campaign **reproduces and extends**; it does not claim Spring authorship.

---

## Safe claims (approved wording)

| Claim | Exact numbers | Source | Allowed use |
|-------|---------------|--------|-------------|
| Live UDB GT size | **223** params; 100% any / **91%** strong keyword match | metrics §1 | Application, README |
| Part I v2 vs pinned GT185 | adj recall **72.9%**, class acc **88.4%**, WARL **50%** (12/24) | metrics §2; remeasure | Lead numbers |
| Same LLM output vs live GT223 | adj recall **64.2%**, class acc **88.6%**, WARL still **50%** | metrics §2 | Gold drift story |
| named=yes rows | **87** rows / **83** unique names | metrics §4 | Never say 97 |
| Artifact B named export | **83/83** schema-valid; all 83 already in UDB | metrics §7 (was §6) | Structural validity only |
| Artifact B new export | **20/20** schema-valid drafts; not in UDB | metrics §7 | Candidates, not merges |
| Pilot | **COMPLETE_WITH_MODEL_SPLIT** ~**$0.05**; 021 gpt-4o, 020 gpt-4o-mini | metrics §3; pilot manifest | TPM honesty |
| Artifact A model | **gpt-4o-mini**, PROMPT **v2**, **60/60** chunks | metrics §5; A manifest | Not pure gpt-4o |
| Artifact A vs GT185 | adj **32.2%**, WARL **12.5%** (3/24), ~**$0.16** | metrics §5 | Honest worse-than-Claude |
| Claude Part I baseline (not re-billed) | adj **72.9%**, 346 deduped names | metrics §5 | Comparison baseline |
| Name agreement A | shared **21**, Jaccard **3.8%** | metrics §5.3 | Review-gating story |
| High-conf proposed-new both models | **9** names | metrics §5.4 | Candidates needing review |
| v3 prompt WARL ablation | **60/60**; adj **35.0%**; WARL **8.3%** (2/24); ~**$0.16** | metrics §6; stretch-c manifest | **Null / negative** for WARL |
| Public repo | https://github.com/titoatwork/lfx-firstanalysis | git | Prework link |
| Coding challenge pack | 2 snippets · fail-closed CI · curated + live multi-model under `challenge/` | monorepo | Path A |
| Live multi-model (snippets) | Multiple providers; **best free legs** hit CMO=3 + CSR=0 (e.g. Nemotron Ultra free, Gemini free, Ling free); some models under-extract or CSR false-positive — report honestly | `challenge/results/live/MANIFEST.md` | Not corpus-scale; not Sonnet claim |
| Open Spring PRs (context) | #1765–#1832 still the Part I surface | GitHub | “merge/export still open” |
| UDB PRs (when open) | Prefer issue-linked data fixes (#2102 STVAL_WIDTH, #2046 HPM_EVENTS) | GitHub PR URLs | Only after open; never invent merges |

### The nine dual-model high-conf “new” candidates (not confirmed params)

`FLEN`, `IALIGN`, `ILEN`, `MISELECT_ACCESS`, `NUM_PRIVILEGE_MODES`, `PAUSE_DURATION`, `RNMI_EXCEPTION_TRAP_HANDLER_ADDRESS`, `SEED_CSR_ACCESS_CONTROL`, `SISELECT_MIN_RANGE`

---

## Forbidden or unsafe claims

| Do **not** say | Why |
|----------------|-----|
| “I built / authored Spring Part I” | Authorship is @ishaan-arora-1 / Spring PRs |
| “97 named parameters” | Measured **87/83** |
| “Pure gpt-4o full pilot / full multi-model matrix” | Pilot model-split; A is mini |
| “Mini matched or beat Claude” | 32.2% vs 72.9% |
| “v3 improved WARL” | WARL fell 3/24 → 2/24 |
| “9 overlapping names are real parameters” | Candidates only |
| “Schema-valid means architecturally correct” | Structural check only |
| “Artifact C (CSR-field context) is done” | **Not run**; only prompt-v3 ablation done |
| Fake merge counts or SIG attendance | Not true |
| “Curated challenge results are live LLM scores” | Curated = CI gold; live = `results/live/` |
| “We beat Anshul / guaranteed selection” | Strategy talk, not evidence |
| Applicant counts / admission probability | Unknown; do not invent |

---

## Four red-team checks (apply to every sentence)

1. **Attribution** — reproduction vs original authorship  
2. **Measurement** — number in metrics/manifest?  
3. **Scope** — model, corpus, denominator, prompt version stated?  
4. **Interpretation** — claim only what the measurement shows?

---

## One-sentence narrative (memorize)

> I reproduced the Spring pipeline, measured where it fails across models and a WARL prompt ablation, built a schema-valid UDB export path, and have a concrete plan to turn generated findings into small human-reviewed upstream contributions.
