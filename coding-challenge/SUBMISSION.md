# Coding challenge submission

**Applicant:** Ibteshamul Haque (`@titoatwork`)
**Project:** AI-assisted extraction of architectural parameters from RISC-V specifications, Part II
**Date:** 2026-08-04

The challenge asks for three things: details of the LLMs used, how the prompts were developed and how hallucination was handled, and results as YAML with fields for name, description, type and constraints. Sections 1, 2 and 3 answer those in order. Section 4 records what happened when I checked my own answer against the live database, which is the part I would read first.

| Item | Path |
|------|------|
| LLM details | §1 and `LLM-DETAILS.md` |
| Prompt development | §2 and `prompts/` |
| Results, as the challenge asks | `results/cmo_cache_blocks.yaml`, `results/csr_address_mapping.yaml` |
| Same results in real UDB schema shape | `results/udb-shaped/` |
| Snippets, verbatim | `snippets/` |

---

## Changes since submission

This pack was submitted on **2026-08-04**. The answer has not changed since:
`results/`, `prompts/` and `snippets/` are byte-identical to the submitted
version, and no parameter, prompt, model figure or conclusion has been revised.

Three things changed on **2026-08-11**, all of them in prose, and all listed here
so the repository can be diffed against the submitted PDF without surprises:

1. **A number was corrected.** §4 said "four upstream items" where the submitted
   PDF correctly says **six**. The public copy had understated it since first
   publication.
2. **The evidence base was published**, at
   [`riscv-param-extraction/challenge/`](../riscv-param-extraction/challenge/).
   Those runs are dated **2026-07-26**, before submission; the directory was held
   back pending review and simply never un-ignored. Nothing in it was produced
   after the deadline.
3. **Pointers and one disclosure were added.** §6 now names the offline command
   that checks this pack, and `LLM-DETAILS.md` explains why the newly published
   scorer prints 4 where the page publishes 3. That paragraph exists because
   publishing the scorer would otherwise leave a visible contradiction.

The git history carries all of it with timestamps.

---

## 1. LLMs used

Ten models were run on both snippets under the same v3 prompt at temperature 0. Full table in `LLM-DETAILS.md`.

| Field | Value |
|-------|-------|
| Model behind the submitted result | **gemini-3.6-flash** (Google AI), temperature 0 |
| Contrast model | **gpt-4o-mini-2024-07-18** (OpenAI), 128k context, temperature 0 |
| Others | gpt-4o-2024-11-20, llama-3.3-70b-versatile, nemotron-3 ultra / super / nano, ling-3.0-flash, laguna-s-2.1, gemma-4-26b |

I am naming the model that actually got the snippets right rather than the one I used most. That distinction matters, because model choice changed the answer:

| Model | CMO parameters found | CSR negative control |
|-------|---------------------:|----------------------|
| gemini-3.6-flash, nemotron-3-ultra, ling-3.0-flash | **3** | pass |
| llama-3.3-70b-versatile | 3 | **fail**, 5 false positives |
| gpt-4o-2024-11-20 | 1 | pass |
| gpt-4o-mini-2024-07-18 | 1 | **fail**, 1 false positive |

**4 of 10 models invented at least one parameter from the CSR snippet.** Five of ten under-extracted the CMO snippet. A single model run is not a safe basis for review, which is the practical finding from this exercise.

---

## 2. Prompts: development, refinement, hallucination

Full texts in `prompts/`.

| Version | Intent | Failure observed | Fix |
|---------|--------|------------------|-----|
| v1 naive | "List every architectural parameter" | Treated fixed CSR address conventions as parameters; invented constraints absent from the text; no evidence | Add the optionality triggers; require a verbatim quote |
| v2 keyword-anchored | Triggers plus required quote | Still invented structure; empty result never stated as acceptable | Make "zero is a valid answer" explicit; schema-shaped fields; forbid recall of UDB from memory |
| v3 schema-constrained | UDB-shaped YAML, closed world | Used for every run here | Independent axes when the text lists them separately; minimal schema when no value space is given |

### Anti-hallucination measures

1. **Closed world.** Only the snippet counts. No "recall the Privileged Spec".
2. **Verbatim quote per parameter**, mechanically checked as a whitespace-normalized substring of the snippet. All quotes in this pack pass.
3. **Zero is a correct answer.** Snippet 2 is a deliberate negative control.
4. **Do not invent enums** when the text says only "implementation-specific".
5. **Anti-hallucination at the schema layer, not just the quote layer.** If the value space is not enumerable, emit a minimal schema and say so, rather than inventing one that looks authoritative.
6. **Negative control by construction**, then measured: 4 of 10 models fail it, so it discriminates.

### Where the prompt is not the bottleneck

Every model that identified `CACHE_BLOCK_SIZE` correctly described it in prose as a "naturally aligned power-of-two" range. **None encoded that as a constraint in the schema.** Prompting improved which parameters were found; it did not make any model turn a stated property into a machine-checkable constraint. That is the one place in this submission where I overrode all ten models, and §4 explains why I am confident it is the right call.

---

## 3. Results

### Snippet 1, Privileged Spec 19.3.1 (CMO cache blocks)

Three parameters: `CACHE_BLOCK_SIZE`, `CACHE_CAPACITY`, `CACHE_ORGANIZATION`. See `results/cmo_cache_blocks.yaml`.

**How many parameters is this sentence?** The text reads "The capacity and organization of a cache and the size of a cache block are **both** implementation-specific." The word "both" joins two noun phrases that between them name three properties, so 1, 2 and 3 are all defensible readings:

- **1** bundled `CACHE_CONFIG`. Rejected: it overclaims a shared constraint the text does not state.
- **2**, following "both" literally: cache properties, and block size. Rejected: capacity and organization have no shared value space either, so the grouping is grammatical rather than architectural.
- **3**, one per independently varying property. Chosen.

I am flagging this rather than presenting 3 as obvious, because it is a modeling judgment and the SIG may reasonably disagree. §4 shows the database currently disagrees.

**Constraints extracted.** The snippet states three, and I encode all three rather than leaving them in prose:

- **Power of two.** "naturally aligned power-of-two (or NAPOT) range". This is the only hard, machine-checkable constraint in the passage.
- **Minimum 1.** A block cannot be zero bytes.
- **Uniform across the system.** "the size of a cache block shall be uniform throughout the system". Recorded, with a caveat: this is a system-level invariant, and a per-configuration parameter cannot express "every hart agrees". Noting the limit is more useful than silently dropping it.

No maximum is given, so none is invented.

### Snippet 2, Privileged Spec 2.1 (CSR address mapping)

**Zero parameters.** See `results/csr_address_mapping.yaml`.

The passage contains none of the optionality triggers. "By convention" describes a fixed, shared encoding of the 12-bit CSR address space, not an implementation choice. A model that emits `NUM_CSRS`, `CSR_ADDRESS_SPACE_SIZE` or `CSR_ACCESSIBILITY_ENCODING` here has hallucinated, and four of the ten did exactly that.

### Two shapes of the same answer

`results/*.yaml` uses the field names the challenge asks for: `name`, `description`, `type`, `constraints`. `results/udb-shaped/` carries the same content in the schema a real UDB parameter file uses, with `$schema`, `kind`, `definedBy` and a nested `schema:` block, and with evidence held alongside rather than inline, since `evidence_quote` is not a valid UDB key. The second form is what would actually be proposed upstream.

---

## 4. What happened when I checked this against the live database

I did not stop at producing YAML. I checked all three parameters against `riscv/riscv-unified-db`.

**Only one of the three exists.** Of the 227 parameters in `spec/std/isa/param/`, there is exactly one cache parameter, `CACHE_BLOCK_SIZE`. That count is 227 at `52822ae6`, the revision the analyses in this repository scanned, and still 227 at `4cf908e8`, checked 2026-08-06. There is no `CACHE_CAPACITY` and no `CACHE_ORGANIZATION`. I report those two as candidates, not as misses: the snippet does mark them implementation-specific, but neither is observable to software through the CMO extensions, which is a plausible reason the SIG has not modeled them. Deciding that is a mentor call, not mine.

**The extension gating was a hit.** I inferred `definedBy: anyOf [Zicbom, Zicbop, Zicboz]` from the section context. That matches the upstream file exactly.

**The constraint I encoded was genuinely missing upstream, and I fixed it.** Before my patch, UDB's own `CACHE_BLOCK_SIZE` read:

```yaml
long_name: TODO
schema:
  type: integer
  minimum: 1
  maximum: 18446744073709551615
```

The snippet says power-of-two. The database accepted 3 bytes, or 2^64-1. I filed [#2188](https://github.com/riscv/riscv-unified-db/issues/2188) and fixed it in [#2189](https://github.com/riscv/riscv-unified-db/pull/2189), merged as `57d70cfa`. The file now carries a power-of-two enum, a real `long_name`, and a NAPOT sentence in its description.

So the shape every model produced, `type: integer, minimum: 1`, is character for character the defective state I later corrected upstream. That is why §2 says the prompt was not the bottleneck.

**Why the fix is an inline enum and not a reference.** UDB has a reusable `$defs/64bit_unsigned_pow2`. Two things were in the way. That definition contained `4095`, which is not a power of two, which I filed as [#2137](https://github.com/riscv/riscv-unified-db/issues/2137) and fixed in [#2138](https://github.com/riscv/riscv-unified-db/pull/2138) with a regression test. And parameter schemas still cannot reference those definitions at all, because `idlc` raises "unhandled ref", which is open as [#2199](https://github.com/riscv/riscv-unified-db/issues/2199) with a fix in [#2212](https://github.com/riscv/riscv-unified-db/pull/2212).

One snippet from this challenge, six upstream items, two of them merged.

---

## 5. Honest limitations

- The submitted YAML is a human-reviewed reference result. `gemini-3.6-flash` reproduces the parameter set and the empty CSR answer; the power-of-two constraint is mine, and no model produced it.
- Three parameters from snippet 1 is a modeling judgment, not a fact. UnifiedDB models one, at `52822ae6` and still at `4cf908e8`.
- Extension gating on the CMO extensions follows the section context. Whether cache capacity should be gated that way is a SIG question.
- These are two snippets. Nothing here is a recall measurement, and it should not be read as one.

## 6. Reproducing

**Checking this submission needs no API key and no model call.** From the repository root:

```
./verify.sh
```

Gate 7 re-derives every figure in §1 from the raw per-model responses in
[`riscv-param-extraction/challenge/results/live/_raw/`](../riscv-param-extraction/challenge/results/live/_raw/):
the 4 CSR hallucinations, the 5 under-extractions, and the 3 fully correct. It
also holds §1's stricter "3" against the scorer's "4" so the two cannot drift
apart. The other six gates cover the rest of the repository.

To re-score or re-validate directly:

```
python riscv-param-extraction/challenge/scripts/score_live_matrix.py   # the ten-model matrix
python riscv-param-extraction/challenge/scripts/check_negatives.py     # 4 negative controls
python riscv-param-extraction/challenge/scripts/validate.py --results <dir>
```

**To re-run the models themselves**, which does need keys:

1. Take `prompts/v3_final.txt` and replace `{{SNIPPET}}` with a file from `snippets/`.
2. Temperature 0.
3. Check every `evidence_quote` appears in the snippet, whitespace-normalized, and that the CSR snippet returns an empty list.
