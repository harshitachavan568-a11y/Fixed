#!/usr/bin/env bash
# SmartPool launcher for macOS / Linux:  ./run_smartpool.sh
cd "$(dirname "$0")" || exit 1
PY="$(command -v python3 || command -v python)"
if [ -z "$PY" ]; then
  echo "Python 3.10+ is required: https://www.python.org/downloads/"; exit 1
fi
[ -d .venv ] || "$PY" -m venv .venv
.venv/bin/python -m pip install -q -r requirements-demo.txt || { echo "Package install failed (check internet)."; exit 1; }
exec .venv/bin/python run.py
