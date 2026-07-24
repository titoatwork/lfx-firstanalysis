### Inter-model agreement (parameter names)

| Metric | Value |
|--------|------:|
| Model A | claude-sonnet-4 |
| Model B | gpt-4o-mini |
| Unique params A | 346 |
| Unique params B | 230 |
| Shared names | 21 |
| Only A | 325 |
| Only B | 209 |
| Jaccard (name) | 3.8% |
| Match rate vs A (|shared|/|A|) | 6.1% |
| Match rate vs B (|shared|/|B|) | 9.1% |
| Class agreement on shared (evaluated) | 81.0% (17/21) |

### Hallucination-overlap (proposed-new)

| Metric | Value |
|--------|------:|
| Confidence filter | high |
| Proposed-new A | 236 |
| Proposed-new B | 218 |
| Both models (overlap) | 9 |
| Only A | 227 |
| Only B | 209 |
| Overlap rate vs A | 3.8% |
| Overlap rate vs B | 4.1% |

_Proposed-new = name not in UDB set and no trusted existing_udb_name hit; confidence==high only. UDB names loaded: 185._
