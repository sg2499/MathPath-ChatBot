#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../backend"
if [ ! -d .venv ]; then
  python -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created backend/.env. Add your OPENAI_API_KEY and ADMIN_API_KEY before production."
fi
uvicorn main:app --reload --host 0.0.0.0 --port 8000
