# Local clone (do not re-clone unless missing)

Path: `Desktop\LFX-Mentorship\riscv-unified-db`
Branch: `lfx-1832` (full Part I param_extraction tree)
Local PR branches: lfx-1765 lfx-1766 lfx-1791 lfx-1792 lfx-1793 lfx-1831 lfx-1832
isa-manual submodule: `ext/riscv-isa-manual` (checked out)

## Commands used
```powershell
cd Desktop\LFX-Mentorship
git clone https://github.com/riscv/riscv-unified-db
cd riscv-unified-db
foreach ($n in 1765,1766,1791,1792,1793,1831,1832) { git fetch origin pull/$n/head:lfx-$n }
git checkout lfx-1832
git submodule update --init ext/riscv-isa-manual
python param_extraction\scripts\export_udb_params.py
python param_extraction\scripts\map_params_to_spec.py
python param_extraction\scripts\generate_report.py
```

## Note on dirty tree
Phase 1 scripts were re-run; `param_extraction/data/*` may differ from PR freeze (185 → 223 params).
Committed Part I metrics live under `param_extraction/results/v2/`.
