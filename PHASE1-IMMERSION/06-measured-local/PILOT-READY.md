# Pilot READY — offline setup complete

**Status:** READY for key (zero API calls made while writing this)  
**Date prepared:** 2026-07-22  
**Budget law:** OpenAI credits ~$5 total · first paid action = **one** `pilot` only · target **cents** · stop if path looks > ~$0.50 before finish  

---

## Verified inventory

| Check | Result |
|-------|--------|
| UDB path | `Desktop\LFX-Mentorship\riscv-unified-db` |
| Branch | **lfx-1832** |
| `extract.py` | Present; subcommands `pilot \| run \| merge \| status` |
| Model alias | **`gpt4o`** → `gpt-4o-2024-11-20` (OpenAI) |
| `pilot` filter | `source_filter="machine.adoc"` only |
| Chunks | `param_extraction/chunks/manifest.json` present |
| machine.adoc chunks | **2**: `chunk_020` (~154 KB body) + `chunk_021` (~15 KB body) |
| Prompt versions | `prompts/v1` and `prompts/v2` present |
| Part I baseline metrics | v2 Claude → use **`PROMPT_VERSION=v2`** for fair pilot |
| `openai` package | Installed offline (`openai` 2.x) — import only, no network test |
| Artifact B | Intact under `riscv-param-extraction/` (83+20 schema-valid) |
| Full corpus status | Claude 60/79 done; **gpt-4o not started** |

---

## Exact commands (PowerShell)

### 1. cd

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
```

### 2. Set key (placeholder only until user pastes)

```powershell
# Do NOT commit. Do NOT write to .env in git tree if avoidable.
$env:OPENAI_API_KEY = "<PASTE_KEY_HERE>"
$env:PROMPT_VERSION = "v2"
```

### 3. Single paid pilot (ONLY approved first spend)

```powershell
python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v
```

| Flag | Why |
|------|-----|
| `pilot` | machine.adoc only — **not** full `run` |
| `--model gpt4o` | OpenAI path matching Part I alias |
| `--retries 0` | No paid re-attempt on parse failure (default is 1 → extra spend) |
| `-v` | Verbose for token/error visibility |
| **Do not** use `--force` | Would re-bill completed chunks |
| **Do not** run `extract.py run` | Full corpus — burns most of $5 |

### 4. Where results land

With `PROMPT_VERSION=v2`:

```text
param_extraction/results/v2/gpt-4o/chunk_020.json
param_extraction/results/v2/gpt-4o/chunk_021.json
```

(Default without env would be `results/gpt-4o/` under v1 — **always set v2**.)

### 5. How to read tokens / cost after run

- Console summary prints **Input tokens** / **Output tokens**.
- Each result JSON has `input_tokens`, `output_tokens`.
- Rough gpt-4o list pricing (check current OpenAI pricing page):  
  ~$2.50 / 1M input + ~$10 / 1M output  
- Offline estimate for **this** pilot (2 calls, v2 system prompt, rough char/4 tokens):  
  - ~45k input tokens total  
  - ~$0.10–$0.20 typical if output modest  
  - **~$0.27** if both calls hit large output (still under $0.50 abort line)  
- Fill `pilot-manifest.md` with **real** numbers from the run.

### 6. Abort conditions (STOP — ask user)

- Auth / billing errors  
- Any path that expands beyond machine.adoc  
- Estimated or observed spend trending **> ~$0.50** before pilot finishes  
- Urge to re-run pilot “to check” or start Artifact A without explicit yes  
- Missing chunks/manifest (fix offline; no paid retry as “debug”)

---

## After success (next agent)

1. Fill `PHASE1-IMMERSION/06-measured-local/pilot-manifest.md`  
2. Update `PROGRESS.md` + `PHASE1-STATUS.md`: pilot = DONE  
3. **STOP.** Do not start Artifact A full run unless user authorizes after seeing pilot cost.  
4. No GitHub push unless user orders it. Single home: `titoatwork/lfx-firstanalysis`.

---

## Forbidden until explicit user yes

- `extract.py run` (full or large source)  
- Multi-model full matrix  
- Second pilot / `--force` re-run  
- Writing key to disk, README, commits, or chat echo  

---

## READY gate line for next agent

> Setup complete. Zero spend so far.  
> Command: `python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v`  
> with `$env:PROMPT_VERSION="v2"` and `$env:OPENAI_API_KEY` set.  
> **API key please — I will run only the pilot once.**
