# Interview / walkthrough sheet — Part II

**Date:** 2026-07-26  
**Public walkthrough path:** root README → metrics → A manifest → B exporter → v3 null → nine-week plan  

---

## 60-second pitch

Part II continues Spring LFX work on extracting architectural parameters from RISC-V specs with LLMs, scoring against gold lists including UDB YAML, and landing maintainable merges. I reproduced the public Spring pipeline—credit @ishaan-arora-1 and PRs #1765–#1832—and measured 72.9% adjusted recall on the pinned 185-parameter gold and 64.2% on the live 223-parameter set. I built a schema-valid draft UDB YAML exporter for 83 existing and 20 candidate parameters, ran a 60-chunk gpt-4o-mini comparison that scored only 32.2% versus Claude’s 72.9% with 3.8% name Jaccard, and published a negative prompt-only WARL result (3/24→2/24). That evidence says Part II needs grounded context, review gates, provenance, and small PRs—not bulk generation. Public prework is on github.com/titoatwork/lfx-firstanalysis.

---

## Five-minute walkthrough

| Min | Open | Say |
|-----|------|-----|
| 0–1 | Root README | Problem + single public home + headline numbers |
| 1–2 | metrics §1–2 | Reproduction: GT223, 72.9% / 64.2%, WARL 50% |
| 2–3 | metrics §5 + A manifest | Multi-model: 32.2% vs 72.9%, Jaccard 3.8%, 9 dual-new candidates |
| 3–4 | metrics §7 + drafts/ | Exporter: 83+20 schema-valid; structural only |
| 4–5 | metrics §6 + nine-week plan | v3 null; Fall plan → 5 objectives; small PRs |

---

## Definitions (crisp)

| Term | Answer |
|------|--------|
| Architectural parameter | ISA-constrained implementer choice: name + value domain + definedBy |
| Adjusted recall | Part I metric accounting for allowed alignments (not only exact string match) |
| WARL parameter | The set of legal values of a Write-Any-Read-Legal CSR field is the parameter |
| Schema-valid | Passes UDB JSON schema structure; **not** mentor architectural approval |
| Cross-model agreement | Shared extracted names; low Jaccard → review protocol, not automatic truth |

---

## Survive these technical questions

**Exact vs adjusted recall?**  
Exact requires identical names; adjusted allows curated alignments / one-to-many groups from the Part I analyzer. Headline remeasure uses Part I’s adjusted definition.

**Why did recall fall on live gold?**  
Gold grew 185→223; same LLM output covers a larger denominator → 72.9%→64.2%. Gold drift matters.

**Why is 3.8% Jaccard important?**  
Same chunks and prompt; disagreement is model-driven. Single-model “discoveries” are mostly private; dual agreement is a review priority signal, not truth.

**Schema-valid proves / does not prove?**  
Proves structural conformance to param_schema. Does not prove the parameter is real, correctly named, or merge-ready.

**How did v3 get more WARL labels but fewer matches?**  
Prompt encouraged WARL-class tagging; alignment to gold WARL names still failed → over-labeling without better identification.

**Context grounding without leaking gold names?**  
Auxiliary CSR-field text only; leakage audit strips exact/normalized gold names before API; hashes pre/post filter.

**Why small PRs?**  
Spring extraction work still sits on open PRs; bulk dumps are hard to review. Tooling and tiny reviewed data batches match maintainer load.

**How are candidates human-reviewed?**  
Rubric: accept / reject / defer; require excerpt + class + confidence + provenance; export only accepted rows.

---

## Strong questions for mentors

1. When Manual YAML, keyword spreadsheet, and UDB YAML disagree, which is authoritative?  
2. What evidence is enough for a proposed new architectural parameter?  
3. Is manual-side params.yaml the expected export path Part II should align with?  
4. What PR size has the best chance of timely review?  
5. First deliverable: workflow robustness or a small reviewed parameter set?  
6. How should one-to-many conceptual alignments be represented?  
7. What review fields must accompany every generated candidate?

---

## Tone checks

- Credit Spring; never claim authorship  
- Honest about mini underperformance and v3 null  
- No fake certainty / no applicant probability lectures  
- No “I’ll merge 200 params in week 2”  
