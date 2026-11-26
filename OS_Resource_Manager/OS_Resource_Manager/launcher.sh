#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "          OS RESOURCE MANAGER"
echo "=========================================="

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is not installed or not in PATH."
    exit 1
fi

mkdir -p reports logs

if [[ ! -d ".venv" ]]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

PYTHON=".venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
    PYTHON="python3"
fi

if [[ -f "requirements.txt" ]]; then
    "$PYTHON" -m pip install -r requirements.txt
fi

echo "Launching application..."
"$PYTHON" main.py 2>&1 | tee -a logs/launcher.log
