# Manifest — challenge curated results

| Field | Value |
|-------|--------|
| Status | CURATED_REFERENCE (not multi-model API matrix) |
| Date | 2026-07-26 |
| Snippets | `cmo_cache_block.txt`, `csr_address_mapping.txt` |
| CMO params | CACHE_BLOCK_SIZE, CACHE_CAPACITY, CACHE_ORGANIZATION |
| CSR result | zero parameters (`csr_address_mapping.NO_PARAMETERS_FOUND.txt`) |
| Validation | `python scripts/validate.py --results results/curated` |
| Bad fixtures | 4 files under `tests/bad_examples/` (expect fail) |
| Live API | Not required for CI; `scripts/extract.py --live` optional with key |

Credit: Spring Part I pipeline context @ishaan-arora-1 / UDB PRs #1765–#1832.
Challenge task is the shared LFX applicant coding challenge (2 snippets).
