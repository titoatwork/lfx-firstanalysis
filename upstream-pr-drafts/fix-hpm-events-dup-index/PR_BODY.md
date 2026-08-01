# PR body (not filed) — HPM_EVENTS duplicate index

**Outcome:** not filed. Already owned for [#2046](https://github.com/riscv/riscv-unified-db/issues/2046).

Draft below is historical.

---

## Summary

1. **`HPM_EVENTS.yaml`:** remove duplicate `HPM_COUNTER_EN` / `index: 4` entry in `definedBy.allOf[1].param.anyOf` (schema does not enforce uniqueness).
2. **`HPM_EVENTS.yaml` / `HPM_COUNTER_EN.yaml`:** replace `long_name: TODO` with real short titles.
3. **`HPM_COUNTER_EN.yaml`:** correct non-existent CSR spelling `mhmpcountinhibit` → `mcountinhibit` in the description.

## Diff scope

- 2 files under `spec/std/isa/param/`
- No value-schema redesign; no bulk dump

## Test plan

- `index: 4` appears once in `HPM_EVENTS.yaml`
- Schema validation still passes
- Description CSR name matches Privileged Spec (`mcountinhibit`)
