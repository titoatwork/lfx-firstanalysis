# Technical FAQ

Definitions used throughout this repository, and direct answers to the questions the measurements invite. If an answer here conflicts with [`docs/metrics.md`](../riscv-param-extraction/docs/metrics.md), the metrics win.

## Definitions

| Term | Meaning as used here |
|------|----------------------|
| Architectural parameter | An ISA-constrained implementer choice: a name, a value domain, and the extension that defines it |
| Adjusted recall | The Part I metric, allowing the documented name alignments rather than requiring exact string equality |
| WARL parameter | The parameter is the *set of legal values* of a WARL CSR field, not the field itself |
| Schema-valid | Passes `param_schema` structurally. It says nothing about architectural correctness or merge-readiness |
| Cross-model agreement | Shared parameter names between two models. Low Jaccard is a signal to review, not evidence of truth |
| Exploratory null | A result that did not reach its endpoint under known limitations, reported rather than discarded |

## The condition attached to every recall number

**Were the gold parameter names given to the model?**
Yes. Every Part I prompt injects all 185 gold names, a set identical to the ground truth, with the instruction to reuse them exactly. So every published recall figure measures grounding, locating which catalogue entries apply to a passage and evidencing them, rather than discovery. For the Spring deliverables that is the right design. It does mean no published number shows whether a model can find parameters unaided, and that measurement is [preregistered](../riscv-param-extraction/artifact_c/PREREGISTRATION.md) but not yet run.

**Does that invalidate the WARL finding?**
It sharpens it. WARL recall is 12/24 with all 24 correct names already in the prompt, so the failure is identification rather than vocabulary. That also explains why prompt-only WARL guidance made results worse: more instruction does not help a model that was never missing the name.

## Questions the numbers raise

**Why report exact and adjusted recall differently?**
Exact requires identical names; adjusted allows the Part I alignments. The headline remeasure uses adjusted, and both are in metrics §2.

**Why does recall fall from 72.9% to 64.2%?**
The gold set grew from the pinned 185 parameters to 223 live ones. Same LLM output, larger denominator. Nothing about the extraction changed.

**Why does a 3.8% name Jaccard matter?**
Prompt and chunk set were held constant across two models, so the disagreement is attributable to the model rather than the pipeline. It means a single model's list of "new" parameters cannot be trusted without a review gate. The nine names both models proposed are review candidates, not confirmed parameters.

**Prompt v3 produced more WARL labels but fewer correct ones. Why report it?**
Because it failed. Raw WARL class labels rose from about 36 to 59 while matched WARL recall fell from 3/24 to 2/24. More confident labelling is not more correct labelling, and prompt-only guidance is the wrong lever for WARL.

**The temporal holdout returned 0/10 in both arms. Is the harness broken?**
The harness ran to completion, 26/26 calls, with the model pinned and an immutable run directory. Prompt v1.2 carried case-specific guidance and label-revealing negatives, which is documented in the results. It is an exploratory null under known limitations, not evidence that CSR context does or does not fix WARL. The negative false-positive difference is not attributable to the treatment, because the negative prompts were byte-identical across arms.

**How is context added without leaking gold names?**
CSR-field text only, with a fail-closed leak scan, no classification sourced from UDB YAML, and evaluation metadata kept separate from model input.

**Why small upstream PRs instead of bulk generated YAML?**
Review capacity is the binding constraint, and the Spring extraction is still unmerged. A large generated dump adds review load without adding trust. Every upstream change from this work is issue-linked and small enough to read in one sitting.

**What does the challenge pack actually establish?**
Two snippets, with four fail-closed fixtures, four hard negatives, markup robustness cases, and ten live models. It establishes extraction mechanics and negative-control behaviour. It is not corpus-scale recall, and the known-parameter bench (n=15) scores mechanics on committed pairs, with pretraining leakage applying to any public UDB set.

## Open questions for maintainers

1. When the Manual YAML, the keyword spreadsheet, and UDB YAML disagree, which is authoritative?
2. What is the evidence bar for proposing a genuinely new architectural parameter?
3. What is the preferred export path into UDB for Part II output?
4. What PR size gets reviewed most reliably?
5. Is the more useful first deliverable workflow robustness, or a small reviewed set of parameters?
6. How should one-to-many conceptual alignments be represented?
7. Which review fields should every generated candidate carry?
