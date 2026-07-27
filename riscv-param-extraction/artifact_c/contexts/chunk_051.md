## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `mstateen0`
Machine State Enable 0 Register | address 780 | privilege M

Each bit of a `stateen` CSR controls less-privileged access to an extension’s state,
or an extension that was not deemed "worthy" of a full XS field in `sstatus` like the
FS and VS fields for the F and V extensions.

The number of registers provided at each level is four because it is believed that
4 * 64 = 256 bits for machine and hypervisor levels, and 4 * 32 = 128 bits for
supervisor level, ...

Fields:
- `SE0` (bits 63), access RW
    The SE0 bit in `mstateen0` controls access to the `hstateen0`, `hstateen0h`, and the `sstateen0` CSRs.
- `ENVCFG` (bits 62), access RW
    The ENVCFG bit in `mstateen0` controls access to the `henvcfg`, `henvcfgh`, and the `senvcfg` CSRs.
- `CSRIND` (bits 60), access RW
    The CSRIND bit in `mstateen0` controls access to the `siselect`, `sireg*`, `vsiselect`, and the `vsireg*`
    CSRs provided by the Sscsrind extensions.
- `AIA` (bits 59), access RW
    The AIA bit in `mstateen0` controls access to all state introduced by the Ssaia extension and is not
    controlled by either the CSRIND or the IMSIC bits.
- `IMSIC` (bits 58), access RW
    The IMSIC bit in `mstateen0` controls access to the IMSIC state, including CSRs `stopei` and `vstopei`,
    provided by the Ssaia extension.
- `CONTEXT` (bits 57), access RW
    The CONTEXT bit in `mstateen0` controls access to the `scontext` and `hcontext` CSRs provided by the
    Sdtrig extension.
- `P1P13` (bits 56), access RW
    The P1P13 bit in `mstateen0` controls access to the `hedelegh` introduced by Privileged Specification
    Version 1.13.
- `SRMCFG` (bits 55), access RW
    The SRMCFG bit in `mstateen0` controls access to the `srmcfg`` CSR introduced by the Ssqosid Chapter 18
    extension.
- `CTR` (bits 54), access RW
    When Smstateen is implemented, the `mstateen0.CTR` bit controls access to CTR register state from
    privilege modes less privileged than M-mode.
- `JVT` (bits 2), access RW
    The JVT bit controls access to the `jvt` CSR provided by the Zcmt extension.
- `FCSR` (bits 1), access RW
    The FCSR bit controls access to `fcsr` for the case when floating-point instructions
    operate on `x` registers instead of `f` registers as specified by the Zfinx and related
    extensions (Zdinx, etc.). Whenever `misa.F` = 1, FCSR bit of `mstateen0` is read-only
    zero (and hence read-only zero in `hstateen0` and `sstateen0` too). For convenience,
    when the `stateen` CSRs are implemented and `misa.F` = 0, then if the FCSR bit of a
    controlling `stateen0` CSR is zero, all floating-point instructions cause an illegal
    instruction trap (or virtual instruction trap, if relevant), as though they all ...
- `C`, access RW
    The C bit controls access to any and all custom state. The C bit of these registers is
    not custom state itself; it is a standard field of a standard CSR, either `mstateen0`,
    `hstateen0`, or `sstateen0`.

### CSR `hstateen0`
Hypervisor State Enable 0 Register | address 1548 | privilege S

Each bit of a `stateen` CSR controls less-privileged access to an extension’s state,
for an extension that was not deemed "worthy" of a full XS field in `sstatus` like the
FS and VS fields for the F and V extensions.

The number of registers provided at each level is four because it is believed that
4 * 64 = 256 bits for machine and hypervisor levels, and 4 * 32 = 128 bits for
supervisor level, ...

Fields:
- `SE0` (bits 63), access RW
    The SE0 bit in `hstateen0` controls access to the `sstateen0` CSR.
- `ENVCFG` (bits 62), access RW
    The ENVCFG bit in `hstateen0` controls access to the `senvcfg` CSRs.
- `CSRIND` (bits 60), access RW
    The CSRIND bit in `hstateen0` controls access to the `siselect` and the
    `sireg*`, (really `vsiselect` and `vsireg*`) CSRs provided by the Sscsrind
    extensions.
- `AIA` (bits 59), access RW
    The AIA bit in `hstateen0` controls access to all state introduced by
    the Ssaia extension and is not controlled by either the CSRIND or the
    IMSIC bits of `hstateen0`.
- `IMSIC` (bits 58), access RW
    The IMSIC bit in `hstateen0` controls access to the guest IMSIC state,
    including CSRs `stopei` (really `vstopei`), provided by the Ssaia extension.
    
    Setting the IMSIC bit in `hstateen0` to zero prevents a virtual machine
    from accessing the hart’s IMSIC the same as setting `hstatus.`VGEIN = 0.
- `CONTEXT` (bits 57), access RW
    The CONTEXT bit in `hstateen0` controls access to the `scontext` CSR provided
    by the Sdtrig extension.
- `CTR` (bits 54), access RW
    If the H extension is implemented and `mstateen0.CTR=1`, the `hstateen0.CTR` bit controls access to
    supervisor CTR state when V=1. This state includes `sctrctl` (really `vsctrctl`), `sctrstatus`, and `sireg*`
    (really `vsireg*`) when `siselect` (really `vsiselect`) is in 0x200..0x2FF. `hstateen0.CTR` is read-only 0 when
    `mstateen0.CTR=0`.
- `JVT` (bits 2), access RW
    The JVT bit controls access to the `jvt` CSR provided by the Zcmt extension.
- `FCSR` (bits 1), access RW
    The FCSR bit controls access to `fcsr` for the case when floating-point instructions
    operate on `x` registers instead of `f` registers as specified by the Zfinx and related
    extensions (Zdinx, etc.). Whenever `misa.F` = 1, FCSR bit of `mstateen0` is read-only
    zero (and hence read-only zero in `hstateen0` and `sstateen0` too). For convenience,
    when the `stateen` CSRs are implemented and `misa.F` = 0, then if the FCSR bit of a
    controlling `stateen0` CSR is zero, all floating-point instructions cause an illegal
    instruction trap (or virtual instruction trap, if relevant), as though they all ...
- `C`, access RW
    The C bit controls access to any and all custom state. The C bit of these registers is
    not custom state itself; it is a standard field of a standard CSR, either `mstateen0`,
    `hstateen0`, or `sstateen0`.

### CSR `sstateen0`
Supervisor State Enable 0 Register | address 268 | privilege S

Each bit of a `stateen` CSR controls less-privileged access to an extension’s state,
for an extension that was not deemed "worthy" of a full XS field in `sstatus` like the
FS and VS fields for the F and V extensions.

The number of registers provided at each level is four because it is believed that
4 * 64 = 256 bits for machine and hypervisor levels, and 4 * 32 = 128 bits for
supervisor level, ...

Fields:
- `JVT` (bits 2), access RW
    The JVT bit controls access to the `jvt` CSR provided by the Zcmt extension.
- `FCSR` (bits 1), access RW
    The FCSR bit controls access to `fcsr` for the case when floating-point instructions
    operate on `x` registers instead of `f` registers as specified by the Zfinx and related
    extensions (Zdinx, etc.). Whenever `misa.F` = 1, FCSR bit of `mstateen0` is read-only
    zero (and hence read-only zero in `hstateen0` and `sstateen0` too). For convenience,
    when the `stateen` CSRs are implemented and `misa.F` = 0, then if the FCSR bit of a
    controlling `stateen0` CSR is zero, all floating-point instructions cause an illegal
    instruction trap (or virtual instruction trap, if relevant), as though they all ...
- `C`, access RW
    The C bit controls access to any and all custom state. The C bit of these registers is
    not custom state itself; it is a standard field of a standard CSR, either `mstateen0`,
    `hstateen0`, or `sstateen0`.

### CSR `sstatus`
Supervisor Status | address 256 | privilege S

The sstatus register tracks and controls the hart's current operating state.

All fields in sstatus are aliases of the same field in mstatus.

Fields:
- `SD` (bits 63), access RO-H
    *State Dirty*
    
    Alias of `mstatus.SD`.
- `UXL` (bits 33-32), access RO
    *U-mode XLEN*
    
    Alias of `mstatus.UXL`.
- `MXR` (bits 19), access RW
    *Make eXecutable Readable*
    
    Alias of `mstatus.MXR`.
- `SUM` (bits 18), access RW
    *permit Supervisor Memory Access*
    
    Alias of `mstatus.SUM`.
- `XS` (bits 16-15), access RO
    Custom (X) extension context Status.
    
    Alias of `mstatus.XS`.
- `FS` (bits 14-13), access RW-H
    Floating point context status.
    
    Alias of `mstatus.FS`.
- `VS` (bits 10-9), access RW-H
    Vector context status.
    
    Alias of `mstatus.VS`.
- `SPP` (bits 8), access RW-H
    *S-mode Previous Privilege*
    
    Alias of `mstatus.SPP`.
- `UBE` (bits 6), access RO
    *U-mode Big Endian*
    
    Alias of `mstatus.UBE`.
- `SPIE` (bits 5), access RW-H
    *S-mode Previous Interrupt Enable*
    
    Alias of `mstatus.SPIE`.
- `SIE` (bits 1), access RW-H
    *S-mode Interrupt Enable*
    
    Alias of `mstatus.SIE`.

### CSR `sireg`
Supervisor Indirect Register Alias | address 337 | privilege S

Access to `sireg` from M-mode or S-mode while `siselect` holds a number in a
standard-defined and implemented range results in specific behavior that, for each combination of
`siselect` and `sireg`, is defined by the extension to which the `siselect` value is allocated.

Ordinarily, `sireg` will access register state, access read-only 0 state, or, unless
executing in a virtual machine (covered in ...

Fields:
- `VALUE` (bits 63-0), access RW
    The data read from or written to the register selected by the current `siselect` value.

### CSR `siselect`
Supervisor Indirect Register Select | address 336 | privilege S

The `siselect` register will support the value range 0..0xFFF at a minimum. A future extension may
define a value range outside of this minimum range. Only if such an extension is implemented will
`siselect` be required to support larger values.

Requiring a range of 0-0xFFF for `siselect`, even though most or all of the space may be reserved or
inaccessible, permits M-mode to emulate indirectly ...

Fields:
- `VALUE` (bits 63-0), access RW
    Value ranges are allocated to dependent extensions, which specify the
    register state accessible via each `sireg*` register, for each `siselect` value.

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

### CSR `hstateen0h`
Upper 32 bits of Hypervisor State Enable 0 Register | address 1564 | privilege S

For RV64 harts, the Smstateen/Ssstateen extension adds four new 64-bit CSRs at machine level: `mstateen0` (Machine State Enable 0),
`mstateen1`, `mstateen2`, and `mstateen3`. If supervisor mode is implemented, another four CSRs are defined at
supervisor level: `sstateen0`, `sstateen1`, `sstateen2`, and `sstateen3`. And if the hypervisor extension is implemented,
another set of CSRs is added: ...

Fields:
- `SE0` (bits 31), access RW
    The SE0 bit in `hstateen0h` controls access to the `sstateen0` CSR.
- `ENVCFG` (bits 30), access RW
    The ENVCFG bit in `hstateen0h` controls access to the `senvcfg` CSRs.
- `CSRIND` (bits 28), access RW
    The CSRIND bit in `hstateen0h` controls access to the `siselect` and the
    `sireg*`, (really `vsiselect` and `vsireg*`) CSRs provided by the Sscsrind
    extensions.
- `AIA` (bits 27), access RW
    The AIA bit in `hstateen0h` controls access to all state introduced by
    the Ssaia extension and is not controlled by either the CSRIND or the
    IMSIC bits of `hstateen0`.
- `IMSIC` (bits 26), access RW
    The IMSIC bit in `hstateen0h` controls access to the guest IMSIC state,
    including CSRs `stopei` (really `vstopei`), provided by the Ssaia extension.
    
    Setting the IMSIC bit in `hstateen0h` to zero prevents a virtual machine
    from accessing the hart’s IMSIC the same as setting `hstatus.`VGEIN = 0.
- `CONTEXT` (bits 25), access RW
    The CONTEXT bit in `hstateen0h` controls access to the `scontext` CSR provided
    by the Sdtrig extension.
- `CTR` (bits 22), access RW
    If the H extension is implemented and `mstateen0.CTR=1`, the `hstateen0.CTR` bit controls access to
    supervisor CTR state when V=1. This state includes `sctrctl` (really `vsctrctl`), `sctrstatus`, and `sireg*`
    (really `vsireg*`) when `siselect` (really `vsiselect`) is in 0x200..0x2FF. `hstateen0.CTR` is read-only 0 when
    `mstateen0.CTR=0`.