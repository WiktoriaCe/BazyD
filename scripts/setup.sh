#!/usr/bin/env bash
set -euo pipefail

echo "=== Quick Start Script for Medical Research Database ==="

PY=python3
VENV_DIR=".venv"

# Check for python3
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "Error: $PY not found. Install Python 3 and try again." >&2
  exit 1
fi

# Create virtualenv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR..."
  $PY -m venv "$VENV_DIR"
fi

# Activate venv for the duration of the script
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "Upgrading pip..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found; skipping dependency installation." >&2
fi

# Run Django migrations
if [ -f "manage.py" ]; then
  echo "Applying Django migrations..."
  python manage.py migrate --noinput
else
  echo "Error: manage.py not found. Are you in the project root?" >&2
  exit 1
fi

# Populate sample data if script exists
if [ -f "populate_data.py" ]; then
  echo "Loading sample data (populate_data.py)..."
  python populate_data.py
else
  echo "populate_data.py not found; skipping sample data load." >&2
fi

echo
echo "Quick Start finished successfully. To start the server:"
echo "  source $VENV_DIR/bin/activate"
echo "  python manage.py runserver"

echo "Admin credentials (if sample data created): admin / admin123"

exit 0
