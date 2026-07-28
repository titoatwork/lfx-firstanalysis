#!/usr/bin/env bash
# Re-derive every published number from committed artifacts. No credentials, no
# network, no model calls. Fails if any published figure disagrees with the file
# it came from.
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

if [ "${1:-}" = "--list" ]; then
  "$PY" riscv-param-extraction/scripts/verify_claims.py --list
  exit 0
fi

# 1. Every number published in metrics.md and PRIMARY_RESULTS.md must re-derive
#    from a committed artifact.
step "published claims re-derive from committed artifacts" \
  "$PY" riscv-param-extraction/scripts/verify_claims.py

# 2. The coding-challenge pack: fail-closed fixtures, hard negatives, markup
#    robustness, known-parameter bench. The [FAIL] lines it prints are the
#    bad_examples deliberately failing; the gate is its own exit code.
step "coding challenge CI gate" \
  "$PY" riscv-param-extraction/challenge/scripts/ci_check.py

# 3. Evaluation fixtures intact (including the WARL distinction they exist to
#    protect), and review metadata kept out of UDB-valid YAML.
step "eval fixtures + review-envelope separation" \
  "$PY" riscv-param-extraction/workflow_slice/scripts/ci_slice_check.py

hr
if [ "$fail" -eq 0 ]; then
  echo "PASS  every published number re-derives, and every gate holds"
else
  echo "FAIL  see above"
fi
hr
exit "$fail"
