# Pilot runbook (Phase 1 last technical step)

**Authoritative ready-check:** [PILOT-READY.md](./PILOT-READY.md)  
**Manifest template:** [pilot-manifest.md](./pilot-manifest.md)

## Goal
One extraction pilot on `machine.adoc` using Part I `extract.py` (**~cents**, not full corpus).

## Prerequisites
- `riscv-unified-db` on branch `lfx-1832`
- API key for **one** provider (do not commit keys; do not paste into git)
- Offline: `pip install openai` already done for OpenAI path
- Prefer **`PROMPT_VERSION=v2`** (matches Part I remeasure baseline)

## Budget law (user — OpenAI ~$5 credits)
- First paid action only: `pilot --model gpt4o`
- **Forbidden** without explicit yes: `extract.py run`, `--force`, multi-model full, re-pilot “to check”
- Use `--retries 0` to avoid paid parse-failure re-calls
- Stop if spend path looks **> ~$0.50** before pilot completes

## Commands (OpenAI — preferred for this budget)

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"
$env:OPENAI_API_KEY = "<your key>"
$env:PROMPT_VERSION = "v2"
python param_extraction\scripts\extract.py pilot --model gpt4o --retries 0 -v
```

Results (v2): `param_extraction/results/v2/gpt-4o/chunk_020.json` and `chunk_021.json`  
(machine.adoc is **two** chunks — two API calls, still pilot scope.)

### Other providers (not first if saving OpenAI $5)

```powershell
# Anthropic (Part I default model family)
# $env:ANTHROPIC_API_KEY = "<key>"
# $env:PROMPT_VERSION = "v2"
# python param_extraction\scripts\extract.py pilot --model claude --retries 0 -v

# Gemini
# python param_extraction\scripts\extract.py pilot --model gemini --retries 0 -v
```

## After success
1. Fill **real** tokens/cost in `pilot-manifest.md`  
2. Update `PHASE1-STATUS.md` and `PROGRESS.md`: pilot = DONE  
3. **STOP** — do not start Artifact A full run unless user authorizes after seeing cost  

## Failure
- Auth errors → key/env  
- Missing deps → `pip install openai` (or anthropic / google genai)  
- Diagnose offline; **no automatic re-spend**  
- Do not invent pilot metrics without a real run  
