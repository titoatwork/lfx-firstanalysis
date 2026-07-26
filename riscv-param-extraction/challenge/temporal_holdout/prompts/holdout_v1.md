# Holdout prompt v1 — baseline / treatment (shared template)

**Status:** frozen for pilot `temporal-holdout-artifact-c-v1`.  
**Do not edit** after first live run without bumping `prompt_version`.

Placeholders:

- `{{SOURCE}}` — case source excerpt  
- `{{CONTEXT_BLOCK}}` — empty for baseline; CSR/field block for treatment  

```text
You extract architectural parameters from RISC-V ISA Manual excerpts for the
RISC-V Unified Database (UDB).

OPTIONALITY TRIGGERS (emit a parameter only if text supports an implementation choice):
  may, might, should, optional, optionally,
  implementation-defined, implementation-specific,
  WARL, WLRL (when the legal value set is implementation-defined)

NOT PARAMETERS:
  - Fixed architectural conventions ("by convention", mandatory encodings)
  - Normative shall/must that leave no software-observable choice
  - Software/compiler advice that does not configure hardware
  - Content not present in the provided SOURCE (closed world; context is assist only)

ANTI-HALLUCINATION
1. Every parameter needs a verbatim quote from SOURCE (preferred) or from the
   CSR/FIELD CONTEXT block if provided.
2. Returning ZERO parameters is valid when there is no implementation choice.
3. Prefer independent parameters; do not invent names not justified by text.
4. If value space is unspecified, use a minimal schema; do not invent enums.

CLASS LABEL (optional field on each param):
  NORM_CSR_WARL | NORM_CSR_RW | NORM_DIRECT | OTHER

OUTPUT FORMAT
Emit zero or more YAML documents. Each document:
  $schema: param_schema.json#
  kind: parameter
  name: UPPER_SNAKE_CASE
  class: NORM_CSR_WARL   # if known
  long_name: short title
  description: |
    ...
  definedBy: Privileged ISA
  schema: { type: integer|boolean|string|array|... }

Also emit a sibling evidence object (JSON) per parameter:
  { "name": "...", "quote": "..." }

SOURCE:
{{SOURCE}}
{{CONTEXT_BLOCK}}
```
