## CSR and field reference for this excerpt
Definitions of CSRs named in the text above. Reference material only.

### CSR `mseccfg`
Machine Security Configuration | address 1863 | privilege M

Machine Security Configuration

### CSR `marchid`
Machine Architecture ID | address 3858 | privilege M

The `marchid` CSR is an PARAM_074-bit read-only register encoding the base
microarchitecture of the hart. This register must be readable in any
implementation, but a value of 0 can be returned to indicate the field
is not implemented. The combination of `mvendorid` and `marchid` should
uniquely identify the type of hart microarchitecture that is
implemented.

Open-source project architecture IDs are ...

Fields:
- `Architecture` (bits 63-0), access RO
    Vendor-specific microarchitecture ID.

### CSR `mimpid`
Machine Implementation ID | address 3859 | privilege M

Reports the vendor-specific implementation ID.

The `mimpid` CSR provides a unique encoding of the version of the
processor implementation. This register must be readable in any
implementation, but a value of 0 can be returned to indicate that the
field is not implemented. The Implementation value should reflect the
design of the RISC-V processor itself and not any surrounding ...

Fields:
- `Implementation` (bits 63-0), access RO
    Vendor-specific implementation ID.

### CSR `mvendorid`
Machine Vendor ID | address 3857 | privilege M

Reports the JEDEC manufacturer ID of the core.

Fields:
- `Bank` (bits 31-7), access RO
    JEDEC manufacturer ID bank minus 1
- `Offset` (bits 6-0), access RO
    JEDEC manufacturer ID offset