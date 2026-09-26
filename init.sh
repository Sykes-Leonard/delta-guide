#!/usr/bin/env bash
# ==============================================================================
# init.sh - Initialize / Brand Knowledge Guide for Your Organization
# ==============================================================================
# Usage:
#   ./init.sh
#   ./init.sh --org "Acme Health" --title "Acme Knowledge Base"
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=""

if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "ERROR: python3 not found. Python 3.8+ is required." >&2
    exit 1
fi

exec "$PYTHON_BIN" "$SCRIPT_DIR/scripts/init_repo.py" "$@"
