# param_extraction scripts inventory


## analyze.py

`python
#!/usr/bin/env python3
# Copyright (c) 2026 Contributors to the RISCV UnifiedDB <https://github.com/riscv/riscv-unified-db>
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""
Phase 5: Analyze, deduplicate, align, and evaluate LLM extraction results.

Compares Claude extraction results against UDB ground truth to produce
metrics, discrepancy reports, and a clean deduplicated parameter list.

Modes:
  dedup   — deduplicate per-model results, keep highest-confidence instance
  align   — align LLM params to UDB via exact + fuzzy matching
  metrics — compute recall, precision proxy, classification accuracy
  report  — generate discrepancies.csv and summary report
  all     — run all steps in sequence
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RESULTS_DIR = PROJECT_DIR / "results"
DATA_DIR = PROJECT_DIR / "data"

logger = logging.getLogger("analyze")

# ── UDB parameters that come from the debug spec, not priv/unpriv ──────────
# These are excluded from recall calculations since we don't process debug files.
DEBUG_SPEC_PREFIXES = ("DBG_", "DCSR_", "TRIGGER_", "TDATA_", "MCONTEXT_", "HCONTEXT_", "SCONTEXT_")


# ── Data loading ───────────────────────────────────────────────────────────


def load_merged_results(model_display: str = "claude-sonnet-4") -> dict:
    path = RESULTS_DIR / f"all_results_{model_display}.json"
`


## chunker.py

`python
#!/usr/bin/env python3
# Copyright (c) 2026 Contributors to the RISCV UnifiedDB <https://github.com/riscv/riscv-unified-db>
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""
AsciiDoc-aware chunker for the RISC-V specification.

Splits spec .adoc files into semantically coherent chunks that preserve
CSR section integrity and respect LLM context window limits.

Chunking rules:
  1. Never split within a ==== section (CSR sections are atomic)
  2. Split at === or ==== boundaries
  3. Target chunk size: 2500-3500 lines (~35K-45K tokens)
  4. Include overlap at boundaries (heading + first paragraph of previous)
  5. Files under 2000 lines are a single chunk

Output:
  chunks/ directory with numbered chunk files and a manifest.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
SPEC_DIR = PROJECT_DIR.parent / "ext" / "riscv-isa-manual" / "src"
CHUNKS_DIR = PROJECT_DIR / "chunks"

TARGET_MIN_LINES = 2500
TARGET_MAX_LINES = 3500
SMALL_FILE_THRESHOLD = 2000
OVERLAP_LINES = 30


@dataclass
class Section:
    """A section of an AsciiDoc file."""

    line_start: int  # 0-based
`


## export_udb_params.py

`python
#!/usr/bin/env python3
"""
Phase 1, Step 1: Export all UDB parameters to structured JSON.

Reads every spec/std/isa/param/*.yaml file (excluding MOCK_* test fixtures),
extracts metadata, derives value types from JSON Schema structures,
cross-references with CSR definitions to find WARL connections,
and heuristically classifies each parameter.

Output: data/ground_truth.json
"""

import yaml
import json
import re
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PARAM_DIR = REPO_ROOT / "spec" / "std" / "isa" / "param"
CSR_DIR = REPO_ROOT / "spec" / "std" / "isa" / "csr"
SPEC_DIR = REPO_ROOT / "ext" / "riscv-isa-manual" / "src"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Schema analysis: derive the "value type" from JSON Schema structures
# ---------------------------------------------------------------------------

def derive_value_type(schema):
    """
    Analyze a JSON Schema object and return a structured description
    of the parameter's value type.

    Returns a dict with:
      - type: one of "binary", "enum", "range", "set", "bitmask",
              "value", "conditional", "unknown"
      - details: type-specific metadata
    """
    if schema is None:
`


## extract.py

`python
#!/usr/bin/env python3
# Copyright (c) 2026 Contributors to the RISCV UnifiedDB <https://github.com/riscv/riscv-unified-db>
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""
LLM extraction pipeline for RISC-V architectural parameters.

Assembles prompts from Phase 2 templates, sends them to LLM APIs,
parses structured JSON responses, and stores results per chunk and model.

Modes:
  pilot   — run extraction on machine.adoc chunks only (for prompt validation)
  run     — run extraction on all chunks
  merge   — merge per-chunk results into a single all_results_{model}.json
  status  — show progress (which chunks have been processed)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
CHUNKS_DIR = PROJECT_DIR / "chunks"
RESULTS_DIR = PROJECT_DIR / "results"
PROMPTS_DIR = PROJECT_DIR / "prompts" / "v1"
DATA_DIR = PROJECT_DIR / "data"

PROMPT_VERSION = os.environ.get("PROMPT_VERSION", "v1")

sys.path.insert(0, str(SCRIPT_DIR))
from run_prompt import (  # noqa: E402
    estimate_tokens,
    format_examples_section,
    format_param_names_section,
    load_examples,
    load_system_prompt,
`


## generate_report.py

`python
#!/usr/bin/env python3
"""
Phase 1, Final: Generate a comprehensive human-readable report and CSV
from the ground truth and spec mapping data.

Produces:
  - data/phase1_report.txt    (human-readable summary)
  - data/parameters_catalog.csv  (spreadsheet-ready catalog)
  - data/udb_param_names.txt  (flat list for LLM prompt inclusion)

Reads:
  - data/ground_truth.json
  - data/spec_mappings.json
"""

import json
import csv
from pathlib import Path
from collections import defaultdict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def main():
    # Load data
    with open(DATA_DIR / "ground_truth.json", encoding="utf-8") as f:
        gt = json.load(f)
    with open(DATA_DIR / "spec_mappings.json", encoding="utf-8") as f:
        sm = json.load(f)

    params = gt["parameters"]
    mappings = {m["parameter_name"]: m for m in sm["mappings"]}

    # Generate flat name list (for LLM prompts)
    names = sorted(p["name"] for p in params)
    names_path = DATA_DIR / "udb_param_names.txt"
    with open(names_path, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")
    print(f"Written {len(names)} parameter names to {names_path}")

    # Generate CSV catalog
    csv_path = DATA_DIR / "parameters_catalog.csv"
    generate_csv(params, mappings, csv_path)
    print(f"Written CSV catalog to {csv_path}")
`


## generate_spreadsheet.py

`python
#!/usr/bin/env python3
# Copyright (c) 2026 Contributors to the RISCV UnifiedDB <https://github.com/riscv/riscv-unified-db>
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""
Phase 7: Generate the final parameter spreadsheet.

Consolidates the V2 deduplicated LLM extraction results (Phase 6) with the
UDB ground truth (Phase 1) and the LLM↔UDB alignment (Phase 5) into a single
authoritative spreadsheet covering every confirmed parameter — both existing
UDB parameters and newly discovered ones.

Inputs (defaults; configurable via CLI):
  - param_extraction/results/v2/deduped_claude-sonnet-4.json   (Phase 6)
  - param_extraction/results/v2/alignment_claude-sonnet-4.json (Phase 5/6)
  - param_extraction/data/ground_truth.json                    (Phase 1)
  - param_extraction/data/udb_param_names.txt                  (Phase 1)

Outputs:
  - param_extraction/data/parameters.csv   (CSV for programmatic use)
  - param_extraction/data/parameters.xlsx  (Excel for review / presentation)
  - param_extraction/data/parameters_stats.txt (human-readable summary)

Columns (per Phase 7 acceptance criteria):
  adoc_file, line_number, excerpt, parameter_name, named,
  class, value_type, confidence, notes
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"

logger = logging.getLogger("phase7")

`


## insert_tags.py

`python
#!/usr/bin/env python3
# Copyright (c) 2026 Contributors to the RISCV UnifiedDB <https://github.com/riscv/riscv-unified-db>
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""
Phase 8: Insert ``[#param:NAME]`` tags into the riscv-isa-manual spec.

For every row in the Phase 7 spreadsheet, locate the verbatim excerpt in the
matching ``.adoc`` file and wrap it with ``[#param:NAME]#excerpt#`` — following
the existing ``[#norm:NAME]#text#`` convention already used ~1,361 times in
the upstream spec.

LLM-reported line numbers are advisory only (LLMs notoriously mis-count
lines); the matcher works on whitespace-normalized text across the whole
file and uses the line number purely as a proximity tiebreaker.

Edge cases handled:
  - Excerpt is already wrapped in a ``[#norm:NAME]#...#`` block      →
      emit a bare ``[#param:NAME]`` anchor on the preceding line so the
      anchor still attaches to the same paragraph without breaking the
      existing inline norm wrap.
  - Excerpt spans multiple source lines                              →
      wrap the entire span (joined by the original whitespace).
  - Multiple parameters on the same line                             →
      processed in left-to-right offset order, with offsets adjusted
      after each insertion.
  - Excerpt cannot be located                                        →
      logged and emitted to ``unmatched.csv`` for manual review; the
      ``.adoc`` file is not modified.

Modes:
  run     - tag every matchable row, write a per-file diff summary
  dry-run - same matching, but no files are modified (default)
  verify  - run asciidoctor on every modified file and check for errors

Inputs (defaults; configurable via CLI):
  - param_extraction/data/parameters.csv        (Phase 7 spreadsheet)
  - ext/riscv-isa-manual/src/*.adoc             (target files)

Outputs:
  - Modified .adoc files (in-place, under ext/riscv-isa-manual/src/)
  - param_extraction/data/tagging_report.txt    (per-file statistics)
  - param_extraction/data/tagging_unmatched.csv (rows that could not be located)
"""

from __future__ import annotations
`


## map_params_to_spec.py

`python
#!/usr/bin/env python3
"""
Phase 1, Step 2: Map UDB parameters to their source locations in the RISC-V spec.

For each parameter, searches the spec .adoc files for sentences that describe
the implementation choice that parameter represents. Uses multiple search
strategies: keyword matching from descriptions, CSR name references,
known WARL/implementation-defined language patterns, and exact name matches.

Reads:  data/ground_truth.json
Output: data/spec_mappings.json
"""

import json
import re
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SPEC_DIR = REPO_ROOT / "ext" / "riscv-isa-manual" / "src"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# Spec file loading and indexing
# ---------------------------------------------------------------------------

def load_spec_files():
    """Load all .adoc files from the spec directory, returning {filename: [lines]}."""
    spec_files = {}
    for adoc in sorted(SPEC_DIR.glob("*.adoc")):
        with open(adoc, encoding="utf-8") as f:
            spec_files[adoc.name] = f.readlines()
    return spec_files


def is_note_block(lines, line_idx):
    """
    Check if a given line is inside a NOTE/TIP/WARNING block (non-normative).
    AsciiDoc NOTE blocks are delimited by '===='.
    Also checks for explicit [NOTE]/[TIP]/[WARNING] markers.
    """
    note_markers = {"[NOTE]", "[TIP]", "[WARNING]", "[IMPORTANT]", "[CAUTION]"}

    # Look backwards from this line for the nearest block marker
`


## run_prompt.py

`python
#!/usr/bin/env python3
# Copyright (c) 2026 Contributors to the RISCV UnifiedDB <https://github.com/riscv/riscv-unified-db>
# SPDX-License-Identifier: BSD-3-Clause-Clear
"""
Prompt assembler for RISC-V architectural parameter extraction.

Combines system prompt + few-shot examples + UDB parameter names + spec chunk
into a complete prompt suitable for LLM analysis.

Three operational modes:
  assemble  — build and print a complete prompt for a given spec chunk
  chunk     — split a spec file into overlapping chunks suitable for LLM context
  estimate  — report token estimates for each prompt layer
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TypedDict

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
PROMPT_DIR = PROJECT_DIR / "prompts" / os.environ.get("PROMPT_VERSION", "v1")
DATA_DIR = PROJECT_DIR / "data"

CHARS_PER_TOKEN = 3.8

CONTEXT_LIMITS: dict[str, int] = {
    "gpt-4o": 128_000,
    "gpt-4-turbo": 128_000,
    "claude-3-5-sonnet": 200_000,
    "claude-3-opus": 200_000,
    "gemini-1.5-pro": 1_000_000,
    "llama-3-70b": 8_192,
    "default": 128_000,
}

RESERVED_OUTPUT_TOKENS = 4_096
SYSTEM_OVERHEAD_TOKENS = 200


`


## validate_prompt.py

`python
#!/usr/bin/env python3
"""
Validation script for Phase 2 deliverables.

Checks:
1. taxonomy.md completeness and consistency
2. examples.json structure, coverage, and spec text accuracy
3. system_prompt.txt output schema and taxonomy coverage
4. run_prompt.py assembly correctness and token budgets
5. Chunk boundary integrity
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
PROMPT_DIR = PROJECT_DIR / "prompts" / "v1"
DATA_DIR = PROJECT_DIR / "data"
SPEC_DIR = PROJECT_DIR.parent / "ext" / "riscv-isa-manual" / "src"

EXPECTED_CLASSES = {
    "NORM_DIRECT", "NORM_CSR_WARL", "NORM_CSR_RW", "SW_RULE",
    "NON_ISA", "NON_NORM", "DOC_RULE", "UNKNOWN",
}

EXPECTED_VALUE_TYPES = {"binary", "enum", "range", "set", "bitmask", "value"}

REQUIRED_OUTPUT_FIELDS = {
    "excerpt", "line_number", "parameter_name", "existing_udb_name",
    "class", "value_type", "confidence", "reasoning",
}

errors: list[str] = []
warnings: list[str] = []
checks_passed = 0


def check(condition: bool, message: str, *, warn_only: bool = False) -> None:
    global checks_passed
    if condition:
        checks_passed += 1
`
