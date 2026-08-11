Eighteen instruction descriptions name an operand the file never declares. `vadd.vx` says "scalar register `rs1`" while its encoding declares `xs1` and its assembly is `vd, vs2, xs1, vm`. `c.sw` is the clearest, using both spellings for the same operand three words apart: "Stores a 32-bit value in register `xs2` ... It expands to `sw` `rs2, offset(xs1)`".

This is not a convention change. Both spellings are legitimate: across the 1,544 instruction files, `xs1` is a declared encoding variable in 878 and `rs1` in 116, and a file that declares `rs1` and says `rs1` is consistent and untouched. Only the mismatch is fixed.

Descriptions only, 19 lines. Every token was confirmed to occur the same number of times in the file as in its description before editing, so no encoding variable, `assembly` string or `operation()` body changes. All 18 still validate against `inst_schema.json`. `c.addi4spn` keeps its RVC prime and gains the prefix, `rd'` to `xd'`, matching `c.beqz`, `c.bnez`, `c.not` and `c.mul`.

The sweep found 33 files in this shape. Three are correct and left alone: `fround.q`, `froundnx.q` and `fround.s` name the `rs2` encoding field at bits 24-20, and the match strings agree. Eleven need a decision rather than a rename, and are enumerated in the issue, along with a separate defect in `vsub.vx` whose description states `vrsub.vx`'s semantics.

Closes #2458
