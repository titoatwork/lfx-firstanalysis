## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

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

### CSR `menvcfg`
Machine Environment Configuration | address 778 | privilege M

Contains fields that control certain characteristics of the execution environment
for modes less privileged than M-mode.

The `menvcfg` CSR controls
certain characteristics of the execution environment for modes less
privileged than M.

If bit FIOM (Fence of I/O implies Memory) is set to one in `menvcfg`,
FENCE instructions executed in modes less privileged than M are modified
so the requirement ...

Fields:
- `STCE` (bits 63), access RW
    *STimecmp Enable*
    
    When set, `stimecmp` is operational.
    
    When clear, `stimecmp` access in a mode other than M-mode raises an `Illegal Instruction` trap.
    S-mode timer interrupts will not be generated when clear, and `mip` and `sip` revert to their prior behavior without `Sstc`.
- `PBMTE` (bits 62), access RW
    *Page Based Memory Type Enable*
    
    The PBMTE bit controls whether the Svpbmt extension is available for use in S-modeand G-stage
    address translation (i.e., for page tables pointed to by satp or hgatp). When PBMTE=1, Svpbmt is
    available for S-mode  and G-stage  address translation. When PBMTE=0, the implementation behaves
    as though Svpbmt were not implemented. If Svpbmt is not implemented, PBMTE is read-only zero.
    
    Furthermore, henvcfg.PBMTE is read-only zero if
    menvcfg.PBMTE is zero.
    
    After changing `menvcfg.PBMTE`, executing an `sfence.vma` instruction with _rs1_=_x0_ and
    _rs2_=_x0_ suffices ...
- `ADUE` (bits 61)
    If the Svadu extension is implemented, the ADUE bit controls whether hardware updating of
    PTE A/D bits is enabled for S-mode and G-stage address translations. When ADUE=1, hardware
    updating of PTE A/D bits is enabled during S-mode address translation, and the
    implementation behaves as though the Svade extension were not implemented for S-mode address
    translation.
    
    When the hypervisor extension is implemented, if ADUE=1, hardware updating of PTE A/D bits
    is enabled during G-stage address translation, and the implementation behaves as though the
    Svade extension were not implemented for G-stage ...
- `CBZE` (bits 7), access RW
    *Cache Block Zero instruction Enable*
    
    Enables the execution of the cache block zero instruction, `CBO.ZERO`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
- `CBCFE` (bits 6), access RW
    *Cache Block Clean and Flush instruction Enable*
    
    Enables the execution of the cache block clean instruction, `CBO.CLEAN`, and the
    cache block flush instruction, `CBO.FLUSH`,
    
    in S-mode
    
    in U-mode
    .
    
      * `0`: The instruction raises an illegal instruction or virtual instruction exception
      * `1`: The instruction is executed
- `CBIE` (bits 5-4), access RW-R
    *Cache Block Invalidate instruction Enable*
    
    Enables the execution of the cache block invalidate instruction, `CBO.INVAL`,
    
    in S-mode
    
    in U-mode
    .
    
      * `00`: The instruction raises an illegal instruction or virtual instruction exception
      * `01`: The instruction is executed and performs a flush operation
      * `10`: _Reserved_
      * `11`: The instruction is executed and performs an invalidate operation
- `SSE` (bits 3), access RW
    *Shadow Stack Enable*
    
    When the SSE field is set to 1 the Zicfiss extension isactivated in S-mode. When SSE
    field is 0, the following rules apply to privilege modes that are less than M:
    
      - 32-bit Zicfiss instructions will revert to their behavior as defined by Zimop.
    
      - 16-bit Zicfiss instructions will revert to their behavior as defined by Zcmop.
    
      - The pte.xwr=010b encoding in VS/S-stage page tables becomes reserved.
    
      - SSAMOSWAP.W/D raises an illegal-instruction exception.
    
    When menvcfg.SSE is 0, the henvcfg.SSE and senvcfg.SSE fields are read-only zero.
- `FIOM`, access RW
    *Fence of I/O implies Memory*
    
    When `menvcfg.FIOM` is set,
    FENCE instructions ordering I/O regions also implicitly order memory regions when executed
    in any mode less privileged than M-mode.
    
    [separator="!",%autowidth,float="center",align="center",cols="^,<",options="header"]
    !===
    !Instruction bit !Meaning when set
    !PI +
    PO
    !Predecessor device input and memory reads (PR implied) +
    Predecessor device output and memory writes (PW implied)
    !SI +
    SO
    !Successor device input and memory reads (SR implied) +
    Successor device output and memory writes (SW implied)
    !===
    
    Similarly, for modes less ...

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

### CSR `mcounteren`
Machine Counter Enable | address 774 | privilege M

The counter-enable `mcounteren` register is a 32-bit register that controls the availability
of the hardware performance-monitoring counters to

S-mode

U-mode

the next-lower privileged mode

.

The settings in this register only control accessibility. The act of reading or writing this
register does not affect the underlying counters, which continue to increment even when not
accessible.

When ...

Fields:
- `CY`
    When set, the `cycle` CSR (an alias of `mcycle`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.CY` is also set, `cycle` is further accessible to U-mode.
    
    When `hcounteren.CY` is also set, `cycle` is further accessible to VS-mode.
    
    When `hcounteren.CY` && `scounteren.CY` are both set, `cycle` is further accessible to VU-mode.
- `TM` (bits 1), access RO
    Placeholder for delegating `time` to less-privileged modes; however, since `time`
    is memory-mapped rather than a CSR, this field is always read-only zero.
- `IR` (bits 2)
    When set, the `instret` CSR (an alias of `minstret`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.IR` is also set, `instret` is further accessible to U-mode.
    
    When `hcounteren.IR` is also set, `instret` is further accessible to VS-mode.
    
    When `hcounteren.IR` && `scounteren.IR` are both set, `instret` is further accessible to VU-mode.
- `HPM3` (bits 3)
    When set, the `hpmcounter3` CSR (an alias of `mhpmcounter3`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM3` is also set, `hpmcounter3` is further accessible to U-mode.
    
    When `hcounteren.HPM3` is also set, `hpmcounter3` is further accessible to VS-mode.
    
    When `hcounteren.HPM3` && `scounteren.HPM3` are both set, `hpmcounter3` is further accessible to VU-mode.
- `HPM4` (bits 4)
    When set, the `hpmcounter4` CSR (an alias of `mhpmcounter4`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM4` is also set, `hpmcounter4` is further accessible to U-mode.
    
    When `hcounteren.HPM4` is also set, `hpmcounter4` is further accessible to VS-mode.
    
    When `hcounteren.HPM4` && `scounteren.HPM4` are both set, `hpmcounter4` is further accessible to VU-mode.
- `HPM5` (bits 5)
    When set, the `hpmcounter5` CSR (an alias of `mhpmcounter5`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM5` is also set, `hpmcounter5` is further accessible to U-mode.
    
    When `hcounteren.HPM5` is also set, `hpmcounter5` is further accessible to VS-mode.
    
    When `hcounteren.HPM5` && `scounteren.HPM5` are both set, `hpmcounter5` is further accessible to VU-mode.
- `HPM6` (bits 6)
    When set, the `hpmcounter6` CSR (an alias of `mhpmcounter6`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM6` is also set, `hpmcounter6` is further accessible to U-mode.
    
    When `hcounteren.HPM6` is also set, `hpmcounter6` is further accessible to VS-mode.
    
    When `hcounteren.HPM6` && `scounteren.HPM6` are both set, `hpmcounter6` is further accessible to VU-mode.
- `HPM7` (bits 7)
    When set, the `hpmcounter7` CSR (an alias of `mhpmcounter7`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM7` is also set, `hpmcounter7` is further accessible to U-mode.
    
    When `hcounteren.HPM7` is also set, `hpmcounter7` is further accessible to VS-mode.
    
    When `hcounteren.HPM7` && `scounteren.HPM7` are both set, `hpmcounter7` is further accessible to VU-mode.
- `HPM8` (bits 8)
    When set, the `hpmcounter8` CSR (an alias of `mhpmcounter8`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM8` is also set, `hpmcounter8` is further accessible to U-mode.
    
    When `hcounteren.HPM8` is also set, `hpmcounter8` is further accessible to VS-mode.
    
    When `hcounteren.HPM8` && `scounteren.HPM8` are both set, `hpmcounter8` is further accessible to VU-mode.
- `HPM9` (bits 9)
    When set, the `hpmcounter9` CSR (an alias of `mhpmcounter9`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM9` is also set, `hpmcounter9` is further accessible to U-mode.
    
    When `hcounteren.HPM9` is also set, `hpmcounter9` is further accessible to VS-mode.
    
    When `hcounteren.HPM9` && `scounteren.HPM9` are both set, `hpmcounter9` is further accessible to VU-mode.
- `HPM10` (bits 10)
    When set, the `hpmcounter10` CSR (an alias of `mhpmcounter10`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM10` is also set, `hpmcounter10` is further accessible to U-mode.
    
    When `hcounteren.HPM10` is also set, `hpmcounter10` is further accessible to VS-mode.
    
    When `hcounteren.HPM10` && `scounteren.HPM10` are both set, `hpmcounter10` is further accessible to VU-mode.
- `HPM11` (bits 11)
    When set, the `hpmcounter11` CSR (an alias of `mhpmcounter11`) is accessible to
    
    S-mode.
    
    U-mode.
    
    When `scounteren.HPM11` is also set, `hpmcounter11` is further accessible to U-mode.
    
    When `hcounteren.HPM11` is also set, `hpmcounter11` is further accessible to VS-mode.
    
    When `hcounteren.HPM11` && `scounteren.HPM11` are both set, `hpmcounter11` is further accessible to VU-mode.

### CSR `scountovf`
Supervisor Count Overflow | address 3488 | privilege S

A 32-bit read-only register that contains shadow copies of the OF bits in the 29 `mhpmevent` CSRs
(`mhpmevent3` - `mhpmevent31`) — where `scountovf` bit X corresponds to `mhpmeventX`.

This register enables supervisor-level overflow interrupt handler
software to quickly and easily determine which counter(s) have overflowed
without needing to make an execution environment call up to M-mode.

Read ...

Fields:
- `OF3` (bits 3)
    [when="PARAM_018[3] == true"]
    Shadow copy of mhpmevent3 overflow (OF) bit.
    
    [when="PARAM_018[3] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF4` (bits 4)
    [when="PARAM_018[4] == true"]
    Shadow copy of mhpmevent4 overflow (OF) bit.
    
    [when="PARAM_018[4] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF5` (bits 5)
    [when="PARAM_018[5] == true"]
    Shadow copy of mhpmevent5 overflow (OF) bit.
    
    [when="PARAM_018[5] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF6` (bits 6)
    [when="PARAM_018[6] == true"]
    Shadow copy of mhpmevent6 overflow (OF) bit.
    
    [when="PARAM_018[6] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF7` (bits 7)
    [when="PARAM_018[7] == true"]
    Shadow copy of mhpmevent7 overflow (OF) bit.
    
    [when="PARAM_018[7] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF8` (bits 8)
    [when="PARAM_018[8] == true"]
    Shadow copy of mhpmevent8 overflow (OF) bit.
    
    [when="PARAM_018[8] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF9` (bits 9)
    [when="PARAM_018[9] == true"]
    Shadow copy of mhpmevent9 overflow (OF) bit.
    
    [when="PARAM_018[9] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF10` (bits 10)
    [when="PARAM_018[10] == true"]
    Shadow copy of mhpmevent10 overflow (OF) bit.
    
    [when="PARAM_018[10] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF11` (bits 11)
    [when="PARAM_018[11] == true"]
    Shadow copy of mhpmevent11 overflow (OF) bit.
    
    [when="PARAM_018[11] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF12` (bits 12)
    [when="PARAM_018[12] == true"]
    Shadow copy of mhpmevent12 overflow (OF) bit.
    
    [when="PARAM_018[12] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF13` (bits 13)
    [when="PARAM_018[13] == true"]
    Shadow copy of mhpmevent13 overflow (OF) bit.
    
    [when="PARAM_018[13] == false"]
    This field is read-only zero because the counter is not enabled.
- `OF14` (bits 14)
    [when="PARAM_018[14] == true"]
    Shadow copy of mhpmevent14 overflow (OF) bit.
    
    [when="PARAM_018[14] == false"]
    This field is read-only zero because the counter is not enabled.

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