# Measured facts — cite these, do not invent

Source of truth for tables: `riscv-param-extraction/docs/metrics.md`  
Pilot detail: `riscv-param-extraction/manifests/pilot-machine-adoc.md`  
Artifact A detail: `riscv-param-extraction/manifests/artifact-a-gpt-4o-mini.md`  
Local remeasure JSON: `PHASE1-IMMERSION/06-measured-local/metrics_summary.json`

```
GT live UDB:                 223 params; 100% any / 91% strong match
Part I v2 vs GT185:          adj recall 72.9%, class acc 88.4%, WARL 50%
Part I v2 vs live GT223:     adj recall 64.2%, class acc 88.6%, WARL 50%
parameters.csv named=yes:     87 rows / 83 unique  (NEVER claim 97 without recount)
Artifact B named export:     83/83 schema-valid
Artifact B new (limit 20):   20/20 schema-valid
Pilot:                       COMPLETE_WITH_MODEL_SPLIT ~$0.05
  chunk_021: gpt-4o-2024-11-20 — ~10115 in / 1152 out, 6 params, ~$0.037
  chunk_020: gpt-4o-mini-2024-07-18 — ~44874 in / 1541 out, 9 params, ~$0.008
  reason: gpt-4o org TPM 30k blocked ~44k input chunk
Artifact A (v2, mini, 60/60): COMPLETE — adj 32.2% vs Claude 72.9%; WARL 12.5%;
                              name Jaccard 3.8%; high-conf new both 9; ~$0.16
v3 WARL ablation (mini):     COMPLETE null: adj 35.0%; WARL 8.3% (2/24) vs A WARL 12.5%
```

If disk disagrees after a real remeasure, update metrics.md + this file + AGENTS.md + AGENT-RULES.md §9 in the same session.
