# Preregistration: does leakage-audited CSR-field context improve parameter extraction?

**Status:** PREREGISTERED, amended once. Committed **before** any model call in any arm.
**Registered:** 2026-07-27 (commit `dfa6b23`, public timestamp 13:58:34Z)
**Amended:** 2026-07-27, same day, **before any run**. See Amendment 1.
**Supersedes:** an earlier small temporal-holdout pilot (n=10 positives, prompt v1.2) that returned
an exploratory null with documented guidance-leakage limitations. That pilot is local-only and is not
evidence about the context hypothesis. This document is the adequately powered test.

---

## Amendment 1: design widened from two arms to four

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

### H5, registered on 2026-07-28 before any run, from an external prediction

**H5 (agreement selects for easy cases).** Where two models independently propose the same new
candidate, that agreement concentrates on well-known quantities rather than on genuinely
implementation-defined ones. Under this hypothesis a dual-model agreement gate filters *toward* the
candidates a reviewer least needs help with, which would invert the value I claimed for it.

**Falsified if** the agreed set does not differ systematically from the model-exclusive sets on the
rubric below.

**Amended 2026-07-28, before any run.** My first wording said agreement selects "easier" cases and left
"easier" undefined until the names were visible. That is decided after seeing the list, which makes it
not a hypothesis. @RAJVEER42 identified this and proposed the fix used here. Every candidate, agreed or
exclusive, is labelled against UDB as exactly one of:

| Cat | Meaning | Checkable by |
|-----|---------|--------------|
| **1** | Absent from UDB and arguably should exist. A real gap, the `Smpmpmt` class | no param file, no derivation, normative implementation choice in the text |
| **2** | Absent because UDB **derives** it from other choices rather than treating it as a parameter | a function in `globals.isa`, or determined by which extension is implemented |
| **3** | Absent because it is **out of scope**: microarchitectural, or execution-environment | not ISA-visible |

**Every label also records its evidence type**, because two labels of the same category are not equally strong. `IALIGN` has an executable definition, so its derivation is a fact about the model and is machine-checkable across the whole repository. `FLEN` has prose in `F.yaml` saying the width follows from `F`/`D`/`Q`, which is a fact about the documentation and is not. Both are category 2; only one can be found automatically.

| Evidence type | Meaning |
|---------------|---------|
| `executable` | a derivation function exists, e.g. `function ialign` in `globals.isa` |
| `documented` | prose in a UDB file states the derivation, but nothing executes it |
| `absent` | neither; the label rests on the labeller's reading |

Counts are reported per category **and** per evidence type. A category-2 finding resting entirely on `documented` evidence is a weaker result than one resting on `executable`, and collapsing them would hide that. Distinction raised by @RAJVEER42.

**Labels of `unresolved` are permitted and are reported.** A rubric that never returns "unresolved" on a real case is not being applied honestly; `ILEN` is currently unresolved between 2 and 3 and stays that way.

All three are decided by inspecting the repository, with no reference to which arm or model produced
the candidate, so labelling is blind to the thing being tested. **Only category 1 counts as a genuine
missed parameter.** The claim under test is whether the agreed set is enriched for categories 2 and 3
relative to the exclusive sets.

Reported as counts per category per set. No significance testing at this n.

**Already-known result, recorded before the run so it cannot be presented as a discovery afterwards.**
Applying the rubric to the existing nine:

- `IALIGN` is **category 2, verified**. `spec/std/isa/isa/globals.isa` defines `function ialign`
  returning 16 or 32 depending on `C` and `misa.C`. No parameter file exists. Two models proposed it as
  a new parameter at high confidence and it is not one. Found by @RAJVEER42.
- `FLEN` is **category 2**, less cleanly. No parameter file and no derivation function, but the width
  follows from which of `F`/`D`/`Q` is implemented and UDB states this in extension prose.
- `ILEN` is **unresolved between 2 and 3**. No parameter file, no function, and its only whole-word
  appearance under `spec/std/isa` is inside a prose constraint in `Ziccif.yaml`.

So at least two of the nine dual-model candidates are not missed parameters, with a third unclear.
Dual-model agreement at high confidence did not filter them. That is a stronger and more damaging
result than the "skews easy" version, and it is checkable rather than inferred.

**Agreement must be computed within-arm, then pooled with the arm recorded per row.** Arms A and C
supply the gold catalogue to both models, so agreement in those arms is partly agreement on a list both
were handed. Merging the arms before computing agreement would let H0 leak into H5 and would quietly
invalidate the result. Raised by @RAJVEER42; I had not accounted for it and the analysis would have
been wrong without it.

Nine candidates cannot support a distributional claim. The four arms across five models should raise
the count, but the comparison is reported as counts per rubric category per set, never as a mean.

**Credit.** This prediction is [@RAJVEER42's](https://github.com/riscv/riscv-unified-db/issues/2053),
raised in issue #2053 from an 18-run study over 2 snippets. It is registered here because it is a
sharper objection to the dual-model gate than anything in my own analysis, and because testing it at
60-chunk scale costs nothing on a run that was happening anyway.

**Prior evidence, stated so it cannot be quietly dropped.** Of the nine dual-model candidates from
Artifact A, four (`FLEN`, `IALIGN`, `ILEN`, `NUM_PRIVILEGE_MODES`) are textbook quantities. That is a
qualitative read consistent with H5, not a measurement, and the per-chunk data needed to test it
properly was not retained from the earlier run. See section 8.

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

## 4b. Power and coverage, measured before running

Context is only attached to chunks that name a CSR, so treatment and baseline are byte-identical for
chunks with no CSR mention. That dilution has to be quantified before the run, not discovered after.

Of the 60 scored chunks, **32 receive context** and 28 do not. Taken alone that looks like heavy
dilution. But the gold parameters are not spread evenly across chunks. Mapping each gold parameter to
its best spec location and then to its chunk:

| Class | Gold (non-debug) | Located to a chunk | In a context-receiving chunk | Share |
|-------|-----------------:|-------------------:|-----------------------------:|------:|
| `NORM_CSR_RW` | 51 | 49 | 49 | **100%** |
| `NORM_CSR_WARL` | 24 | 23 | 21 | **91.3%** |
| `NORM_DIRECT` | 100 | 100 | 87 | 87.0% |
| `SW_RULE` | 2 | 2 | 2 | 100% |

So 21 of 24 gold WARL parameters sit in chunks the treatment can actually affect. The primary metric is
not crippled by dilution.

Two things are worth stating plainly because they cut against a clean reading:

1. **Three parameters could not be resolved to a chunk**, one of them WARL
   (`MTVEC_BASE_ALIGNMENT_VECTORED`). They are scored as normal; they simply cannot be attributed to a
   covered or uncovered chunk. No parameter is excluded from any denominator.
2. **Coverage itself follows the same ordering as CSR-reference density** (CSR_RW ≥ WARL > DIRECT).
   That is expected, since CSR-referencing parameters are described in CSR-mentioning passages, but it
   means coverage and the H2 gradient are not fully independent. H2 is therefore evidence about
   mechanism only in combination with the *magnitude* ordering, not from direction alone.

**Prespecified secondary analysis:** all per-class metrics are additionally reported restricted to the
32 context-receiving chunks. The full-corpus numbers remain primary. The restricted numbers are
reported whether or not they are more favourable.

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

## 5b. Registered 2026-07-28: baiting-clause stratification, and how to read a null

**Temperature 0 is not determinism, and that is measured here rather than assumed.** @RAJVEER42 reports
N=3 runs per model per snippet at `temperature=0` that were not identical in every case. Independently,
arm A of this experiment reproduces the published condition byte-for-byte and returns WARL 9/24 against
a published 3/24. Both arms are therefore run twice and diffed at the level of individual gold
parameters (`scripts/compare_runs.py`), and **no per-class claim is made from a single run**. Run-to-run
stability is reported as a first-class number alongside every metric.

**Baiting-clause stratification (registered as a stratification of the existing arms, not a fifth arm).**
The capacity failure @RAJVEER42 observed has two candidate causes with different fixes: a prompt gap, if
the wrong reading only appears when the passage places a discovery or enumeration clause next to the
implementation-defined clause, or a model prior, if it appears regardless.

Testing that properly wants paired passages differing only in the adjacent clause, which is a corpus
that does not exist. Rather than block on building one, the registered analysis is the cheapest tier
that uses data already in hand:

1. Label each of the 60 chunks for whether a discovery or enumeration clause sits adjacent to an
   implementation-defined clause. Labelling is done on chunk text alone, before results are examined.
2. Compare over-extraction rates across the two strata.

This is **observational and confounded**: chunks differ in more than the adjacent clause. It is
registered as a stratification with that limitation stated in the design rather than discovered in a
discussion section. Minimal-edit pairs, ten to twenty passages with only the adjacent clause deleted,
are the registered follow-up if and only if the stratification shows a difference worth pinning down.
Tiering proposed by @RAJVEER42.

**How a null must be read.** The four arms were chosen for H0. H5 and the capacity work ride on a design
built for a different question. A null on either is therefore reported as **"not detected under a design
built for something else"**, never as evidence of absence. Written here in advance so it cannot be
argued about afterwards.

## 6b. Artefact retention, made a hard requirement

The earlier Artifact A run kept per-chunk outputs local rather than committing them. The working clone
has since moved branches and those files are gone. The aggregates survive (236 and 218 high-confidence
proposed-new, 9 in both) but the **exclusive sets do not**, so the candidates each model proposed alone
cannot be recomputed or audited. That is a reproducibility failure in the artifact I have leaned on
most, and it is the direct reason H5 cannot be tested against existing data.

The runner therefore treats retention as a gate rather than a convenience. It must write, and the run
is void without them:

- every per-chunk response for every arm and model, raw, before parsing
- the parsed candidate list per chunk, with the arm and model recorded on each
- the agreed and model-exclusive candidate sets, materialised as name lists rather than counts
- token counts, cost, latency, refusals and parse failures per call
- the resolved prompt for at least one chunk per arm, so the arms can be diffed after the fact

Aggregate-only outputs are not acceptable. If a number appears in the write-up, the file it was
computed from is in the repository.

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
