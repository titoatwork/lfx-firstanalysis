# Manifest — Artifact A (gpt-4o-mini)

**Status:** `NOT_RUN` — fill after paid extract  
**Artifact:** A (multi-model vs Claude-sonnet-4 Part I baseline)  
**Repo:** [titoatwork/lfx-firstanalysis](https://github.com/titoatwork/lfx-firstanalysis) · `riscv-param-extraction/`  
**No secrets.**

---

## Claim (template — do not mark complete until real run)

Second-model extraction with **gpt-4o-mini** and **PROMPT_VERSION=v2** over Part I param-bearing chunks; metrics vs GT185; agreement + hallucination-overlap vs committed Claude v2. Honest if worse than Claude.

---

## Run configuration

| Field | Value |
|-------|--------|
| Date | _TBD_ |
| Upstream tree | local `riscv-unified-db`, branch **`lfx-1832`** |
| Monorepo branch | `analysis/artifact-a` |
| Tool | Part I `param_extraction/scripts/extract.py` |
| Model alias | `gpt4o-mini` |
| Model id | `gpt-4o-mini-2024-07-18` |
| Prompt version | **v2** |
| Retries | **0** |
| Force | **no** |
| Chunk set | Part I processable (60 param-bearing); skip_done for existing mini results |

### Command

```powershell
cd <path-to>/riscv-unified-db
$env:PROMPT_VERSION = "v2"
# OPENAI_API_KEY in session or gitignored .env — never committed
python param_extraction\scripts\extract.py run --model gpt4o-mini --retries 0 -v
python param_extraction\scripts\extract.py merge --model gpt4o-mini
```

---

## Tokens / cost (fill after run)

| Field | Value |
|------:|
| Input tokens | _TBD_ |
| Output tokens | _TBD_ |
| Approx cost (USD) | _TBD_ |
| Chunks OK | _TBD_ |
| Chunks skipped / errors | _TBD_ |

### Skips / errors

| Chunk | Reason |
|-------|--------|
| _none yet_ | |

### Pre-existing (not re-billed)

| Chunk | Source |
|-------|--------|
| chunk_020 | pilot 2026-07-22 (gpt-4o-mini) |

---

## Analysis outputs (fill after offline steps)

| Artifact | Path |
|----------|------|
| Merged | `param_extraction/results/v2/all_results_gpt-4o-mini.json` |
| Metrics (analyze) | `param_extraction/results/metrics_gpt-4o-mini.json` |
| Agreement JSON | `riscv-param-extraction/results/artifact_a_agreement.json` |
| Public tables | `docs/metrics.md` §5 |

---

## Limitations (update after run)

- Second model is **gpt-4o-mini**, not full gpt-4o corpus.  
- Headline recall vs **GT185** (Part I freeze), not silently mixed with live GT223.  
- Pilot machine.adoc model-split remains a **separate** claim.  
