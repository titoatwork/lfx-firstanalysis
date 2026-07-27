## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `cycle`
Cycle counter for RDCYCLE Instruction | address 3072 | privilege U

Alias for M-mode CSR `mcycle`.

Privilege mode access is controlled with `mcounteren.CY`, `scounteren.CY`, and `hcounteren.CY` as follows:

[%autowidth,cols="1,1,1,1,1,1,1",separator="!"]
!===
.2+h![.rotate]#`mcounteren.CY`# .2+h! [.rotate]#`scounteren.CY`# .2+h! [.rotate]#`hcounteren.CY`#
4+^.>h! `cycle` behavior
.^h! S-mode .^h! U-mode .^h! VS-mode .^h! VU-mode

! 0 ! - ! - ! ...

Fields:
- `COUNT` (bits 63-0), access RO-H
    Alias of `mcycle.COUNT`.

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

### CSR `instret`
Instructions retired counter for RDINSTRET Instruction | address 3074 | privilege U

Alias for M-mode CSR `minstret`.

Privilege mode access is controlled with `mcounteren.IR`, `scounteren.IR`, and `hcounteren.IR` as follows:

[%autowidth,cols="1,1,1,1,1,1,1",separator="!"]
!===
.2+h![.rotate]#`mcounteren.IR`# .2+h! [.rotate]#`scounteren.IR`# .2+h! [.rotate]#`hcounteren.IR`#
4+^.>h! `instret` behavior
.^h! S-mode .^h! U-mode .^h! VS-mode .^h! VU-mode

! 0 ! - ! - ! ...

Fields:
- `COUNT` (bits 63-0), access RO-H
    Alias of `minstret.COUNT`.

### CSR `time`
Timer for RDTIME Instruction | address 3073 | privilege U

[when,"PARAM_146 == false"]
This CSR does not exist, and access will cause an IllegalInstruction exception.

[when,"PARAM_146 == true"]
--
Shadow of the memory-mapped M-mode CSR `mtime`.

Privilege mode access is controlled with `mcounteren.TM`, `scounteren.TM`, and `hcounteren.TM` as ...

Fields:
- `COUNT` (bits 63-0), access RO-H
    Reports the current wall-clock time from the timer device.
    
    Alias of the `mtime` memory-mapped CSR.

### CSR `cycleh`
High-half cycle counter for RDCYCLE Instruction | address 3200 | privilege U

Alias for M-mode CSR `mcycleh`.

Privilege mode access is controlled with `mcounteren.CY`, `scounteren.CY`, and `hcounteren.CY` as follows:

[%autowidth,cols="1,1,1,1,1,1,1",separator="!"]
!===
.2+h![.rotate]#`mcounteren.CY`# .2+h! [.rotate]#`scounteren.CY`# .2+h! [.rotate]#`hcounteren.CY`#
4+^.>h! `cycle` behavior
.^h! S-mode .^h! U-mode .^h! VS-mode .^h! VU-mode

! 0 ! - ! - ! ...

Fields:
- `COUNT` (bits 31-0), access RO-H
    Alias of `mcycleh.COUNT`.

### CSR `instreth`
Instructions retired counter, high bits | address 3202 | privilege U

Alias for high bits of M-mode CSR `minstret`[63:32].

Privilege mode access is controlled with `mcounteren.IR`, `scounteren.IR`, and `hcounteren.IR` as follows:

[%autowidth,cols="1,1,1,1,1,1,1",separator="!"]
!===
.2+h![.rotate]#`mcounteren.IR`# .2+h! [.rotate]#`scounteren.IR`# .2+h! [.rotate]#`hcounteren.IR`#
4+^.>h! `instret` behavior
.^h! S-mode .^h! U-mode .^h! VS-mode .^h! VU-mode

! 0 ! - ...

Fields:
- `COUNT` (bits 31-0), access RO-H
    Alias of `minstret.COUNT`[63:32].

### CSR `timeh`
High-half timer for RDTIME Instruction | address 3201 | privilege U

[when,"PARAM_146 == false"]
This CSR does not exist, and access will cause an IllegalInstruction exception.

[when,"PARAM_146 == true"]
--
Shadow of the memory-mapped M-mode CSR `mtimeh`.

Privilege mode access is controlled with `mcounteren.TM`, `scounteren.TM`, and `hcounteren.TM` as ...

Fields:
- `COUNT` (bits 31-0), access RO-H
    Reports the most significant 32 bits of the current wall-clock time from the timer device.