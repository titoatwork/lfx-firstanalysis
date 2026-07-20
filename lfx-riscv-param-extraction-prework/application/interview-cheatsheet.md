# Interview / async Q cheatsheet — Part II

---

## 60-second project pitch

“Part II continues Spring LFX and Parameter SIG work: extract architectural parameters from priv/unpriv ISA text with LLMs, score against gold lists including UDB YAML, improve classification, make the pipeline reproducible as agents/skills, export real UDB param YAML, and get reviewed PRs merged. Spring V2 got adjusted recall to roughly the low seventies but WARL-class params and merge/export are still open problems—that’s the Fall quality and robustness mandate.”

---

## Definitions (must be crisp)

| Term | Answer |
|------|--------|
| Architectural parameter | Impl-defined ISA-constrained knob: name + value domain + definedBy |
| vs instruction | Instructions are ops; params configure legal widths/modes/options |
| Recall | Fraction of gold params found |
| WARL param | Legal value set for a write-any-read-legal field (e.g. MTVEC_MODES) |
| UDB param file | `spec/std/isa/param/NAME.yaml` under param_schema |

---

## Official 5 goals (memorize)

1. Extract + recreate full gold lists (a Manual YAML, b spreadsheet, c UDB)  
2. Extend classification  
3. Agents/skills, reproducible prompt/context  
4. Export to UDB YAML  
5. PR + merge follow-up  

---

## Spring numbers (approximate; say “from public PR writeups”)

- Adjusted recall V1→V2: ~62.7% → ~72.9%  
- Class accuracy: ~67.9% → ~88.4%  
- WARL recall V2: ~50%  
- Chunks: 78; CSR splits: 0  
- Spreadsheet ~330 medium+; tags ~321  

---

## Likely questions

**Q: Why not just use GPT on the PDF?**  
A: Need structured taxonomy, alignment to gold, reproducibility, schema-valid UDB output, human review—Spring showed single-pass chat is not enough.

**Q: What would you do week 1?**  
A: Pin SHAs, reproduce eval, build error book (WARL/naming/FP), agree KPI with mentors.

**Q: How do you stop hallucinations?**  
A: Neg few-shots, skip NOTE, confidence filters, human rubric for “new”, precision tracking, no bulk merge.

**Q: Experience with LLMs?**  
A: Research pipeline used local/controlled LLM stages with measured overhead mindset; here I’ll treat models as extractors under eval harness. (Stay truthful to COLIDE without confidential links.)

**Q: Hours?**  
A: At least 30/week for the full term.

**Q: Weaknesses?**  
A: Not on Spring team—need handoff week; will be explicit about uncertainty in classifications.

---

## Questions to ask them

See `notes/questions-for-mentors.md` — pick KPI, handoff SHA, merge priority.

---

## Red flags to avoid

- Claiming Spring authorship  
- Guaranteeing 95% recall  
- “I’ll PR 200 new params in week 2”  
- Ignoring WARL / merge gap  
- Under 30h/week  
