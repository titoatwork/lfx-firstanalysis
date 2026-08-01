# Enum literal validation (string-enum params vs IDL)

| | |
|--|--|
| **Outcome** | **Open** |
| Issue | [#2285](https://github.com/riscv/riscv-unified-db/issues/2285) |
| PR | [#2289](https://github.com/riscv/riscv-unified-db/pull/2289) |
| Related | Instance fix for `always_zero` also discussed on [#2271](https://github.com/riscv/riscv-unified-db/pull/2271) |

Adds a smoke check so `PARAM ==/!= "..."` literals against `schema.enum` fail CI when invalid. PR body: [`PR_BODY.md`](./PR_BODY.md).
