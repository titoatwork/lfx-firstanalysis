## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `vtype`
Vector Type | address 3105 | privilege U

Provides the default type used to interpret the contents of the vector register file.

Fields:
- `VILL` (bits 63), access RO-H
    The vill bit is used to encode that a previous vset{i}vl{i} instruction attempted to write an
    unsupported value to vtype.
    
    [NOTE]
    The vill bit is held in bit XLEN-1 of the CSR to support checking for illegal values with a
    branch on the sign bit.
    
    If the vill bit is set, then any attempt to execute a vector instruction that depends upon vtype will
    raise an illegal-instruction exception.
    
    When the vill bit is set, the other XLEN-1 bits in vtype shall be zero.
    
    It is recommended that at reset, vill is set.
- `VMA` (bits 7), access RO-H
    Vector mask agnostic bit. Modifies the behavior of destination inactive masked-off elements during the
    execution of vector instructions.
    
    A value of 0 means inactive elements are undisturbed, meaning the corresponding set of destination elements
    in a vector register group retain the value they previously held.
    
    A value of 1 means inactive elements are agnostic, meaning the corresponding set of destination elements
    in any vector destination operand can either retain the value they previously held, or are overwritten with 1s.
    Within a single vector instruction, each destination element can be ...
- `VTA` (bits 6), access RO-H
    Vector tail agnostic bit. Modifies the bahavior of destination tail elements during the execution of vector
    instructions.
    
    A value of 0 means tail elements are undisturbed, meaning the corresponding set of destination elements
    in a vector register group retain the value they previously held.
    
    A value of 1 means tail elements are agnostic, meaning the corresponding set of destination elements
    in any vector destination operand can either retain the value they previously held, or are overwritten with 1s.
    Within a single vector instruction, each destination element can be either left undisturbed ...
- `VSEW` (bits 5-3), access RO-H
    The value in vsew sets the dynamic selected element width (SEW).
    
    [separator="!"]
    !===
    ! vsew[2:0] ! SEW ! Elements per vector register
    ! 000 ! 8 ! 16
    ! 001 ! 16 ! 8
    ! 010 ! 32 ! 4
    ! 011 ! 64 ! 2
    ! 1XX ! Reserved ! Reserved
    !===
    
    It is recommended that at reset, vill is set, and the remaining bits in vtype are zero.
- `VLMUL` (bits 2-0), access RO-H
    Vector register group multiplier.
    
    Multiple vector registers can be grouped together, so that a single vector instruction can operate on
    multiple vector registers. The term vector register group is used herein to refer to one or more vector
    registers used as a single operand to a vector instruction. Vector register groups can be used to provide
    greater execution efficiency for longer application vectors, but the main reason for their inclusion is to
    allow double-width or larger elements to be operated on with the same vector length as single-width
    elements. The vector length multiplier, LMUL, ...

### CSR `vstart`
Vector Start Index | address 8 | privilege U

Specifies the index of the first element to be executed by a vector instruction.

Fields:
- `VALUE` (bits 63-0), access RW-RH
    Normally, vstart is only written by hardware on a trap on a vector instruction, with the vstart value
    representing the element on which the trap was taken (either a synchronous exception or an
    asynchronous interrupt), and at which execution should resume after a resumable trap is handled.
    All vector instructions are defined to begin execution with the element number given in the vstart
    CSR, leaving earlier elements in the destination vector undisturbed, and to reset the vstart CSR to
    zero at the end of execution.
    
    [NOTE]
    All vector instructions, including vset{i}vl{i}, reset the vstart CSR to ...

### CSR `mstatus`
Machine Status | address 768 | privilege M

The mstatus register tracks and controls the hart's current operating state.

Fields:
- `SD` (bits 63)
    Read-only bit that summarizes whether either the FS, XS, or VS
    fields signal the presence of some dirty state.
- `MDT` (bits 42), access RW-H
    Written to 1 when entering M-mode from an exception/interrupt.
    When returning via an MRET instruction, the bit is written to 0.
    On reset in set to 1, and software should write it to 0 when boot sequence is done.
    When mstatus.MDT=1, direct write by CSR instruction cannot set mstatus.MIE to 1, if not written together.
- `MPV` (bits 39), access RW-H
    Written with the prior virtualization mode when entering M-mode from an exception/interrupt.
    When returning via an MRET instruction, the virtualization mode becomes the value of MPV unless MPP=3, in which case the virtualization mode is always 0.
    Can also be written by software.
- `GVA` (bits 38), access RW-H
    When a trap is taken and a guest virtual address is written into mtval, GVA is set.
    When a trap is taken and a guest virtual address is written into mtval, GVA is cleared.
- `MBE` (bits 37)
    Controls the endianness of data M-mode (0 = little, 1 = big).
    Instructions are always little endian, regardless of the data setting.
    
    [when,"PARAM_075 == little"]
    Since the CPU does not support big endian, this is hardwired to 0.
    
    [when,"PARAM_075 == big"]
    Since the CPU does not support little endian, this is hardwired to 1.
- `SBE` (bits 36)
    Controls the endianness of S-mode (0 = little, 1 = big).
    Instructions are always little endian, regardless of the data setting.
    
    [when,"PARAM_145 == little"]
    Since the CPU does not support big endian, this is hardwired to 0.
    
    [when,"PARAM_145 == big"]
    Since the CPU does not support little endian, this is hardwired to 1.
- `SXL` (bits 35-34)
    Sets the effective XLEN for S-mode (0 = 32-bit, 1 = 64-bit, 2 = 128-bit [reserved]).
    
    [when,"PARAM_144==32"]
    Since the CPU only supports PARAM_144==32, this is hardwired to 1.
    
    [when,"PARAM_144==64"]
    Since the CPU only supports PARAM_144==64, this is hardwired to 2.
    
    [when,"PARAM_144=3264"]
    --
    It is not valid to have PARAM_144 less than PARAM_173.
    
    It is UNDEFINED_LEGAL what will happen if a software sets `mstatus.SXL` to be greater than `mstatus.UXL`.
    
    It is UNDEFINED_LEGAL to set the MSB of SXL.
    --
- `UXL` (bits 33-32)
    U-mode XLEN.
    
    Sets the effective XLEN for U-mode (1 = 32-bit, 2 = 64-bit, 3 = 128-bit [reserved]).
    
    [when,"PARAM_173 == 32"]
    Since the CPU only supports PARAM_173==32, this is hardwired to 1.
    
    [when,"PARAM_173 == 64"]
    Since the CPU only supports PARAM_173==64, this is hardwired to 2.
    
    [when,"PARAM_173 == 3264"]
    --
    It is not valid to have PARAM_144 less than PARAM_173.
    
    It is UNDEFINED_LEGAL what will happen if a software sets `mstatus.SXL` to be greater than `mstatus.UXL`.
    
    It is UNDEFINED_LEGAL to set the MSB of UXL.
    --
- `TSR` (bits 22), access RW
    When 1, attempts to execute the `sret` instruction while executing in HS/S-mode
    will raise an Illegal Instruction exception.
    
    [when,"ext?(:H)"]
    Does not affect the behavior of `sret` in VS_mode (see `hstatus.VTSR`).
- `TW` (bits 21), access RW
    When 1, the WFI instruction will raise an Illegal Instruction trap after an
    implementaion-defined wait period when executed in a mode other than M-mode.
    
    When 0, the `wfi` instruction is permitted to wait forever in (H)S-mode but must
    trap after an implementation-defined wait period in U-mode.
- `TVM` (bits 20)
    When 1, an `Illegal Instruction` trap occurs when
    
    * writing the `satp` CSR, executing an `sfence.vma`, or executing an `sinval.vma` while in (H)S-mode (but not VS-mode)
    * writing the `hgtap` CSR, executing an `hfence.gvma`, or executing an `hinval.gvma` while in HS-mode
    
    Notably, `mstatus.TVM` does *not* cause
    
    *`hfence.vvma`, `sfence.w.inval`, or `sfence.inval.ir` to trap.
    * Any additional traps in VS-mode (controlled via `hstatus.VTVM` instead).
- `MXR` (bits 19), access RW
    When 1, loads from pages marked readable *or executable* are allowed.
    When 0, loads from pages marked executable raise a Page Fault exception.

### CSR `vxrm`
Vector Fixed-Point Rounding Mode | address 10 | privilege U

Holds a 2-bit read-write rounding-mode field in the least-significant bits

Fields:
- `VALUE` (bits 63-0), access RW-H
    The vector fixed-point rounding-mode register holds a two-bit read-write rounding-mode field in the
    least-significant bits (vxrm[1:0]). The upper bits, vxrm[XLEN-1:2], should be written as zeros.
    The vector fixed-point rounding-mode is given a separate CSR address to allow independent access,
    but is also reflected as a field in vcsr.
    
    [NOTE]
    A new rounding mode can be set while saving the original rounding mode using a single csrwi instruction.
    
    The fixed-point rounding algorithm is specified as follows. Suppose the pre-rounding result is v, and d
    bits of that result are to be rounded off. ...

### CSR `vsstatus`
Virtual Supervisor Status | address 512 | privilege VS

The vsstatus register tracks and controls the hart's current operating state.

It is VS-mode's version of `sstatus`, and substitutes for it when in VS-mode
(_i.e._, in VS-mode CSR address 0x100 is `vsstatus`, not `sstatus`).

Unlike the relationship between `sstatus` and `mstatus`, none of the bits in `vsstatus` are
aliases of another field.

Fields:
- `SD` (bits 63), access RO-H
    *State Dirty*
    
    Read-only bit that summarizes whether any of the
    `vsstatus.FS`,  `vsstatus.VS`,  or `vsstatus.XS`
    fields signal the presence of some dirty state
    (_i.e._, any of them hold the value `11`).
    
    This bit is _not_ an alias of `mstatus.SD` since
    it only reflects the state visible to VS-mode
    (_e.g._, `status.FS` does not affect `vsstatus.SD`).
- `UXL` (bits 33-32)
    *VU-mode XLEN*
    
    Sets the effective XLEN for VU-mode (0 = 32-bit, 1 = 64-bit, 2 = 128-bit).
    
    [when,"PARAM_184 == 32"]
    Since the hart only supports PARAM_184==32, this is hardwired to 0.
    
    [when,"PARAM_184 == 64"]
    Since the hart only supports PARAM_184==64, this is hardwired to 1.
- `MXR` (bits 19), access RW
    *Make eXecutable Readable*
    
    Makes it possible to read executable pages when loading from effective VU-mode or VS-mode
    (normally, executable pages are not readable).
    
    * When 1, load in effective VU-mode or VS-mode from pages marked readable *or executable*
      are allowed as long as the page is marked readable (or executable and `status.MXR` is set) in the
      G-stage translation.
    * When 0, load in effective VU-mode or VS-mode from pages marked executable raise a
      Page Fault exception (unless `sstatus.MXR` is also set, in which case the above applies).
    
    'vsstatus.MXR' affects all loads that ...
- `SUM` (bits 18), access RW
    *permit Supervisor Memory Access*
    
    Allows VS-mode to read user pages.
    
    Applies to the following loads and stores:
    
    * All loads and stores in VS-mode.
    * All loads and stores in M-mode when `mstatus.MPRV` == 1, `mstatus.MPP` == 1, and `mstatus.MPV` == 1
    * Loads and stores generated by one of the `hlv.*`, `hlvx.*`, or `hsv.*` instructions.
    
    When `vsstatus.SUM` is 0, the loads and stores from the above categories cause an
    `Illegal Instruction` exception if they access a user page during VS-level translation.
    Otherwise, a load or store from the above categories is permitted to access a user ...
- `XS` (bits 16-15), access RO
    *Custom (X) extension context Status*
    
    Summarizes the current state of any custom extension state.
    Either 0 - Off, 1 - Initial, 2 - Clean, 3 - Dirty.
    Since there are no custom extensions, this field is read-only 0.
- `FS` (bits 14-13), access RW-H
    *Floating point context status*
    
    When 0, floating point instructions (from F and D extensions) in VS-mode or VU-mode are disabled,
    and cause ILLEGAL INSTRUCTION exceptions.
    Floating point instructions in all modes, including VS-mode and VU-mode,
    are similarly disabled when `mstatus.FS` is clear.
    
    When a floating point register, or the `fcsr` register is written in VS-mode or VU-mode,
    `vsstatus.FS` is written with the value 3.
    
    Values 1 and 2 are valid write values for software, but are not interpreted by hardware
    other than to possibly enable a previously-disabled floating point unit.
- `VS` (bits 10-9), access RW-H
    *Vector context status*
    
    When 0, vector instructions (from the V extension) are disabled, and cause ILLEGAL INSTRUCTION exceptions.
    When a vector register or vector CSR is written, VS obtains the value 3.
    Values 1 and 2 are valid write values for software, but are not interpreted by hardware
    other than to possibly enable a previously-disabled vector unit.
- `SPP` (bits 8), access RW-H
    *VS-mode Previous Privilege*
    
    Written with the prior nominal privilege level (_i.e._, 0 for VU-mode and 1 for VS-mode)
    when entering VS-mode from an exception/interrupt.
    Can also be written by software without immediate side-effect.
    
    On a return from an exception from VS-mode, the machine will enter the nominal privilege level
    stored in `vsstatus.SPP`.
- `UBE` (bits 6)
    *VU-mode Big Endian*
    
    Controls the endianness of VU-mode (0 = little, 1 = big).
    
    [when,"PARAM_185 == 'little'"]
    Since the CPU does not support big endian, this is hardwired to 0.
    
    [when,"PARAM_185 == 'big'"]
    Since the CPU does not support big endian, this is hardwired to 1.
- `SPIE` (bits 5), access RW-H
    *VS-mode Previous Interrupt Enable*
    
    Written by hardware in two cases:
    
    * Written with prior value of `vsstatus.SIE` when entering VS-mode from an exception/interrupt.
    * Written with the value 1 when returning from an exception in VS-mode (via the `sret` instruction).
    
    Can also be written by software without immediate side effect.
    
    Other than serving as a record of nested traps as described above, `vsstatus.SPIE` does not affect execution.
- `SIE` (bits 1), access RW-H
    *VS-mode Interrupt Enable*
    
    Written by hardware in two cases:
    
    * Written with the value 0 when entering VS-mode from an exception/interrupt.
    * Written with the prior value of `vsstatus.SPIE` when returning from an exception in VS-mode (via `sret`).
    
    Affects execution by:
    
    * When 0, all VS-mode interrupts are disabled when the current privilege level is VS ((H)S-mode and M-mode interrupts are still enabled).
    * When 1, VS-mode interrupts that are not otherwise disabled with a field in `vsie` are enabled.

### CSR `vxsat`
Vector Fixed-Point Saturate Flag | address 9 | privilege U

Indicates if a fixed-point instruction has had to saturate an output value to fit into a destination format

Fields:
- `VALUE` (bits 63-0), access RW-H
    The vxsat CSR has a single read-write least-significant bit (vxsat[0]) that indicates if a fixed-point
    instruction has had to saturate an output value to fit into a destination format. Bits vxsat[XLEN-1:1]
    should be written as zeros.
    
    The vxsat bit is mirrored in vcsr.

### CSR `vcsr`
Vector Control and Status Register | address 15 | privilege U

Contains aliases to vxrm and vxsat CSRs

Fields:
- `VXRM` (bits 2-1), access RW-RH
    See vxrm.
- `VXSAT`, access RW-RH
    See vxsat.

### CSR `vlenb`
Vector Byte Length | address 3106 | privilege U

Holds the value PARAM_177/8, the vector register length in bytes.

Fields:
- `VALUE` (bits 63-0), access RO
    The value in vlenb is a design-time constant in any implementation.
    Without this CSR, several instructions are needed to calculate PARAM_177 in bytes, and the code
    has to disturb current vl and vtype settings which require them to be saved and restored.