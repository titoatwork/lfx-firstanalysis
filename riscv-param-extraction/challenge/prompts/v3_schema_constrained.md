# Prompt v3 — schema-constrained (production challenge prompt)

**Status:** active for challenge runs.  
**Fixes vs v2:** UDB-shaped param documents; explicit empty-result permission; few-shot discipline without leaking GT for other names.

---

```text
You extract architectural parameters from RISC-V ISA Manual excerpts for the
RISC-V Unified Database (UDB).

OPTIONALITY TRIGGERS (parameter only if text supports implementation choice):
  may, might, should, optional, optionally,
  implementation-defined, implementation-specific

NOT PARAMETERS:
  - Fixed architectural conventions ("by convention", mandatory encodings)
  - Normative shall/must that do not leave a software-observable choice
  - Software/compiler advice that does not configure hardware
  - Content not present in the snippet (closed world)

ANTI-HALLUCINATION
1. Every parameter needs a verbatim quote from the snippet.
2. Returning ZERO parameters is valid and expected when the snippet has no
   implementation choices.
3. Prefer independent parameters when the text lists independent choices
   (do not bundle unrelated axes into one parameter).
4. If the value space is not specified, use a minimal schema and say so in
   description, do not invent enums.

OUTPUT FORMAT
Emit zero or more UDB-shaped YAML documents. Each document:
  $schema: param_schema.json#
  kind: parameter
  name: UPPER_SNAKE_CASE
  long_name: short title
  description: |
    ...
  definedBy:  # extension condition or "Privileged ISA" string form if unknown
  schema: { type: integer|boolean|string|... }

Also emit a sibling evidence object (JSON) per parameter:
  { "name": "...", "snippet": "cmo_cache_block.txt", "quote": "..." }

FEW-SHOT SHAPE (structure only, do not copy blindly if evidence differs):
Existing merged UDB parameter CACHE_BLOCK_SIZE is type integer, minimum 1,
gated by Zicbom/Zicbop/Zicboz. Modeling independent cache capacity/organization
as separate parameters when the text treats them as independent is preferred
over one bundled parameter.

SNIPPET:
{{SNIPPET}}
```
