# PR: fix(param): HPM_EVENTS duplicate index and HPM long_names

**Target:** `riscv/riscv-unified-db`  
**Branch:** `fix/hpm-events-dup-index` (local commit `021a2d7a` on clone)  
**Closes:** #2046  
**Author:** Ibteshamul Haque · `titoatwork`

## Summary

1. **`HPM_EVENTS.yaml`:** remove duplicate `HPM_COUNTER_EN` / `index: 4` entry
   in `definedBy.allOf[1].param.anyOf` (schema does not enforce uniqueness).
2. **`HPM_EVENTS.yaml` / `HPM_COUNTER_EN.yaml`:** replace `long_name: TODO`
   with real short titles.
3. **`HPM_COUNTER_EN.yaml`:** correct non-existent CSR spelling
   `mhmpcountinhibit` → `mcountinhibit` in the description.

## Diff scope

- 2 files under `spec/std/isa/param/`
- No value-schema redesign; no bulk dump

## Test plan

- [ ] `grep -n "index: 4" spec/std/isa/param/HPM_EVENTS.yaml` appears once
- [ ] `./do test:schema` still passes
- [ ] Description CSR name matches Privileged Spec (`mcountinhibit`)

## Suggested title

```
fix(param): HPM_EVENTS duplicate index and HPM long_names (#2046)
```
