# Holdout prompt v1.2 — baseline / treatment (shared template)

**Status:** frozen for pilot `temporal-holdout-artifact-c-v1` (pre-live integrity revision).  
**Do not edit** after first live run without bumping `prompt_version`.

Placeholders:

- `{{SOURCE}}` — case source excerpt  
- `{{CONTEXT_BLOCK}}` — empty for baseline; CSR/field block for treatment  
- `{{DEFINEDBY_GUIDANCE}}` — case-specific definedBy shape (not a free license to invent)

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

OUTPUT FORMAT — UDB parameter documents only (must validate against param_schema):
Emit zero or more YAML documents. Each document MUST use ONLY these fields
(do NOT add a class field — UDB schema forbids additional properties):
  $schema: param_schema.json#
  kind: parameter
  name: UPPER_SNAKE_CASE
  long_name: short title
  description: |
    ...
  definedBy:   # MUST match the case guidance below; do NOT default everything to Sm
    ...
  schema: { type: integer|boolean|string|array|... }

definedBy MUST be case-correct. Valid shapes include:
  extension: { name: Sm }          # machine-mode
  extension: { name: S }           # supervisor
  extension: { name: Zvl32b }      # vector (e.g. SEW-related)
  param: { name: NUM_PMP_ENTRIES, greaterThan: 0 }   # gated by another param

CASE-SPECIFIC definedBy GUIDANCE (use this for parameters you emit from THIS source):
{{DEFINEDBY_GUIDANCE}}

EVALUATION METADATA (separate from UDB docs — not validated as parameters):
After all parameter YAML docs, emit ONE JSON object:
  {
    "eval": true,
    "items": [
      {
        "name": "PARAM_NAME",
        "class": "NORM_CSR_WARL|NORM_CSR_RW|NORM_DIRECT|OTHER",
        "quote": "verbatim quote from SOURCE or context"
      }
    ]
  }
Include one items[] entry per emitted parameter (same name). If zero parameters,
emit: {"eval": true, "items": []}

SOURCE:
{{SOURCE}}
{{CONTEXT_BLOCK}}
```
