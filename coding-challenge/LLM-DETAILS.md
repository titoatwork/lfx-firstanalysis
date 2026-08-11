# LLM details

All ten models below were run on both challenge snippets under the same prompt
(`prompts/v3_final.txt`) at temperature 0, on 2026-07-26. No model was given the
answer, the other models' output, or anything beyond the snippet.

## Model behind the submitted result

| Field | Value |
|-------|-------|
| Name | **gemini-3.6-flash** |
| Version / snapshot | `3.6-flash-07-2026` |
| Vendor / route | Google AI, free tier |
| Temperature | 0 |
| Context length | 1,048,576 input tokens, 65,536 output tokens |
| Why this one | It is one of three models that found all three CMO parameters **and** correctly returned zero for the CSR snippet |

## Contrast model, named because it failed informatively

| Field | Value |
|-------|-------|
| Name | **gpt-4o-mini** |
| Version / snapshot | gpt-4o-mini-2024-07-18 |
| Vendor | OpenAI |
| Context length | 128,000 tokens |
| Temperature | 0 |
| API | Chat Completions |
| Result | Found 1 of 3 CMO parameters, and invented `CSR_ACCESSIBILITY_ENCODING` from the CSR snippet |

I used gpt-4o-mini for most of my prework because it is cheap and deterministic
enough for controlled runs. On this challenge it is the wrong model, and saying
so is more useful than quietly submitting under it.

## Full matrix, both snippets

| Model | Route | CMO parameters | CSR negative control |
|-------|-------|---------------:|----------------------|
| nvidia/nemotron-3-ultra-550b-a55b:free | OpenRouter | **3** | pass |
| inclusionai/ling-3.0-flash:free | OpenRouter | **3** | pass |
| gemini-3.6-flash | Google AI | **3** | pass |
| nvidia/nemotron-3-super-120b-a12b:free | OpenRouter | **3** | pass, with caveat |
| llama-3.3-70b-versatile | Groq | 3 | **fail**, 5 false positives |
| gpt-4o-2024-11-20 | OpenAI | 1 | pass |
| nvidia/nemotron-3-nano-30b-a3b:free | OpenRouter | 1 | pass, with caveat |
| gpt-4o-mini-2024-07-18 | OpenAI | 1 | **fail**, 1 false positive |
| poolside/laguna-s-2.1:free | OpenRouter | 1 | **fail**, 1 false positive |
| google/gemma-4-26b-a4b-it:free | OpenRouter | 1 | **fail**, 1 false positive |

"Pass, with caveat" means the API returned no output for the CSR snippet rather
than an explicit empty list. Counted as zero, flagged rather than hidden.

**Totals: 4 of 10 hallucinated on the CSR snippet. 5 of 10 under-extracted the
CMO snippet. 3 of 10 got both fully right.**

The scorer counts the "fully right" figure as **4**, because it treats a caveat
row as a pass. This page publishes **3**, excluding
`nemotron-3-super-120b-a12b`, on the rule that returning nothing is not the same
as answering zero: a model that emits no output has not demonstrated it can
decline. The other caveat row, `nemotron-3-nano-30b-a3b`, is excluded either way,
since it found 1 of 3 CMO parameters.

The difference is visible in the raw captures, not in the curated results, which
write the same `NO_PARAMETERS_FOUND` marker for both cases. In
`challenge/results/live/_raw/`, the CSR response from
`nemotron-3-super-120b-a12b` is `(No output)`, while
`nemotron-3-ultra-550b-a55b` returned
`(No parameters extracted — the snippet describes fixed architectural conventions only.)`
and `gemini-3.6-flash` returned a refusal with its reasoning. Both numbers are
correct under their own rule and the stricter one is published;
`check_challenge_matrix.py` holds the two together so they cannot drift.

## What this matrix does and does not show

It shows model choice changes the answer on a two-snippet task, and that a
negative control separates models that a positive-only test would rank equally.

It is not a recall measurement. Two snippets is not a corpus, and none of these
numbers should be compared against extraction figures measured on the 60-chunk
set in my prework repository.

One result is uniform across all ten and is not a model-quality difference:
every model that found `CACHE_BLOCK_SIZE` described it as a naturally aligned
power-of-two range in prose, and **none** encoded that as a schema constraint.
See `SUBMISSION.md` section 4.

Model metadata above is as reported by the Google AI `models.get` endpoint. The
version string is a July 2026 build, matching the 2026-07-26 run date.

## Cost and keys

Free tiers and ordinary API usage. No key is committed anywhere in this pack;
keys were supplied through the environment at run time.
