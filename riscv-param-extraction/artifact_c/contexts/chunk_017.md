## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

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

### CSR `vsiselect`
Virtual Supervisor Indirect Register Select | address 592 | privilege VS

The `vsiselect` register will support the value range 0..0xFFF at a minimum.
A future extension may define a value range outside of this minimum range.
Only if such an extension is implemented will `vsiselect` be required to support larger values.

Requiring a range of 0-0xFFF for `vsiselect`, even though most or all of the space may be reserved
or inaccessible, permits a hypervisor to emulate ...

Fields:
- `VALUE` (bits 63-0), access RW
    The index value selecting the register accessed through the `vsireg*` alias registers.

### CSR `miselect`
Machine Indirect Register Select | address 848 | privilege M

The CSRs listed in the table above provide a window for accessing register state indirectly.
The value of `miselect` determines which register is accessed upon read or write of each of
the machine indirect alias CSRs (`mireg*`). `miselect` value ranges are allocated to dependent
extensions, which specify the register state accessible via each `miregi` register, for each
`miselect` value. ...

Fields:
- `VALUE` (bits 63-0), access RW
    Selects which indirect register is accessed via `mireg*`.

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

### CSR `vsireg`
Virtual Supervisor Indirect Register Alias | address 593 | privilege VS

The `vsireg` CSR is one of several alias registers used to indirectly access
virtual supervisor-level CSRs in VS-mode or VU-mode.

The register addressed by `vsireg` is selected by the current value of the `vsiselect` CSR.

The alias mechanism allows indirect CSR access, which helps in virtualization and future extensibility.

A virtual instruction exception is raised for attempts from VS-mode or ...

Fields:
- `VALUE` (bits 63-0), access RW
    The data read from or written to the register selected by the current
    value of the `vsiselect` CSR.

### CSR `mireg`
Machine Indirect Register Alias | address 849 | privilege M

The mireg machine indirect alias CSR is used to access another CSR's state
indirectly upon a read or write, as determined by the value of miselect.

The behavior upon accessing mireg from M-mode, while miselect holds a value
that is not implemented, is UNSPECIFIED.

It is expected that implementations will typically raise an illegal instruction exception for
such accesses, so that, for example, ...

Fields:
- `VALUE` (bits 63-0), access RW
    Register state of the CSR selected by the current `miselect` value

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