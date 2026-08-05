# FAQ

Definitions used in this repository, and direct answers to questions the measurements invite. If an answer here conflicts with [`docs/metrics.md`](../riscv-param-extraction/docs/metrics.md), the metrics win.

## Definitions

| Term | Meaning as used here |
|------|----------------------|
| Architectural parameter | An ISA-constrained implementer choice: a name, a value domain, and the extension that defines it |
| Adjusted recall | Part I metric allowing documented name alignments rather than exact string equality only |
| WARL parameter | The parameter is the set of legal values of a WARL CSR field, not the field itself |
| Schema-valid | Passes `param_schema` structurally; not a claim of architectural correctness |
| Cross-model agreement | Shared parameter names between two models; low Jaccard is a review signal, not truth |
| Exploratory null | Result that finished under documented limitations and is reported rather than discarded |

## Gold names in the prompt

**Were the gold parameter names given to the model?**  
Yes, for the published Part I-style figures. Prompts inject all 185 gold names with an instruction to reuse exact names when they match. Those figures measure **grounding** (locate and evidence catalogue entries), not discovery without a catalogue. Discovery without the list is unmeasured; see [`artifact_c/PREREGISTRATION.md`](../riscv-param-extraction/artifact_c/PREREGISTRATION.md).

**Does that change how WARL rates should be read?**  
Yes. WARL at 12/24 with all correct names already supplied is an identification failure, not a missing-vocabulary failure. Prompt-only WARL guidance that increases labels without improving matches is consistent with that.

## Stability and scoring

**Why report exact and adjusted recall separately?**  
Exact requires identical names; adjusted allows Part I alignments. Headline remeasure uses adjusted; both appear in metrics.

**Why does recall fall from 72.9% to 64.2%?**  
The gold set grew from the 185-parameter Part I freeze to the **223** UDB carried at corpus pin `c184e313`. Same LLM output, larger denominator. 223 is the count at that pin and not a live figure: `main` carried 227 when this was first published, which is corrected on [#2053](https://github.com/riscv/riscv-unified-db/issues/2053).

**Why does a 3.8% name Jaccard matter?**  
Same prompt and chunk set across models, so disagreement is largely model-side. Dual-model agreement alone is not a sufficient review gate (derived non-parameters have appeared in high-confidence overlap lists).

**Prompt v3 produced more WARL labels but fewer correct ones. Why keep it?**  
It failed cleanly: more labels, worse matched WARL rate. Prompt-only guidance is the wrong lever if the failure mode is identification.

**Temporal holdout returned 0/10 in both arms. Is the harness broken?**  
The harness completed under a pinned model and immutable run directory. Limitations of prompt v1.2 (including label-revealing negatives) are documented in the results. That is an exploratory null, not proof for or against CSR context.

## Upstream

**Where is the list of UDB PRs and issues?**  
[`EVIDENCE.md`](./EVIDENCE.md), re-checked against GitHub as of the census date on that page.

**Are issue/PR comments part of the prework measurements?**  
Yes. Several recall and taxonomy figures were first or also posted on UDB threads (#2053, #2163, #2200, #2251). They are indexed in [`metrics.md` §8](../riscv-param-extraction/docs/metrics.md) next to the local tables. Cite the issue link when you mean the public discussion; cite this repo when you mean the offline artifact re-derivation.