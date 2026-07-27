## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `fcsr`
Floating-point control and status register (`frm` + `fflags`) | address 3 | privilege U

The floating-point control and status register, `fcsr`, is a RISC-V
control and status register (CSR). It is a 32-bit read/write register
that selects the dynamic rounding mode for floating-point arithmetic
operations and holds the accrued exception flags, as shown in <<fcsr>>.

[[fcsr, Floating-Point Control and Status Register]]
.Floating-point control and status ...

Fields:
- `FRM` (bits 7-5), access RW-H
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
    !100 !RMM !Round to Nearest, ties to Max Magnitude
    !101 ! !_Reserved for future use._
    !110 ! !_Reserved for future use._
    !111 !DYN !In instruction's _rm_ field, selects dynamic rounding mode; In Rounding Mode register, ...
- `NV` (bits 4), access RW-H
    *Invalid Operation*
    
    Cumulative error flag for floating point operations.
    
    Set by hardware when a floating point operation is invalid and stays set until explicitly
    cleared by software.
- `DZ` (bits 3), access RW-H
    *Divide by zero*
    
    Cumulative error flag for floating point operations.
    
    Set by hardware when a floating point divide attempts to divide by zero and stays set until explicitly
    cleared by software.
- `OF` (bits 2), access RW-H
    *Overflow*
    
    Cumulative error flag for floating point operations.
    
    Set by hardware when a floating point operation overflows and stays set until explicitly
    cleared by software.
- `UF` (bits 1), access RW-H
    *Underflow*
    
    Cumulative error flag for floating point operations.
    
    Set by hardware when a floating point operation underflows and stays set until explicitly
    cleared by software.
- `NX`, access RW-H
    *Inexact*
    
    Cumulative error flag for floating point operations.
    
    Set by hardware when a floating point operation is inexact and stays set until explicitly
    cleared by software.