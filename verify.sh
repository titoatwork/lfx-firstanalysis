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

hr
if [ "$fail" -eq 0 ]; then
  echo "PASS  every registered number re-derives, and every gate holds"
  [ "$skipped" -gt 0 ] && echo "      ($skipped check(s) skipped above, not counted as passing)"
else
  echo "FAIL  see above"
fi
hr
exit "$fail"
