# Interview / walkthrough sheet — Part II

**Date:** 2026-07-26  
**Public path:** root README (badge) → challenge README → metrics → live matrix → holdout PRIMARY_RESULTS → essay/ledger  

**Apply target:** 2026-08-02 (locked). This sheet is for technical walkthrough only.

---

## 60-second pitch

Part II continues Spring LFX parameter extraction: LLMs over RISC-V specs, gold evaluation including UDB YAML, maintainable merges. I reproduced public Spring work—credit @ishaan-arora-1 / #1765–#1832—and measured 72.9% adjusted recall on pinned GT185 and 64.2% on live GT223. I shipped a denser coding-challenge pack (4 fail-closed fixtures, 4 hard negatives, n=15 mechanics, 10-model live matrix with honest CSR fails, green CI), a schema-valid exporter (83+20), a 60-chunk mini vs Claude ablation (32.2% vs 72.9%, Jaccard 3.8%), a negative WARL prompt result, and a preregistered CSR-context holdout with a locked exploratory null (0/10 name recall both arms, limitations documented). Public home: github.com/titoatwork/lfx-firstanalysis.

---

## Five-minute walkthrough

| Min | Open | Say |
|-----|------|-----|
| 0–1 | Root README + CI badge | One monorepo; denser challenge controls than a minimal kit; Path A/B/holdout |
| 1–2 | `challenge/README.md` | Same 2-snippet exam; 4 bad / 4 hard-neg / 10 live / n=15; one `ci_check` |
| 2–3 | metrics §1–2, §5 | Reproduction 72.9%/64.2%; mini 32.2% vs Claude; Jaccard 3.8% |
| 3–4 | metrics §7 + drafts | Exporter 83+20 schema-valid only |
| 4–5 | holdout PRIMARY_RESULTS + plan | Exploratory null under v1.2 limits; Fall needs leakage-audited context + small PRs |

---

## Challenge density (if they only open the kit)

| Control | Number |
|---------|--------|
| Bad fixtures | 4 |
| Hard negatives | 4 |
| Live multi-model | 10 (4 full CMO+CSR pass offline re-score) |
| Known-param mechanics | n=15 (15/15 existence; not blind corpus) |
| Holdout | locked 26/26 exploratory null |

Commands: `python challenge/scripts/ci_check.py` · `python challenge/scripts/score.py`

---

## Definitions (crisp)

| Term | Answer |
|------|--------|
| Architectural parameter | ISA-constrained implementer choice: name + value domain + definedBy |
| Adjusted recall | Part I metric with allowed alignments |
| WARL parameter | Legal value set of a WARL CSR field is the parameter |
| Schema-valid | Passes param_schema structure; not architectural approval |
| Cross-model agreement | Shared names; low Jaccard → review, not truth |
| Exploratory null (holdout) | 0/10 name recall both arms under v1.2; not clean temporal proof |

---

## Survive these technical questions

**Exact vs adjusted recall?**  
Exact = identical names; adjusted allows Part I alignments. Headline remeasure uses adjusted.

**Why recall fell on live gold?**  
Gold 185→223; same LLM output, larger denominator → 72.9%→64.2%.

**Why 3.8% Jaccard matters?**  
Same chunks/prompt; disagreement is model-driven. Dual agreement prioritizes review.

**Schema-valid proves?**  
Structure only — not reality or merge-readiness.

**v3 WARL more labels, fewer matches?**  
Over-labeling without better identification → honest null.

**Holdout treatment didn’t help?**  
On mini + v1.2, name/WARL stayed 0/10 and 0/5. Self-audited guidance leakage; neg FP not attributable to treatment (identical negative prompts). Harness still valuable as method.

**Context without leaking gold names?**  
CSR-field text; leak_scan fail-closed; no class on UDB YAML; eval metadata separate.

**Why small PRs?**  
Review load; Spring extract still unmerged; bulk dumps fail review culture.

---

## Strong questions for mentors

1. When Manual YAML, keyword spreadsheet, and UDB YAML disagree, which wins?  
2. Evidence bar for a new architectural parameter?  
3. Preferred export path into UDB for Part II?  
4. Best PR size for timely review?  
5. First Fall deliverable: workflow robustness or small reviewed set?  
6. How to represent one-to-many conceptual alignments?  
7. Required review fields on every generated candidate?

---

## Tone checks

- Credit Spring; never claim authorship  
- Never claim holdout “proved” CSR context success  
- Never claim n=15 beats corpus recall  
- Never claim we “beat” named competitors  
