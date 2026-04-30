#!/usr/bin/env bash
set -e

# Render/Railway/Fly compatible backend start command.
# The platform supplies PORT. Local fallback is 8000.
PORT=${PORT:-8000}
uvicorn main:app --host 0.0.0.0 --port "$PORT"
