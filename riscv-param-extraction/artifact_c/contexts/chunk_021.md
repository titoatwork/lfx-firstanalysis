## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `pmpaddr0`
PMP Address 0 | address 944 | privilege M

PMP entry address

Fields:
- `ADDR` (bits 63-0)
    Bits PARAM_078-1:2 of the address specifier for PMP entry 0
    (or, if `pmp1cfg.A` == TOR, for PMP entry 1).

### CSR `pmpcfg2`
PMP Configuration Register 2 | address 930 | privilege M

PMP entry configuration

Fields:
- `pmp8cfg` (bits 7-0)
    *PMP configuration for entry 8*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 7   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 6:5 ! _Reserved_ Writes shall be ignored.
    h! A ! 4:3
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        * ...
- `pmp9cfg` (bits 15-8)
    *PMP configuration for entry 9*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 15   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 14:13 ! _Reserved_ Writes shall be ignored.
    h! A ! 12:11
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp10cfg` (bits 23-16)
    *PMP configuration for entry 10*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 23   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 22:21 ! _Reserved_ Writes shall be ignored.
    h! A ! 20:19
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp11cfg` (bits 31-24)
    *PMP configuration for entry 11*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 31   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 30:29 ! _Reserved_ Writes shall be ignored.
    h! A ! 28:27
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp12cfg` (bits 39-32)
    *PMP configuration for entry 12*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 39   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 38:37 ! _Reserved_ Writes shall be ignored.
    h! A ! 36:35
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp13cfg` (bits 47-40)
    *PMP configuration for entry 13*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 47   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 46:45 ! _Reserved_ Writes shall be ignored.
    h! A ! 44:43
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp14cfg` (bits 55-48)
    *PMP configuration for entry 14*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 55   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 54:53 ! _Reserved_ Writes shall be ignored.
    h! A ! 52:51
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp15cfg` (bits 63-56)
    *PMP configuration for entry 15*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 63   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 62:61 ! _Reserved_ Writes shall be ignored.
    h! A ! 60:59
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...

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

### CSR `pmpcfg0`
PMP Configuration Register 0 | address 928 | privilege M

PMP entry configuration

Fields:
- `pmp0cfg` (bits 7-0)
    *PMP configuration for entry 0*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 7   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 6:5 ! _Reserved_ Writes shall be ignored.
    h! A ! 4:3
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        * ...
- `pmp1cfg` (bits 15-8)
    *PMP configuration for entry 1*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 15   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 14:13 ! _Reserved_ Writes shall be ignored.
    h! A ! 12:11
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp2cfg` (bits 23-16)
    *PMP configuration for entry 2*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 23   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 22:21 ! _Reserved_ Writes shall be ignored.
    h! A ! 20:19
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp3cfg` (bits 31-24)
    *PMP configuration for entry 3*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 31   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 30:29 ! _Reserved_ Writes shall be ignored.
    h! A ! 28:27
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp4cfg` (bits 39-32)
    *PMP configuration for entry 4*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 39   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 38:37 ! _Reserved_ Writes shall be ignored.
    h! A ! 36:35
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp5cfg` (bits 47-40)
    *PMP configuration for entry 5*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 47   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 46:45 ! _Reserved_ Writes shall be ignored.
    h! A ! 44:43
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp6cfg` (bits 55-48)
    *PMP configuration for entry 6*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 55   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 54:53 ! _Reserved_ Writes shall be ignored.
    h! A ! 52:51
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp7cfg` (bits 63-56)
    *PMP configuration for entry 7*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 63   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 62:61 ! _Reserved_ Writes shall be ignored.
    h! A ! 60:59
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...

### CSR `pmpcfg1`
PMP Configuration Register 1 | address 929 | privilege M

PMP entry configuration

Fields:
- `pmp4cfg` (bits 7-0)
    *PMP configuration for entry 4*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 7   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 6:5 ! _Reserved_ Writes shall be ignored.
    h! A ! 4:3
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        * ...
- `pmp5cfg` (bits 15-8)
    *PMP configuration for entry 5*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 15   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 14:13 ! _Reserved_ Writes shall be ignored.
    h! A ! 12:11
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp6cfg` (bits 23-16)
    *PMP configuration for entry 6*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 23   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 22:21 ! _Reserved_ Writes shall be ignored.
    h! A ! 20:19
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp7cfg` (bits 31-24)
    *PMP configuration for entry 7*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 31   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 30:29 ! _Reserved_ Writes shall be ignored.
    h! A ! 28:27
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...

### CSR `pmpcfg15`
PMP Configuration Register 15 | address 943 | privilege M

PMP entry configuration

Fields:
- `pmp60cfg` (bits 7-0)
    *PMP configuration for entry 60*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 7   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 6:5 ! _Reserved_ Writes shall be ignored.
    h! A ! 4:3
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        * ...
- `pmp61cfg` (bits 15-8)
    *PMP configuration for entry 61*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 15   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 14:13 ! _Reserved_ Writes shall be ignored.
    h! A ! 12:11
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp62cfg` (bits 23-16)
    *PMP configuration for entry 62*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 23   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 22:21 ! _Reserved_ Writes shall be ignored.
    h! A ! 20:19
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp63cfg` (bits 31-24)
    *PMP configuration for entry 63*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 31   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 30:29 ! _Reserved_ Writes shall be ignored.
    h! A ! 28:27
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...

### CSR `pmpaddr63`
PMP Address 63 | address 1007 | privilege M

PMP entry address

Fields:
- `ADDR` (bits 63-0)
    Bits PARAM_078-1:2 of the address specifier for PMP entry 63
    (or, if `pmp64cfg.A` == TOR, for PMP entry 64).

### CSR `pmpcfg14`
PMP Configuration Register 14 | address 942 | privilege M

PMP entry configuration

Fields:
- `pmp56cfg` (bits 7-0)
    *PMP configuration for entry 56*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 7   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 6:5 ! _Reserved_ Writes shall be ignored.
    h! A ! 4:3
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        * ...
- `pmp57cfg` (bits 15-8)
    *PMP configuration for entry 57*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 15   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 14:13 ! _Reserved_ Writes shall be ignored.
    h! A ! 12:11
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp58cfg` (bits 23-16)
    *PMP configuration for entry 58*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 23   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 22:21 ! _Reserved_ Writes shall be ignored.
    h! A ! 20:19
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp59cfg` (bits 31-24)
    *PMP configuration for entry 59*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 31   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 30:29 ! _Reserved_ Writes shall be ignored.
    h! A ! 28:27
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp60cfg` (bits 39-32)
    *PMP configuration for entry 60*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 39   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 38:37 ! _Reserved_ Writes shall be ignored.
    h! A ! 36:35
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp61cfg` (bits 47-40)
    *PMP configuration for entry 61*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 47   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 46:45 ! _Reserved_ Writes shall be ignored.
    h! A ! 44:43
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp62cfg` (bits 55-48)
    *PMP configuration for entry 62*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 55   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 54:53 ! _Reserved_ Writes shall be ignored.
    h! A ! 52:51
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...
- `pmp63cfg` (bits 63-56)
    *PMP configuration for entry 63*
    
    The bits are as follows:
    
    [separator="!",%autowidth]
    !===
    ! Name ! Location ! Description
    
    h! L ! 63   ! Locks the entry from further modification. Additionally, when set, PMP checks also apply to M-mode for the entry.
    h! - ! 62:61 ! _Reserved_ Writes shall be ignored.
    h! A ! 60:59
    a! Address matching mode. One of:
    
        [when="PARAM_081 < 2"]
        * *OFF* (0) - Null region (disabled)
        * *TOR* (1) - Top of range
        * *NA4* (2) - Naturally aligned four-byte region
        * *NAPOT* (3) - Naturally aligned power of two
    
        [when="PARAM_081 >= 2"]
        ...