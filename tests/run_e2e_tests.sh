#!/usr/bin/env bash
#
# Dotfiles E2E Test Suite Runner
# Requirements R1 - R4 Acceptance Verification
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Verify Python 3 is available
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 is required to run the E2E test suite but was not found." >&2
    exit 1
fi

export PYTHONPATH="$REPO_ROOT:${PYTHONPATH:-}"

echo "[*] Launching Dotfiles E2E Acceptance Test Runner..."
exec python3 "$REPO_ROOT/tests/test_e2e.py" "$@"
