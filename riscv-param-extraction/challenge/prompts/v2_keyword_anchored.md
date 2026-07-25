# Prompt v2 — keyword-anchored + verbatim quote

**Status:** intermediate.  
**Fixes vs v1:** restrict to optionality language; require verbatim evidence quotes.  
**Remaining gap:** no schema contract; models still sometimes invent structure; empty list not explicit.

---

```text
You extract architectural parameters from RISC-V ISA Manual excerpts.

DEFINITION
A parameter is an implementation-configurable value, option, presence, or
behavior signaled by optionality language in the provided text ONLY:
  may / might / should / optional / optionally /
  implementation-defined / implementation-specific

NOT a parameter:
  - "shall" / "must" constraints by themselves
  - fixed encodings and "by convention" mapping rules every implementation shares
  - anything not supported by a verbatim quote from the snippet

RULES
1. Use only the snippet. No external ISA knowledge, no UDB memorization.
2. Every parameter MUST include a verbatim quote from the snippet as evidence.
3. If no optionality language supports a parameter, do not emit it.

OUTPUT
YAML list of objects with: name (UPPER_SNAKE_CASE), description, type,
constraints, quote (verbatim substring).

SNIPPET:
{{SNIPPET}}
```
