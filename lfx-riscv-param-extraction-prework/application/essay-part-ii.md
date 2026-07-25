# Application essay — AI params Part II only

**Updated:** 2026-07-26  
**Canonical paste-ready copy:** [`../../application-packet/ESSAY-PART-II.md`](../../application-packet/ESSAY-PART-II.md)  
**Claim ledger:** [`../../application-packet/MEASURED-CLAIM-LEDGER.md`](../../application-packet/MEASURED-CLAIM-LEDGER.md)

Use when applying to this project on LFX. Do **not** paste the multi-project profile intro unchanged.

Public prework: https://github.com/titoatwork/lfx-firstanalysis

---

## Short version (~150–200 words)

```text
I am applying to AI-assisted extraction of architectural parameters from RISC-V
specifications – Part II (LFX Fall 2026).

I studied and reproduced the public Spring Part I work on riscv-unified-db
(credit: @ishaan-arora-1 / PRs #1765–#1832) rather than treating it as a black
box. Against the pinned 185-parameter gold I remeasured 72.9% adjusted recall,
88.4% classification accuracy, and 50% WARL recall; against the live 223-
parameter set, adjusted recall falls to 64.2%, which shows why pinned and
evolving golds both matter.

I then shipped two concrete pre-apply artifacts in
github.com/titoatwork/lfx-firstanalysis: a schema-valid draft UDB YAML exporter
(83 existing named parameters + 20 candidates) and a controlled 60-chunk second-
model run with gpt-4o-mini (PROMPT v2). Mini reached only 32.2% adjusted recall
versus the public Claude baseline of 72.9%, with 3.8% parameter-name Jaccard.
A prompt-only WARL ablation was negative (matched WARL 3/24 → 2/24).

These results motivate grounded CSR context, cross-model/human review gates,
explicit provenance, and small reviewable PRs—not bulk generation. I can commit
≥30 hours/week for the Fall term.
```

---

## Longer version

See `application-packet/ESSAY-PART-II.md` section 2 (full 350–500 word text with A/B/v3, export path, UM research, logistics).

---

## Form Q&A modules

See `application-packet/ESSAY-PART-II.md` sections 3–8 (why this project, experience, technical approach, outcomes, availability, repo link).

---

## Wording rules (do not break)

- Reproduce Spring work; do **not** claim Spring authorship  
- 83 unique named / 87 rows — never 97  
- Artifact A = gpt-4o-mini, not pure gpt-4o  
- Pilot = model split  
- Nine dual-model names = candidates, not confirmed parameters  
- v3 = null WARL result, not a success  
- Schema-valid ≠ architecturally correct  
- Original CSR-field Artifact C = **not complete**  
