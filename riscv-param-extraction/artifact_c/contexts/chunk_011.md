## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

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

### CSR `hpmcounter3`
Unprivileged Hardware Performance Counter 3 | address 3075 | privilege U

Alias for M-mode CSR `mhpmcounter3`.

See `mhpmcounter3` for information on privilege mode access control.

Fields:
- `COUNT` (bits 63-0), access RO-H
    Alias of `mhpmcounter3.COUNT`.

### CSR `hpmcounter31`
Unprivileged Hardware Performance Counter 31 | address 3103 | privilege U

Alias for M-mode CSR `mhpmcounter31`.

See `mhpmcounter31` for information on privilege mode access control.

Fields:
- `COUNT` (bits 63-0), access RO-H
    Alias of `mhpmcounter31.COUNT`.

### CSR `hpmcounter31h`
Unprivileged Hardware Performance Counter 31, high half | address 3231 | privilege U

Alias for M-mode CSR `mhpmcounter31h`.

See `mhpmcounter31h` for information on privilege mode access control.

Fields:
- `COUNT` (bits 31-0), access RO-H
    Alias of `mhpmcounter31h.COUNT`.

### CSR `hpmcounter3h`
Unprivileged Hardware Performance Counter 3, high half | address 3203 | privilege U

Alias for M-mode CSR `mhpmcounter3h`.

See `mhpmcounter3h` for information on privilege mode access control.

Fields:
- `COUNT` (bits 31-0), access RO-H
    Alias of `mhpmcounter3h.COUNT`.