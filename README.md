# LFX Mentorship — lfx-firstanalysis

[![ci](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml/badge.svg)](https://github.com/titoatwork/lfx-firstanalysis/actions/workflows/ci.yml)

**Owner:** Ibteshamul Haque · GitHub: [titoatwork](https://github.com/titoatwork)  
**Project:** [AI-assisted architectural parameter extraction – Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66)  
**Mentors:** Allen Baum, Ajit Dingankar · **Upstream:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)

Public prework for LFX Fall 2026 Part II: **coding-challenge pack**, **measured corpus science**, **schema-valid export drafts**, **live multi-model results**, and a **temporal holdout harness** (exploratory null, self-audited).

Spring Part I (extract → analyze → spreadsheet) was built on open UDB PR branches **#1765–#1832** by [@ishaan-arora-1](https://github.com/ishaan-arora-1). This repo **reproduces**, **remeasures**, and **extends**. It does **not** claim Part I authorship.

---

## 5-minute mentor path

| # | Open | Proves |
|---|------|--------|
| 1 | **[Challenge pack](./riscv-param-extraction/challenge/)** | Same 2-snippet exam + **denser controls** (4 bad fixtures, 4 hard negatives, n=15, 10 live models) + green CI |
| 2 | **[Measured tables](./riscv-param-extraction/docs/metrics.md)** | GT remeasure, Artifact A multi-model, B export, WARL prompt **null** |
| 3 | **[Live multi-model matrix](./riscv-param-extraction/challenge/results/live/MANIFEST.md)** | Honest CMO/CSR per model (failures included) |
| 4 | **[Temporal holdout](./riscv-param-extraction/challenge/temporal_holdout/)** · [PR #1](https://github.com/titoatwork/lfx-firstanalysis/pull/1) | Preregistered CSR-context pilot; locked **exploratory null** (v1.2 limitations documented) |
| 5 | **[Export + drafts](./riscv-param-extraction/)** | `export/`, `drafts/param/`, `drafts/param-new/` |
| 6 | **[Application packet](./application-packet/)** | Essay, 9-week plan, **claim ledger** |
| 7 | **Upstream work** (below) | Issue-linked fix + adopted review + adversarial eval, not bulk PRs |

### Upstream (riscv/riscv-unified-db)

| Item | State |
|------|-------|
| [PR #2138](https://github.com/riscv/riscv-unified-db/pull/2138) + [issue #2137](https://github.com/riscv/riscv-unified-db/issues/2137) | **Open.** `4095` is not a power of two but appears in both `unsigned_pow2` schema enums; fixed with a regression test wired into the Ruby test runner |
| [PR #2146](https://github.com/riscv/riscv-unified-db/pull/2146) + [issue #2145](https://github.com/riscv/riscv-unified-db/issues/2145) | **Open.** `UXLEN`'s description named `SXLEN` as the parameter `mstatus.UXL` changes; `SXLEN`'s option list used scalars against its own array schema. Found while triaging a sweep that flagged the `MXLEN`/`SXLEN` type asymmetry, which was verified **correct** and deliberately left alone |
| [PR #2090](https://github.com/riscv/riscv-unified-db/pull/2090) | **Merged.** A [review comment](https://github.com/riscv/riscv-unified-db/pull/2090#issuecomment-5084258197) here identified the same defect in the MTVEC alignment enums and the maintainer adopted the correction. **This is the maintainer's PR, not ours; the contribution is the review** |
| [PR #2097](https://github.com/riscv/riscv-unified-db/pull/2097) | Five-point review + frozen adversarial eval pack ([`workflow_slice/eval_2097/`](./riscv-param-extraction/workflow_slice/eval_2097/)) for the proposed parameter-extraction skill |
| [Issue #2053](https://github.com/riscv/riscv-unified-db/issues/2053) | Measured WARL and cross-model findings contributed to the Part II scope discussion |

### Path A vs Path B (do not collapse)

| Path | Proves | Not |
|------|--------|-----|
| **A — Challenge** | Optionality extract, grounding, schema YAML, CSR negative control, multi-model on 2 snippets, denser offline controls | Full-manual recall |
| **B — Corpus** | GT223/185 remeasure, 60-chunk multi-model, bulk export, honest WARL null | Substitute for challenge pack |
| **Holdout** | Method for leakage-audited CSR context under a frozen pin | Clean temporal proof under v1.2 (see PRIMARY_RESULTS) |

---

## Controls density (challenge surface)

| Control | This monorepo | Typical challenge kit |
|---------|---------------|------------------------|
| Bad fixtures (fail-closed) | **4** | often 2 |
| Hard negatives | **4** | often 2 |
| Known-param bench | **n=15** + leakage caveat | n≈13 |
| Live multi-model (2 snippets) | **10** (honest fails) | often 2–3 |
| CI gate | validate + negatives + markup + strategies + n=15 + holdout tests + export | validate-focused |
| Full-corpus multi-model + export | **Yes** (Path B) | usually no |

---

## Snapshot numbers (measured only)

| Item | Value |
|------|------:|
| Part I v2 remeasure (GT 185) | adj **72.9%** · class **88.4%** · WARL **50%** |
| Same vs live GT 223 | adj **64.2%** |
| Pilot machine.adoc | **model split** gpt-4o + gpt-4o-mini · ~**$0.05** |
| Artifact A (gpt-4o-mini vs Claude) | adj **32.2%** vs **72.9%** · Jaccard **3.8%** · ~**$0.16** |
| Artifact B | **83/83** named + **20/20** new schema-valid |
| named=yes | **87** rows / **83** unique |
| Holdout v1.2 (primary) | name **0/10** both arms · WARL **0/5** · exploratory null |

Authoritative tables: [`riscv-param-extraction/docs/metrics.md`](./riscv-param-extraction/docs/metrics.md).  
Holdout write-up: [`challenge/temporal_holdout/results/PRIMARY_RESULTS.md`](./riscv-param-extraction/challenge/temporal_holdout/results/PRIMARY_RESULTS.md).

---

## Layout

```
riscv-param-extraction/     mentor product
  challenge/                coding challenge + CI + live matrix + holdout
  docs/metrics.md           measured numbers
  export/  drafts/          Artifact B
  manifests/  results/      run records
application-packet/         Part II essay / plan / claim ledger
upstream-pr-drafts/         issue-linked drafts (open only if unclaimed)
.github/workflows/ci.yml    fail-closed challenge + export + holdout
```

**Local only (gitignored):** full `riscv-unified-db/` clone, private notes, and secrets.

---

## How to run (challenge CI)

```bash
cd riscv-param-extraction
pip install -r requirements.txt
python challenge/scripts/ci_check.py
```

---

## Limitations (honest)

- Artifact A second model is **gpt-4o-mini** (not full gpt-4o); mini **underperforms** Claude on corpus recall.  
- Pilot used a **model split** (org TPM limits), not pure gpt-4o.  
- Artifact B drafts are **DRAFT**, not unsolicited bulk UDB merges.  
- Challenge curated results are CI gold; live multi-model is under `challenge/results/live/` with per-model honesty.  
- Holdout v1.2 is an **exploratory null** with documented prompt-guidance limitations, not clean temporal-holdout proof.  
- Do **not** claim challenge n=2 scores beat Spring corpus recall on equal footing.  
- Upstream STVAL/HPM-style fixes may already be claimed by others. Open UDB PRs only when original and unclaimed.

---

## License

Code under this tree: see [`riscv-param-extraction/LICENSE`](./riscv-param-extraction/LICENSE). Vendored UDB schemas retain upstream BSD-3-Clause-Clear notices.
