## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `frm`
Floating-Point Dynamic Rounding Mode | address 2 | privilege U

Rounding modes are encoded as follows:

[[rm]]
.Rounding mode encoding.
[%autowidth,float="center",align="center",cols="^,^,<",options="header"]
!===
!Rounding Mode |Mnemonic |Meaning
!000 !RNE !Round to Nearest, ties to Even
!001 !RTZ !Round towards Zero
!010 !RDN !Round Down (towards latexmath:[$-\infty$])
!011 !RUP !Round Up (towards latexmath:[$+\infty$])
!100 !RMM !Round to Nearest, ties to ...

Fields:
- `ROUNDINGMODE` (bits 2-0), access RW-H
    Rounding mode data.