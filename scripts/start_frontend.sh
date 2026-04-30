#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../frontend"
npm install
if [ ! -f .env ]; then
  cp .env.example .env
fi
npm run dev
