# Preregistration: does leakage-audited CSR-field context improve parameter extraction?

**Status:** PREREGISTERED. Written and committed **before** any treatment-arm model call.
**Registered:** 2026-07-27
**Supersedes:** the temporal-holdout pilot (`challenge/temporal_holdout/`), which tested a related
question at n=10 positives under prompt v1.2 and returned an exploratory null with documented
guidance-leakage limitations. That result is not evidence about the context hypothesis. This is the
adequately powered test.

---

## 1. Question

Spring Part I extraction is weakest on WARL parameters. Against the pinned 185-parameter gold, the
committed Claude-sonnet-4 v2 output reaches **72.9%** adjusted recall overall but only **50%**
(12/24) on `NORM_CSR_WARL`. A prompt-only intervention (v3) failed: overall recall rose to 35.0% on
gpt-4o-mini while WARL recall *fell* from 3/24 to 2/24.

A WARL parameter is not defined by the prose that mentions it. It is defined by the **set of legal
values of a CSR field**, and that information lives in the CSR definition, not in the surrounding
specification text. The hypothesis is therefore mechanistic rather than stylistic: extraction fails on
WARL because the model is not shown the object the parameter is about.

## 2. Why this is testable rather than merely plausible

Every parameter in the gold carries its CSR references. Counting them **before running anything**
gives a gradient across classes:

| Class | n (non-debug) | Params with ≥1 CSR reference | Share |
|-------|--------------:|-----------------------------:|------:|
| `NORM_CSR_WARL` | 24 | 22 | **91.7%** |
| `NORM_CSR_RW` | 51 | 38 | 74.5% |
| `NORM_DIRECT` | 100 | 24 | 24.0% |

If CSR-field context helps **because** it supplies legal-value-set information, its benefit must track
this gradient. If it helps `NORM_DIRECT` as much as `NORM_CSR_WARL`, the mechanism is wrong and any
gain is prompt bulk, position effects, or noise.

This is the part the prior pilot could not test and the part no prompt-tweak result can claim.

## 3. Hypotheses, fixed in advance

| ID | Statement | Falsified if |
|----|-----------|--------------|
| **H1** *(primary)* | Treatment raises `NORM_CSR_WARL` recall above baseline on the same model and corpus | WARL recall does not increase |
| **H2** *(mechanism)* | Recall gain is ordered `WARL ≥ CSR_RW ≥ DIRECT` | DIRECT gain exceeds WARL gain |
| **H3** *(replication)* | H1 holds in direction for a majority of models tested | H1 direction fails in most models |

**H2 is the load-bearing hypothesis.** H1 alone is weak evidence: adding any text can move a small
denominator. H1 together with H2 is evidence about the mechanism. H1 without H2 will be reported as a
gain of unknown cause, not as support for the hypothesis.

## 4. Design

**Arms** (identical in every other respect, temperature 0):

- `baseline` — specification chunk only. Byte-identical to the prompt used for the published v2 runs.
- `treatment` — the same chunk, plus a CSR-field context block.

**Context construction, and how leakage is prevented.** Context must be selected without consulting
the gold, or the experiment is circular. Selection is therefore driven **only by the chunk text**:

1. Scan the chunk for CSR names that exist in the UDB `spec/std/isa/csr` tree.
2. For each CSR found, emit its field definitions: field name, location, description, and legal-value
   language.
3. **Scrub** every gold parameter name and normalised variant from that text.
4. Emit **no** parameter YAML, no `param_schema` content, and no gold classification.
5. A fail-closed scan aborts the run if any gold name or variant survives into a context file.

The gold is used only for scoring, never for building context or selecting chunks.

**Corpus.** The 60 param-bearing chunks from the published Artifact A run, unchanged.

**Models.** Two paid and three free, all pinned by exact snapshot id:

| Model | Provider | Role |
|-------|----------|------|
| `gpt-4o-2024-11-20` | OpenAI (paid) | Strongest available |
| `gpt-4o-mini-2024-07-18` | OpenAI (paid) | Comparable to published Artifact A and v3 |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | OpenRouter | Replication |
| `gemini-3.6-flash` | Google | Replication |
| `inclusionai/ling-3.0-flash:free` | OpenRouter | Replication |

Replication across independent providers is what separates a real effect from one model's quirk.

## 5. Scoring, fixed in advance

Scoring uses the existing `param_extraction/scripts/analyze.py` with no modification. Denominators are
the published ones, verified reproducible before registration: **DIRECT 100, CSR_RW 51, WARL 24,
SW_RULE 2** (debug-spec prefixes excluded, matching `docs/metrics.md`).

- **Primary metric:** `NORM_CSR_WARL` recall, treatment minus baseline, per model.
- **Secondary:** per-class recall for all four classes; overall adjusted recall.
- **Reported regardless of outcome:** token counts, cost, refusal and parse-failure counts, and every
  per-case decision.

## 6. Stopping and analysis rules

- Both arms run to completion on all 60 chunks per model before any scoring.
- No prompt edits after the first treatment call. A prompt defect discovered mid-run voids that model's
  run; it is re-registered and re-run, and the void is reported.
- No model is dropped for producing an unfavourable result. Models dropped for API failure are named,
  with the failure.
- WARL n=24 is small. A one- or two-case difference is noise, and will be reported as such rather than
  as a lift.

## 7. Commitment

The result is published in this repository whichever way it falls. A null is a real finding: combined
with the v3 prompt-only null it would mean neither prompt guidance nor retrieved CSR context fixes
WARL, which is itself an argument that the problem needs structural work rather than better prompting.

Both outcomes are written into the nine-week plan before the result is known:

- **If supported:** context retrieval becomes the spine, and the follow-on question is which parts of
  the CSR definition carry the signal.
- **If null:** the plan leads with WARL as an open problem, with the eval harness and two eliminated
  hypotheses as the contribution.

*No result had been observed at the time this file was committed.*
