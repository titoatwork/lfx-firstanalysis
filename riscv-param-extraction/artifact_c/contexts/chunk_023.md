## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `fflags`
Floating-Point Accrued Exceptions | address 1 | privilege U

The accrued exception flags indicate the exception conditions that have arisen on any floating-point arithmetic
instruction since the field was last reset by software.

The base RISC-V ISA does not support generating a trap on the setting of a floating-point exception flag.

As allowed by the standard, we do not support traps on floating-point exceptions in the F
extension, but instead require ...

Fields:
- `NV` (bits 4), access RW-H
    Set by hardware when a floating point operation is invalid and stays set until explicitly
    cleared by software.
- `DZ` (bits 3), access RW-H
    Set by hardware when a floating point divide attempts to divide by zero and stays set until explicitly
    cleared by software.
- `OF` (bits 2), access RW-H
    Set by hardware when a floating point operation overflows and stays set until explicitly
    cleared by software.
- `UF` (bits 1), access RW-H
    Set by hardware when a floating point operation underflows and stays set until explicitly
    cleared by software.
- `NX`, access RW-H
    Set by hardware when a floating point operation is inexact and stays set until explicitly
    cleared by software.