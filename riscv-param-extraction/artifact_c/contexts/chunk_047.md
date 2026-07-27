## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `minstretcfg`
Machine Instructions-Retired Counter Configuration | address 802 | privilege M

The `minstretcfg` CSR is a 64-bit machine-level register that configures privilege
mode filtering for the `minstret` (Machine Instructions-Retired Counter). Each inhibit bit (xINH)
disables counting of retired instructions in the associated privilege mode.

| Field   | Description                                               ...

Fields:
- `MINH` (bits 62), access RW
    If set, then counting of events in M-mode is inhibited.
- `SINH` (bits 61), access RW
    If set, then counting of events in S/HS-mode is inhibited.
- `UINH` (bits 60), access RW
    If set, then counting of events in U-mode is inhibited.
- `VSINH` (bits 59), access RW
    If set, then counting of events in VS-mode is inhibited.
- `VUINH` (bits 58), access RW
    If set, then counting of events in VU-mode is inhibited.

### CSR `mcyclecfg`
Machine Cycle Counter Configuration | address 801 | privilege M

The `mcyclecfg` CSR is a 64-bit machine-level register that configures privilege
mode filtering for the cycle counter. Each inhibit bit (xINH) suppresses
counting of events in the corresponding privilege mode when set.

| Field   | Description                                             |
|---------|---------------------------------------------------------|
| MINH    | If set, then counting of ...

Fields:
- `MINH` (bits 62), access RW
    If set, then counting of events in M-mode is inhibited.
- `SINH` (bits 61), access RW
    If set, then counting of events in S/HS-mode is inhibited.
- `UINH` (bits 60), access RW
    If set, then counting of events in U-mode is inhibited.
- `VSINH` (bits 59), access RW
    If set, then counting of events in VS-mode is inhibited.
- `VUINH` (bits 58), access RW
    If set, then counting of events in VU-mode is inhibited.

### CSR `mcountinhibit`
Machine Counter Inhibit | address 800 | privilege M

Bits to inhibit (stops counting) performance counters.

The counter-inhibit register `mcountinhibit` is a *WARL* register that
controls which of the hardware performance-monitoring counters
increment. The settings in this register only control whether the
counters increment; their accessibility is not affected by the setting
of this register.

When the CY, IR, or HPM__n__ bit in the ...

Fields:
- `CY`
    When set, `mcycle.COUNT` stops counting in all privilege modes.
- `IR` (bits 2)
    When set, `minstret.COUNT` stops counting in all privilege modes.
- `HPM3` (bits 3)
    [when="PARAM_005[3] == true"]
    When set, `hpmcounter3.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[3] == false"]
    Since hpmcounter3 is not implemented, this field is read-only zero.
- `HPM4` (bits 4)
    [when="PARAM_005[4] == true"]
    When set, `hpmcounter4.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[4] == false"]
    Since hpmcounter4 is not implemented, this field is read-only zero.
- `HPM5` (bits 5)
    [when="PARAM_005[5] == true"]
    When set, `hpmcounter5.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[5] == false"]
    Since hpmcounter5 is not implemented, this field is read-only zero.
- `HPM6` (bits 6)
    [when="PARAM_005[6] == true"]
    When set, `hpmcounter6.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[6] == false"]
    Since hpmcounter6 is not implemented, this field is read-only zero.
- `HPM7` (bits 7)
    [when="PARAM_005[7] == true"]
    When set, `hpmcounter7.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[7] == false"]
    Since hpmcounter7 is not implemented, this field is read-only zero.
- `HPM8` (bits 8)
    [when="PARAM_005[8] == true"]
    When set, `hpmcounter8.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[8] == false"]
    Since hpmcounter8 is not implemented, this field is read-only zero.
- `HPM9` (bits 9)
    [when="PARAM_005[9] == true"]
    When set, `hpmcounter9.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[9] == false"]
    Since hpmcounter9 is not implemented, this field is read-only zero.
- `HPM10` (bits 10)
    [when="PARAM_005[10] == true"]
    When set, `hpmcounter10.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[10] == false"]
    Since hpmcounter10 is not implemented, this field is read-only zero.
- `HPM11` (bits 11)
    [when="PARAM_005[11] == true"]
    When set, `hpmcounter11.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[11] == false"]
    Since hpmcounter11 is not implemented, this field is read-only zero.
- `HPM12` (bits 12)
    [when="PARAM_005[12] == true"]
    When set, `hpmcounter12.COUNT` stops counting in all privilege modes.
    
    [when="PARAM_005[12] == false"]
    Since hpmcounter12 is not implemented, this field is read-only zero.

### CSR `mcyclecfgh`
Machine Cycle Counter Configuration High | address 1825 | privilege M

Upper 32 bits of the 64-bit `mcyclecfg` CSR, used for RV32 systems to access
the privilege mode filtering inhibit bits.

Fields:
- `MINH` (bits 30), access RW
    If set, then counting of events in M-mode is inhibited.
- `SINH` (bits 29), access RW
    If set, then counting of events in S/HS-mode is inhibited.
- `UINH` (bits 28), access RW
    If set, then counting of events in U-mode is inhibited.
- `VSINH` (bits 27), access RW
    If set, then counting of events in VS-mode is inhibited.
- `VUINH` (bits 26), access RW
    If set, then counting of events in VU-mode is inhibited.

### CSR `minstretcfgh`
Machine Instructions-Retired Counter Configuration High | address 1826 | privilege M

Upper 32 bits of the 64-bit `minstretcfg` CSR, used on RV32 systems to access
privilege mode filtering inhibit bits for instruction retirement.

Fields:
- `MINH` (bits 30), access RW
    If set, then counting of events in M-mode is inhibited.
- `SINH` (bits 29), access RW
    If set, then counting of events in S/HS-mode is inhibited.
- `UINH` (bits 28), access RW
    If set, then counting of events in U-mode is inhibited.
- `VSINH` (bits 27), access RW
    If set, then counting of events in VS-mode is inhibited.
- `VUINH` (bits 26), access RW
    If set, then counting of events in VU-mode is inhibited.