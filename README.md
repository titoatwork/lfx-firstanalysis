# Architectural parameter extraction (RISC-V)

[![ci](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml/badge.svg)](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml)

Public technical portfolio: measurement, export tooling, evaluation fixtures, and small linked fixes for extracting **architectural parameters** from RISC-V ISA material on [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db).

**Author:** Ibteshamul Haque ([@titoatwork](https://github.com/titoatwork))  
**Context:** [LFX Fall 2026 Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66) · Parameter SIG  
**Spring Part I credit:** [@ishaan-arora-1](https://github.com/ishaan-arora-1) / UDB PRs #1765-#1832 (reproduction and extension only; no claim of Spring authorship)

| | |
|--|--|
| Corpus | 60 param-bearing ISA Manual chunks |
| Gold | 185-parameter pinned freeze; 223-parameter live UDB regeneration |
| Layout | `riscv-param-extraction/` (code + results), `docs/` (summary), `upstream-pr-drafts/` (historical drafts) |

---

## Quick start

```bash
./verify.sh          # re-derive published figures from committed artifacts
./verify.sh --list   # claim table without running checks
```

No API keys, no network model calls. Failures print which artifact disagreed.

More detail: [`docs/`](./docs/README.md) · metrics: [`riscv-param-extraction/docs/metrics.md`](./riscv-param-extraction/docs/metrics.md)

---

## Repository layout

```text
riscv-param-extraction/
  artifact_c/          preregistered dual-run / variance experiment + results
  export/              spreadsheet rows -> draft UDB param YAML
  docs/metrics.md      authoritative measured tables
  analysis/            gold classification and schema-shape audits
  manifests/           run manifests
  workflow_slice/      eval fixtures + review/export path
docs/
  EVIDENCE.md          measurement limits + upstream contribution index
  FAQ.md               definitions and common questions about the numbers
  TERM-PLAN.md         proposed Fall term plan vs official objectives
upstream-pr-drafts/    historical local drafts for filed defects (not the live PR source of truth)
verify.sh              offline verification entrypoint
```

---

## Findings (technical)

### Run-to-run variance

Same model, byte-identical prompt, `temperature=0`, two runs:

| | run 1 | run 2 |
|---|---:|---:|
| adjusted recall | 33.9% | 44.6% |

Prompts match by hash; the scorer is deterministic. Single-run recall is one sample. Filed: [riscv-unified-db#2163](https://github.com/riscv/riscv-unified-db/issues/2163).

### Published recall is grounding, not discovery

Part I prompts inject all **185** gold parameter names (set-identical to the pinned ground truth). Reported 72.9% / 32.2% class of figures measure catalogue grounding under that condition. Discovery without the catalogue is not measured in the published tables.

Discussed on [riscv-unified-db#2053](https://github.com/riscv/riscv-unified-db/issues/2053).

### Exact vs inexact scoring

Most of the weaker model's adjusted score is carried by inexact alignment passes; exact-name rates differ more sharply across models. Decomposition scripts live under `artifact_c/scripts/`.

---

## Upstream (riscv/riscv-unified-db)

Census **2026-08-01**. Live list and discussion links: [`docs/EVIDENCE.md`](./docs/EVIDENCE.md).

| Kind | Count |
|------|------:|
| Merged PRs authored | **7** |
| Open PRs authored | **4** |
| Issues authored | **11** |

**Merged:** [#2138](https://github.com/riscv/riscv-unified-db/pull/2138), [#2146](https://github.com/riscv/riscv-unified-db/pull/2146), [#2189](https://github.com/riscv/riscv-unified-db/pull/2189), [#2215](https://github.com/riscv/riscv-unified-db/pull/2215), [#2227](https://github.com/riscv/riscv-unified-db/pull/2227), [#2256](https://github.com/riscv/riscv-unified-db/pull/2256), [#2266](https://github.com/riscv/riscv-unified-db/pull/2266)

**Open:** [#2289](https://github.com/riscv/riscv-unified-db/pull/2289), [#2255](https://github.com/riscv/riscv-unified-db/pull/2255), [#2212](https://github.com/riscv/riscv-unified-db/pull/2212), [#2164](https://github.com/riscv/riscv-unified-db/pull/2164)

Also: technical comments on other contributors' PRs (e.g. [#2090](https://github.com/riscv/riscv-unified-db/pull/2090), [#2103](https://github.com/riscv/riscv-unified-db/pull/2103), [#2245](https://github.com/riscv/riscv-unified-db/pull/2245)) and design threads ([#2053](https://github.com/riscv/riscv-unified-db/issues/2053), [#2251](https://github.com/riscv/riscv-unified-db/issues/2251), [#2200](https://github.com/riscv/riscv-unified-db/issues/2200)).

---

## Selected measured numbers

All figures below are **single-run** unless noted, and use the **gold name list in the prompt** unless stated otherwise. Prefer [`docs/metrics.md`](./riscv-param-extraction/docs/metrics.md) as the source of truth.

| Item | Value |
|------|------:|
| Part I Claude output vs GT185 | adj **72.9%** · class **88.4%** · WARL **12/24** |
| Same output vs live GT223 | adj **64.2%** |
| Artifact A (gpt-4o-mini) | adj **32.2%** · name Jaccard vs Claude **3.8%** |
| Dual-run noise (arm A) | **33.9%** then **44.6%** |
| Schema-valid export | **83/83** named · **20/20** new drafts (structural only) |

---

## AI assistance

This repository was developed with an AI coding assistant. Prefer the technical artifacts and `./verify.sh` over commit trailers when judging the work. Judgement calls (what to file, what to withdraw, what not to file) are the author's.

---

## License

See [LICENSE](./LICENSE) and package-level licenses under `riscv-param-extraction/`.
