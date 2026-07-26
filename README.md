# LFX Mentorship — lfx-firstanalysis

**Owner:** Ibteshamul Haque · GitHub: [titoatwork](https://github.com/titoatwork)  
**Project:** [AI-assisted architectural parameter extraction – Part II](https://mentorship.lfx.linuxfoundation.org/project/22296947-cecb-4a8f-8bcb-4f34710e9f66)  
**Mentors:** Allen Baum, Ajit Dingankar · **Upstream:** [riscv/riscv-unified-db](https://github.com/riscv/riscv-unified-db)

Public prework for LFX Fall 2026 Part II: **coding-challenge pack**, **measured corpus science**, **schema-valid export drafts**, and **live multi-model results**.

Spring Part I (extract → analyze → spreadsheet) was built on open UDB PR branches **#1765–#1832** by [@ishaan-arora-1](https://github.com/ishaan-arora-1). This repo **reproduces**, **remeasures**, and **extends** — it does **not** claim Part I authorship.

---

## 5-minute mentor path

| # | Open |
|---|------|
| 1 | **[Coding challenge pack](./riscv-param-extraction/challenge/)** — 2 snippets, validate, CSR=0, fail-closed CI, live multi-model |
| 2 | **[Measured tables](./riscv-param-extraction/docs/metrics.md)** — GT remeasure, Artifact A, B, WARL null |
| 3 | **[Live multi-model matrix](./riscv-param-extraction/challenge/results/live/MANIFEST.md)** — honest per-model CMO/CSR |
| 4 | **[Export + drafts](./riscv-param-extraction/)** — `export/`, `drafts/param/`, `drafts/param-new/` |
| 5 | **[Application packet](./application-packet/)** — essay, 9-week plan, claim ledger |
| 6 | **[Upstream PR drafts](./upstream-pr-drafts/)** — issue-linked param data fixes ready to open (STVAL_WIDTH #2102, HPM_EVENTS #2046; not bulk dump) |

### Path A vs Path B (do not collapse)

| Path | Proves | Not |
|------|--------|-----|
| **A — Challenge** | Optionality extract, grounding, schema YAML, CSR negative control, multi-model on 2 snippets | Full-manual recall |
| **B — Corpus** | GT223/185 remeasure, 60-chunk multi-model, bulk export, honest WARL null | Substitute for challenge pack |

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

Authoritative tables: [`riscv-param-extraction/docs/metrics.md`](./riscv-param-extraction/docs/metrics.md).

---

## Layout

```
riscv-param-extraction/     mentor product (challenge, metrics, export, drafts, live results)
  challenge/                coding challenge + CI surface
  docs/metrics.md           measured numbers
  export/  drafts/          Artifact B
  manifests/  results/      run records
application-packet/         Part II essay / plan / claim ledger
upstream-pr-drafts/         small UDB fix draft (reviewable)
.github/workflows/ci.yml    fail-closed challenge + export tests
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
- Artifact B drafts are **DRAFT** — not unsolicited bulk UDB merges.  
- Challenge curated results are CI gold; live multi-model is under `challenge/results/live/` with per-model honesty.  
- Do **not** claim challenge n=2 scores beat Spring corpus recall on equal footing.  

---

## License

Code under this tree: see [`riscv-param-extraction/LICENSE`](./riscv-param-extraction/LICENSE). Vendored UDB schemas retain upstream BSD-3-Clause-Clear notices.
