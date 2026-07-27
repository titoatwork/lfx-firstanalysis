## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `mseccfg`
Machine Security Configuration | address 1863 | privilege M

Machine Security Configuration

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