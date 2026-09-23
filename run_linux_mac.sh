#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
  echo "Python 3.10+ is required. Install it with your operating system package manager."
  exit 1
fi
if [ ! -x .venv/bin/python ]; then
  "$PY" -m venv .venv
fi
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
