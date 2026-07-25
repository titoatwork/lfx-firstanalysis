# Prompt v1 — naive (baseline failure mode)

**Status:** documentation of first attempt — do **not** use for production extract.  
**Observed failure:** over-triggers on technical convention text (CSR address mapping) as if it were implementation-defined parameters.

---

```text
You extract architectural parameters from RISC-V ISA Manual text.

An architectural parameter is a value, option, or behavior that a conforming
implementation may choose or that is left open by the specification.

Read the snippet below and list every architectural parameter you find.
For each parameter output YAML with fields: name, description, type, constraints.

SNIPPET:
{{SNIPPET}}
```

## Failure notes

- Flags fixed CSR encoding conventions as parameters.
- Invents constraints not present in the text.
- No evidence quote requirement → hallucinations hard to reject mechanically.
