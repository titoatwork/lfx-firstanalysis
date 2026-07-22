# pipeline/ — Artifact A (multi-model)

**Status:** scaffold only until an API key is available.

Plan order (locked):

1. Phase 1 **pilot** on `machine.adoc` (`extract.py pilot`) in the local UDB clone  
2. Then full second-model run (gpt4o or gemini) with v2 prompts  
3. Agreement / hallucination-overlap tables vs committed `claude-sonnet-4`  

This directory will hold thin, domain-named wrappers and comparison scripts — not a generic chatbot app. Manifests for every serious run go in `../manifests/`.

Do not invent multi-model metrics until a real run exists.
