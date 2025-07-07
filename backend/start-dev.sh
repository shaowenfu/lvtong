#!/bin/bash
# Fast local development launcher for Flask API
# Usage: bash start-dev.sh [flask|gunicorn]
# Default: flask (with hot reload)

set -e

# Create venv if not exists
if [ ! -d "venv" ]; then
  echo "[INFO] Creating Python virtual environment..."
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
echo "[INFO] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set environment variables for development
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Choose run mode
MODE=${1:-flask}

if [ "$MODE" = "gunicorn" ]; then
  echo "[INFO] Starting API with gunicorn (production-like)..."
  exec gunicorn --bind 0.0.0.0:5000 app:app
else
  echo "[INFO] Starting API with Flask development server (hot reload enabled)..."
  exec flask run --host=0.0.0.0 --port=5000
fi
