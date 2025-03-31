#!/bin/sh

echo "Waiting for PostgreSQL to start..."
sleep 5

echo "Checking Alembic migrations..."
if [ -z "$(ls -A alembic/versions 2>/dev/null)" ]; then
    echo "No migrations found, creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

alembic upgrade head

exec uvicorn main:app --host 0.0.0.0 --port 8009
