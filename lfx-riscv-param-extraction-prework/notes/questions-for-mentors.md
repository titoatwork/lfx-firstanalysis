# Questions for mentors (Allen Baum, Ajit Dingankar)

Use in application (1–2), interview, or week-0 email. Prefer **specific** over generic.

---

## Priority (ask early)

1. **KPI:** For Fall graduation, what is the primary success metric—adjusted recall vs UDB, WARL-class recall, precision on “new” params, number of schema-valid YAML merges, or something else?  
2. **Handoff:** Which Spring artifacts are canonical (PR branches, tarball, Drive folder)? Which git SHAs pin gold lists (a)(b)(c)?  
3. **Access:** When do mentees get Google Drive `keyword_matches` and per-chapter Manual YAML (1a/1b)?  
4. **Merge path:** Prefer landing `param_extraction` tooling on UDB main, reviewed `spec/std/isa/param/*.yaml`, isa-manual `[#param:]` tags, or a staging repo first?  
5. **Multi-model:** Is multi-LLM comparison required for robustness, or one strong model + ablations enough if metrics are clean?

---

## Technical depth

6. For `NORM_CSR_WARL`, should extraction target **legal value sets** only, or also emit coupled access params (`*_ACCESS`) in the same pass?  
7. How should **one-to-many** UDB groups be maintained—curated allowlist (Spring style) vs learned rules?  
8. Preferred home for agent skills—UDB `.agents/skills/`, separate repo, or Parameter SIG materials?  
9. How strict is **IDL `requirements`** completeness for new YAML exports in Fall?  
10. Interaction with **Parameter SIG** deliverables outside UDB (encodings, non-UDB consumers)?

---

## Process

11. Expected cadence (sync meetings, async updates)?  
12. Review SLA for PRs (who are code owners for params)?  
13. Any license/data constraints on LLM providers for ISA text?

---

## Questions I will **not** lead with

- “What is RISC-V?”  
- “Can you guarantee I’ll be selected?”  
- “Please assign me issues before acceptance.”  
