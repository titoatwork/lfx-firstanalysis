# Live multi-model matrix (requires your keys)

Anshul’s remaining hard lead on the **challenge axis** is a published
Sonnet / Opus / GLM matrix. Offline we already ship:

- curated grounded results + CSR=0
- multi-**strategy** disagreement (`scripts/score_strategies.py`)
- fail-closed CI denser than his fixture set

To take a **mile** on multi-model too, run live models and commit under
`results/live/<model>/` with evidence JSON.

## One-command dry-run (no spend)

```bash
cd riscv-param-extraction
python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt
python challenge/scripts/extract.py --snippet challenge/snippets/csr_address_mapping.txt
```

## Live (spend go required)

```bash
set OPENAI_API_KEY=...   # user shell only; never commit
python challenge/scripts/extract.py --snippet challenge/snippets/cmo_cache_block.txt --live --model gpt-4o-mini-2024-07-18 --retries 0
```

Recommended matrix (match/beat his breadth):

| Leg | Model | Role |
|-----|--------|------|
| 1 | gpt-4o-mini or Sonnet | primary cheap/frontier |
| 2 | second frontier if available | disagreement routing |
| 3 | open-weight (GLM / local) | omission vs hallucination |

After runs: place YAML + `*.evidence.json` under `results/live/<model>/`, then:

```bash
python challenge/scripts/validate.py --results challenge/results/live/<model>
```

**Campaign rules:** key + spend cap + explicit go; `--retries 0`; rotate keys after chat paste.
