#!/usr/bin/env bash
# Re-derive every registered number from committed artifacts. No credentials, no
# network, no model calls. Fails if a registered figure disagrees with the file
# it came from. Coverage is the claim table in scripts/verify_claims.py, not a
# scan of the prose, so this proves the registered figures, not that every
# figure got registered.
#
#   ./verify.sh          everything
#   ./verify.sh --list   show the claim table without checking
#
# Exit 0 only if every checkable claim matches.

set -uo pipefail
cd "$(dirname "$0")"

export PYTHONUTF8=1
PY="${PYTHON:-python}"
fail=0
skipped=0

hr() { printf '%.0s-' {1..66}; echo; }

step() {
  local name="$1"; shift
  hr
  echo "## $name"
  hr
  if "$@"; then
    echo "   ok"
  else
    echo "   FAILED (exit $?)"
    fail=1
  fi
  echo
}

# Same as step, but exit 3 means "could not run here". Reported as skipped, and
# never folded into the pass line, so an unrun check cannot read as a passing one.
step_skippable() {
  local name="$1"; shift
  local rc=0
  hr
  echo "## $name"
  hr
  "$@" || rc=$?
  case "$rc" in
    0) echo "   ok" ;;
    3) echo "   SKIPPED, not checked here" ; skipped=$((skipped + 1)) ;;
    *) echo "   FAILED (exit $rc)" ; fail=1 ;;
  esac
  echo
}

if [ "${1:-}" = "--list" ]; then
  "$PY" riscv-param-extraction/scripts/verify_claims.py --list
  exit 0
fi

# Preflight. Fail with an instruction rather than a traceback three checks in.
if ! "$PY" -c "import yaml, jsonschema" 2>/dev/null; then
  echo "Missing verification dependencies (PyYAML, jsonschema)."
  echo
  echo "  pip install -r riscv-param-extraction/requirements.txt"
  echo
  echo "Nothing else is required. Verification is offline and uses no API key."
  exit 1
fi

# 1. Every number published in metrics.md and PRIMARY_RESULTS.md must re-derive
#    from a committed artifact.
step "registered claims re-derive from committed artifacts" \
  "$PY" riscv-param-extraction/scripts/verify_claims.py

# 2. Evaluation fixtures intact (including the WARL distinction they exist to
#    protect), and review metadata kept out of UDB-valid YAML.
step "eval fixtures + review-envelope separation" \
  "$PY" riscv-param-extraction/workflow_slice/scripts/ci_slice_check.py

# 3. No figure measured against the pinned corpus may be described as if it came
#    from live UDB. Pure wording gate, no UDB checkout needed.
step "no figure claims currency it cannot have" \
  "$PY" riscv-param-extraction/scripts/check_pinned_wording.py

# 4. The H5 evidence types are pin-dependent, so the documents name a commit for
#    each one. This checks the repository still says what they claim. Needs a UDB
#    clone beside this one; skips loudly without it.
step_skippable "H5 evidence types match UDB at their pinned commits" \
  "$PY" riscv-param-extraction/artifact_c/scripts/test_derivation_detector.py

# 5. The published census count must equal the threads actually listed. Offline
#    only: GitHub is the source of the count, and refreshing it is the --online
#    run documented in EVIDENCE.md 2.6.
step "census figures equal the threads listed" \
  "$PY" riscv-param-extraction/scripts/check_census.py

# 6. Step 1 proves every registered number re-derives. It cannot notice a number
#    that was published and never registered, which is how "exact-name 48.6% vs
#    6.2%" and "44 of 227" reached the public surface ungated. This reports that
#    gap and holds it to a recorded baseline so it can shrink but not grow.
step "no new published figure escapes the claim table" \
  "$PY" riscv-param-extraction/scripts/check_claim_coverage.py

# 7. The coding-challenge pack publishes three figures about ten models on two
#    snippets. Until the raw outputs were published on 2026-08-11 those were prose
#    and nothing could contradict them. This re-derives all three from the
#    committed per-model responses. Offline: the model calls happened once, on
#    2026-07-26, and their outputs are in the tree.
step "coding-challenge model figures re-derive from the raw outputs" \
  "$PY" riscv-param-extraction/scripts/check_challenge_matrix.py

hr
if [ "$fail" -eq 0 ]; then
  echo "PASS  every registered number re-derives, and every gate holds"
  [ "$skipped" -gt 0 ] && echo "      ($skipped check(s) skipped above, not counted as passing)"
else
  echo "FAIL  see above"
fi
hr
exit "$fail"
