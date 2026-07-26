# Draft review for riscv/riscv-unified-db#2097

**Status:** ready to post (one comment; no pings)  
**Tone:** constructive, evidence-based, collaborative

---

## Comment body (paste into #2097)

Thanks for landing a parameter analogue of the instruction-extraction skill — the signal families, NOTE-skipping, and mandatory verbatim excerpt are the right anti-hallucination core for Part II-style work.

I reproduced the skill *rules* (not a paid re-run of the agent) against a small frozen adversarial pack built from existing open corpus/challenge fixtures in https://github.com/titoatwork/lfx-firstanalysis (`riscv-param-extraction/workflow_slice/eval_2097/`). Cases:

**Positives (5)** — DIRECT / CSR_RW / WARL  
- `CACHE_BLOCK_SIZE` (implementation-specific cache block)  
- `NUM_PMP_ENTRIES` (implementation-defined count)  
- `MTVEC_ACCESS` (RO vs RW choice)  
- `MTVEC_MODES` (true WARL: legal MODE set is implementation-chosen)  
- `ASID_WIDTH` / ASIDLEN-style width  

**Negatives (4)**  
- Fixed CSR address-mapping convention (shared challenge negative)  
- Software/compiler “should/may” advice (not a hardware parameter)  
- Pure shall constraint without implementation delegation  
- **WARL vocabulary with an ISA-fixed legal set** (legal value must be 0 for all implementations; not implementation-defined)

### Concrete observations

1. **WARL as almost-always-positive signal**  
   The skill ranks `WARL` under “almost always name a parameter.” That matches many real cases (`MTVEC_MODES`), but the fixed-legal-set negative shows a failure mode: the *word* WARL can appear where the legal *set* is fully fixed by the ISA. WARL-field misclassification is already a central Part II / Spring pain point; a skill aimed at parameters should require that the **set of legal values** is implementation-chosen, not merely that the field is labeled WARL.

2. **“Superset of param_schema” vs mergeable UDB files**  
   The documented output is a top-level `parameters:` list with `excerpt` / `source` / `classification` / `status`. That is a valuable **review envelope**, but it is not a file that validates as `param_schema.json` (missing required fields such as `kind`, `long_name`, `description`, and the wrapper key is outside the parameter object schema). Calling it a schema superset can over-promise merge readiness.

3. **“Compare by name and meaning” for existing/new**  
   Duplicate detection is underspecified for renames and conceptual duplicates. Spring Part I needed curated one-to-many alignments; a skill step should either point at an explicit alias/alignment table or mark uncertain duplicates as `possible_duplicate` rather than binary existing/new.

4. **`definedBy` from subsection ownership**  
   Inferring `definedBy` only from the subsection’s owning extension is unsafe for multi-extension gates (e.g. CMO `anyOf`) and param-gated parameters (e.g. usable PMP count depending on `NUM_PMP_ENTRIES`).

5. **No automated validation / negatives in the skill itself**  
   The two worked examples help, but without negative controls and a machine check that (a) every candidate has an excerpt present in the subsection and (b) post-review emission validates as UDB YAML, regressions will be hard to catch.

### Suggested two-artifact design

Separate the products of the skill:

1. **Review envelope** (what the skill should emit first): evidence excerpt, anchor, classification, confidence/uncertainty, existing/new/possible-duplicate, proposed name, proposed `definedBy`, open questions.  
2. **Clean UDB parameter YAML** (param_schema-valid only): emitted **after** human approval — no review-only keys, no `parameters:` wrapper.

Happy to contribute the frozen fixtures + a small validator (`workflow_slice/eval_2097/`) in whatever form is preferred (subtree under the skill, separate test path, or follow-up PR). No need to take any of this as blocking if you already planned a review-envelope split — flagging so Part II WARL and schema-validity expectations stay aligned.

Reproduction (no API):

```bash
cd riscv-param-extraction
python workflow_slice/eval_2097/scripts/validate_eval_pack.py
python workflow_slice/scripts/ci_slice_check.py
```
