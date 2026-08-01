# PR body (filed) — counter-enable requirements

**Outcome:** merged as [#2266](https://github.com/riscv/riscv-unified-db/pull/2266) · closes [#2265](https://github.com/riscv/riscv-unified-db/issues/2265)

---

fix(param): enforce the counter-enable rules the descriptions already state

---

`MCOUNTENABLE_EN`, `SCOUNTENABLE_EN` and `HCOUNTENABLE_EN` carry the same three sentences in their descriptions: an unimplemented counter cannot be enabled, bits 0 to 2 must be false without `Zicntr`, and bits 3 to 31 must be false without `Zihpm`. Only `SCOUNTENABLE_EN` encodes all three in `requirements`. `MCOUNTENABLE_EN` encodes one and `HCOUNTENABLE_EN` has no `requirements` block, so both accept configurations their own descriptions forbid.

This adds the missing clauses, copying the encoding `SCOUNTENABLE_EN` already uses. `MCOUNTENABLE_EN` keeps its existing counter-existence clause, which is the same rule written as a contrapositive. No cross-level clause is added, since the privileged spec states that a bit in `mcounteren` does not affect whether the corresponding bit in `scounteren` is writable.

No configuration changes status. Of the seven under `cfgs/` that set any of these parameters, none is newly rejected.

Closes #2265
