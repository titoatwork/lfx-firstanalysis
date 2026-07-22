# Pilot runbook (Phase 1 last technical step)

## Goal
One extraction pilot on `machine.adoc` using Part I `extract.py` (~cents).

## Prerequisites
- `riscv-unified-db` on branch `lfx-1832`
- API key for one provider (do not commit keys; do not paste into git)

## Commands

```powershell
cd "C:\Users\Ibteshamul Haque\Desktop\LFX-Mentorship\riscv-unified-db"

# Anthropic (matches Part I default)
$env:ANTHROPIC_API_KEY = "<your key>"
python param_extraction\scripts\extract.py pilot --model claude -v

# OR OpenAI
# $env:OPENAI_API_KEY = "<your key>"
# python param_extraction\scripts\extract.py pilot --model gpt4o -v

# OR Gemini (ensure Google client env as required by extract.py)
# python param_extraction\scripts\extract.py pilot --model gemini -v
```

## After success
1. Note output path under `param_extraction/results/`  
2. Record in `pilot-manifest.md` (create next to this file):

```text
date:
model alias:
model_id:
prompt version:
input_tokens:
output_tokens:
approx_cost_usd:
command:
notes:
```

3. Update `PHASE1-STATUS.md` and `PHASE1-CLOSEOUT.md` checklist: pilot = DONE  
4. Phase 1 technical fully closed → Phase 2 OK to start  

## Failure
- Auth errors → key/env  
- Missing deps → `pip install anthropic` / `openai` / google genai per extract.py errors  
- Do not invent pilot metrics without a real run  
