## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `mctrctl`
Machine Control Transfer Records Control Register | address 846 | privilege M

The `mctrctl` register enables and configures the Control Transfer Records capability in M mode.

Fields:
- `U`, access RW
    Enable transfer recording in the User mode.
- `S` (bits 1), access RW
    Enable transfer recording in the Supervisor mode.
- `M` (bits 2), access RW
    Enable transfer recording in the Machine mode.
- `RASEMU` (bits 7), access RW
    When set, it enables RAS (Return Address Stack) Emulation Mode.
- `STE` (bits 8), access RW
    Enables recording of traps to S-mode when S=0.
- `MTE` (bits 9), access RW
    Enables recording of traps to M-mode when M=0.
- `BPFRZ` (bits 11), access RW
    Set `sctrstatus.FROZEN` on a breakpoint exception that traps to M or S mode.
- `LCOFIFRZ` (bits 12), access RW
    Set `sctrstatus.FROZEN` on local-counter-overflow interrupt (LCOFI) that traps
    to M or S mode.
- `EXCINH` (bits 33), access RW
    When set, it inhibits recording of exceptions.
- `INTRINH` (bits 34), access RW
    When set, it inhibits recording of interrupts.
- `TRETINH` (bits 35), access RW
    When set, it inhibits recording of trap returns.
- `NTBREN` (bits 36), access RW
    When set, it enables recording of not-taken branches.

### CSR `sctrctl`
Supervisor Control Transfer Records Control Register | address 334 | privilege S

The `sctrctl` register enables and configures the Control Transfer Records capability in S mode.

Fields:
- `U`, access RW
    Enable transfer recording in the User mode.
- `S` (bits 1), access RW
    Enable transfer recording in the Supervisor mode.
- `RASEMU` (bits 7), access RW
    When set, it enables RAS (Return Address Stack) Emulation Mode.
- `STE` (bits 8), access RW
    Enables recording of traps to S-mode when S=0.
- `BPFRZ` (bits 11), access RW
    Set `sctrstatus.FROZEN` on a breakpoint exception that traps to M or S mode.
- `LCOFIFRZ` (bits 12), access RW
    Set `sctrstatus.FROZEN` on local-counter-overflow interrupt (LCOFI) that traps
    to M or S mode.
- `EXCINH` (bits 33), access RW
    When set, it inhibits recording of exceptions.
- `INTRINH` (bits 34), access RW
    When set, it inhibits recording of interrupts.
- `TRETINH` (bits 35), access RW
    When set, it inhibits recording of trap returns.
- `NTBREN` (bits 36), access RW
    When set, it enables recording of not-taken branches.
- `TKBRINH` (bits 37), access RW
    When set, it inhibits recording of taken branches.
- `INDCALLINH` (bits 40), access RW
    When set, it inhibits recording of indirect calls.

### CSR `vsctrctl`
Virtual Supervisor Control Transfer Records Control Register | address 590 | privilege VS

The `vsctrctl` register is a VS-mode's version of supervisor register `sctrctl` that
configures the Control Transfer Records capability. When `V=1`, vsctrctl substitutes
for the usual `sctrctl`, so instructions that normally read or modify `sctrctl` actually
access `vsctrctl` instead.

Fields:
- `U`, access RW
    Enable transfer recording in the VU mode.
- `S` (bits 1), access RW
    Enable transfer recording in the VS mode.
- `RASEMU` (bits 7), access RW
    When set, it enables RAS (Return Address Stack) Emulation Mode.
- `STE` (bits 8), access RW
    Enables recording of traps to VS-mode when S=0.
- `BPFRZ` (bits 11), access RW
    Set `sctrstatus.FROZEN` on a breakpoint exception that traps to VS mode.
- `LCOFIFRZ` (bits 12), access RW
    Set `sctrstatus.FROZEN` on local-counter-overflow interrupt (LCOFI) that traps to VS mode.
- `EXCINH` (bits 33), access RW
    When set, it inhibits recording of exceptions.
- `INTRINH` (bits 34), access RW
    When set, it inhibits recording of interrupts.
- `TRETINH` (bits 35), access RW
    When set, it inhibits recording of trap returns.
- `NTBREN` (bits 36), access RW
    When set, it enables recording of not-taken branches.
- `TKBRINH` (bits 37), access RW
    When set, it inhibits recording of taken branches.
- `INDCALLINH` (bits 40), access RW
    When set, it inhibits recording of indirect calls.

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