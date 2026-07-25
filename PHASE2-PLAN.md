# Phase 2 — Execution plan (Artifact A focus)

**Status:** ACTIVE  
**Plan lock:** `PLAN-SOURCE-OF-TRUTH.md` + `GITHUB-PRESENTATION.md`  
**Grok entry:** root `AGENTS.md` · `HANDSOFF.md` · this file when executing A  
**Started:** 2026-07-22  
**Budget:** ~**$5** OpenAI remaining (pilot already spent ~$0.05)

---

## Phase 2 map (what “done” means)

| ID | Artifact | Status | Notes |
|----|----------|--------|--------|
| **B** | CSV → draft UDB YAML + schema validate | **DONE** | 83 named unique + 20 new drafts; monorepo path |
| **A** | Multi-model extract + agreement vs Claude Part I | **DONE** (2026-07-24/25) | mini 32.2% vs Claude 72.9%; Jaccard 3.8%; ~$0.16 |
| **C** | WARL recall stretch / v3 prompt ablation | **Done — null WARL** | Prompt-only v3 did not lift WARL; see metrics §6 |
| **Obj 3** | Manifests every serious run | Pilot + A done | Add v3 manifest when complete |
| **Public surface** | README + `docs/metrics.md` + samples | Mostly done | A tables public; push reframe if needed |

**Do not** re-open pilot unless user says so.  
**Do not** full `extract.py run` on gpt-4o without a cost gate (TPM + $).

---

## What Artifact A must deliver (locked plan)

Using Part I pipeline (same chunks, v2 prompts where possible):

1. **Second-model extraction** (GPT or Gemini) — not Claude re-run required if Part I Claude v2 results already on disk  
2. **Per-class recall** vs Claude-sonnet-4 Part I baseline (and vs GT)  
3. **Inter-model agreement** (name overlap / match rate)  
4. **Hallucination-overlap** (LLM_NEW high-conf both models vs only one)  
5. **Honest numbers if worse**  
6. **Manifests:** model id, prompt version, tokens, cost, command, commit/chunk set  

Compare primarily to **committed Part I Claude v2** results already produced in Spring (~60 chunks merged), not to a new Claude bill.

---

## Hard constraints from pilot

| Fact | Implication for A |
|------|-------------------|
| gpt-4o org TPM **30k** | Any chunk ≳30–35k input **fails** (chunk_020 ~44k) |
| Full Claude v2 was ~**1.03M in / 83k out** tokens | Full gpt-4o at list prices can approach or exceed **$5–10** |
| gpt-4o-mini ran 44k OK at **~$0.008** for one huge chunk | **mini is the realistic full-corpus model on $5** |
| Pilot model-split claim already public story | A can be **gpt-4o-mini vs Claude Part I** (honest, strong) |

---

## Recommended path (default)

### A0 — Offline first ($0) — do before any key

1. Confirm machine has:
   - `riscv-unified-db` on **`lfx-1832`**
   - Part I Claude results under `param_extraction/results/v2/` (or equivalent)
   - Prototype `riscv-param-extraction/` (or monorepo copy)
2. Inventory chunks: count, which exceed ~28k estimated tokens (TPM-safe margin)
3. Wire **`gpt4o-mini`** alias in extract.py if not already (from pilot work)
4. Scaffold analysis scripts in prototype or thin wrappers:
   - load Claude merged results + new model merged results
   - compute agreement / unique-to-model / class confusion sketch
   - emit tables for `docs/metrics.md`
5. Dry-run `extract.py status` / merge paths with **no API**
6. Write `manifests/artifact-a-plan.md` with exact commands + abort rules
7. **READY gate** → ask user for key

### A1 — Paid run (user go-ahead only)

**Default model:** `gpt-4o-mini` (full or near-full `extract.py run`)  
**Prompt:** `PROMPT_VERSION=v2`  
**Retries:** `0`  
**Force:** never unless intentional re-spend  

**Hard rules:**
- Stop and ask if projected spend **> ~$4.50** (leave tiny buffer)
- Skip or split only chunks that still fail limits; document skips
- Do **not** re-run Claude
- Do **not** re-pilot machine.adoc “for fun”

**After run:**
- `merge` → `analyze.py` metrics vs GT185 (and note GT223 if useful)
- Agreement tables vs Claude v2 param sets
- Fill `docs/metrics.md` + public manifest
- Local commit; push only if user orders

### A2 — Publish

- README: remeasure → pilot split → **A tables** → B  
- Small result samples only; large JSON gitignored  
- Optional later: sig-parameters short note (after A+B public)

---

## Alternative paths (only if user chooses)

| Path | When | Risk |
|------|------|------|
| **A-mini full** (default) | $5 budget, want complete A | Quality vs Claude may be lower — **OK if honest** |
| **A-stratified** (e.g. 15–25 high-value chunks) | Even tighter money | Must document “not full corpus” |
| **A-gpt4o partial** | Only small chunks on 4o + mini for large | Messy model mix; more bookkeeping |
| **A-gemini** | Free/cheap Google key | Extra setup; still valid 2nd model |
| **Full gpt-4o all chunks** | Need tier raise + more $ | Likely **over budget** + TPM pain |

---

## Cost gut-check (order of magnitude)

Part I Claude scale: ~1M input tokens for ~60 chunks.

| Model (ballpark) | Full-ish run |
|------------------|--------------|
| gpt-4o | often **multi-dollar to $10+** — risky on $5 |
| gpt-4o-mini | often **well under $5** if run is clean — **target** |
| Stratified 20 chunks | cents–low dollars |

Exact cost: measure after first 3–5 chunks; abort if burn rate too high.

---

## Honest claim templates (A)

**Good:**
> Second-model extraction with gpt-4o-mini (v2 prompts) over Part I chunks; metrics and agreement vs committed Claude-sonnet-4 Part I results; manifests include tokens/cost. Chunks skipped for limit reasons listed.

**Bad:**
> “Matched or beat Claude on all classes” (unless true)  
> “Full gpt-4o multi-model matrix” (unless true)  
> Invented agreement % without a run

---

## Non-goals

- Unsolicited UDB mega-PR  
- Re-clone / re-deep-study Phase 1  
- Spending remaining $5 on pilot retries  
- Claiming B as Phase 2 “still to build” (B is done)  
- Apply to LFX until A evidence is written up (target apply window still Jul 31–Aug 2)

---

## Immediate next actions

1. **User decision:** confirm **A-mini full** (recommended) or alternative  
2. **User:** which machine has UDB + prototype (this Mac currently lacks both clones)  
3. **Agent offline:** inventory + mini alias + agreement scaffold + READY  
4. **User:** rotated API key + spend go-ahead  
5. **Agent:** run → analyze → docs → stop  

---

## Session kickoff snippet (after user confirms A-mini)

```text
EXECUTE PHASE2-PLAN.md + PLAN-SOURCE-OF-TRUTH.md + GITHUB-PRESENTATION.md
Phase 2 Artifact A only. B done. Pilot closed.
Budget ~$5 OpenAI. Model default: gpt-4o-mini, PROMPT_VERSION=v2, retries 0.
Offline ready gate first; zero API until I paste key.
After key: run/merge/analyze; manifests; metrics tables; no full gpt-4o; no UDB PR; no push unless ordered.
```

---

*Phase 2 plan locked to monorepo presentation rules. Replace only if user changes strategy.*
