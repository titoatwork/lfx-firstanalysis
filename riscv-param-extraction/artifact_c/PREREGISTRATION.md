# Preregistration: does leakage-audited CSR-field context improve parameter extraction?

**Status:** PREREGISTERED, amended once. Committed **before** any model call in any arm.
**Registered:** 2026-07-27 (commit `dfa6b23`, public timestamp 13:58:34Z)
**Amended:** 2026-07-27, same day, **before any run**. See Amendment 1.
**Supersedes:** the temporal-holdout pilot (`challenge/temporal_holdout/`), which tested a related
question at n=10 positives under prompt v1.2 and returned an exploratory null with documented
guidance-leakage limitations. That result is not evidence about the context hypothesis. This is the
adequately powered test.

---

## Amendment 1 — design widened from two arms to four

**What changed.** The registered design compared prose-only against prose-plus-CSR-context. It now
also varies whether the gold parameter name list is supplied.

**Why.** While building the runner, I traced prompt assembly in `param_extraction/scripts/extract.py`.
Every prompt is built by `build_user_message()`, which unconditionally injects
`format_param_names_section(load_udb_param_names())`. That list is read from `data/udb_param_names.txt`
and is **set-identical** to the 185 parameters in `ground_truth.json`:

```
injected list size : 185
gold set size      : 185
identical sets     : True
```

Both originally registered arms would therefore have run with the complete answer key in the prompt.
The experiment would have measured whether CSR context improves *grounding against a supplied
catalogue*, which is a narrower question than the one worth asking, and the registered mechanism claim
would have been confounded: a model that already has every correct name cannot be failing for lack of
vocabulary.

**State at amendment.** No model call had been made in any arm. No result of any kind had been
observed. The original two-arm text is preserved in git history at `dfa6b23`.

**Consequence.** The primary hypothesis changes. Discovery recall, meaning extraction without the name
list, is unmeasured in this repository and appears unmeasured publicly. It becomes H0 below, and the
CSR-context question is evaluated both with and without the catalogue.

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
| **H0** *(primary, new in Amendment 1)* | Removing the gold name list substantially reduces recall, so published figures depend materially on the supplied catalogue | Recall without the list is close to recall with it |
| **H1** | CSR context raises `NORM_CSR_WARL` recall above the matched no-context arm | WARL recall does not increase |
| **H2** *(mechanism)* | Recall gain from context is ordered `WARL ≥ CSR_RW ≥ DIRECT` | DIRECT gain exceeds WARL gain |
| **H3** *(replication)* | H1 holds in direction for a majority of models tested | H1 direction fails in most models |
| **H4** *(substitution)* | CSR context recovers more recall when the name list is absent than when present | Context helps equally or more in the catalogue-supplied condition |

**H0 is now the headline.** It is a measurement, not a guess, and no prediction is registered for its
magnitude because I have no basis for one. Whatever it returns is the finding.

**H2 remains load-bearing for the context claim.** H1 alone is weak: adding any text can move a small
denominator. H1 with H2 is evidence about mechanism. H1 without H2 will be reported as a gain of
unknown cause.

**H4 is the question the amendment makes possible.** If context substitutes for the catalogue, then
retrieval is doing real extraction work rather than decorating a lookup task.

## 4. Design

**Arms.** Two binary factors, name list and CSR context, giving four cells. Temperature 0 throughout,
identical in every other respect.

| Arm | Gold name list | CSR context | Purpose |
|-----|:--------------:|:-----------:|---------|
| **A** | yes | no | Reproduces the published condition exactly. Validates the harness against known figures |
| **B** | **no** | no | **Discovery recall. The unmeasured number** |
| **C** | yes | yes | The originally registered context question |
| **D** | no | yes | Does context substitute for the catalogue (H4) |

Arm A is a control in the strict sense: if it does not land near the published figures for the same
model, the harness is wrong and no other arm is interpretable. It is scored first and its agreement
with `docs/metrics.md` is reported before anything else.

The name list is removed by omitting `format_param_names_section` from the assembled user message.
Nothing else changes: the system prompt, the few-shot examples and the chunk section are byte-identical
across arms.

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
