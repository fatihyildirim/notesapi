#!/usr/bin/env sh
set -e

echo "Applying migrations..."
alembic upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}