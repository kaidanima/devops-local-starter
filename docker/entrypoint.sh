#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] waiting for database..."
python - <<'PY'
import os, sys, time
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

user=os.getenv("POSTGRES_USER","appuser")
pwd=quote_plus(os.getenv("POSTGRES_PASSWORD","secretpassword") or "")
host=os.getenv("POSTGRES_HOST","db")
port=os.getenv("POSTGRES_PORT","5432")
db  =os.getenv("POSTGRES_DB","appdb")
url =f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"

for i in range(30):
    try:
        eng=create_engine(url, future=True)
        with eng.connect() as c:
            c.execute(text("SELECT 1"))
        print("[entrypoint] DB ready")
        sys.exit(0)
    except Exception as e:
        print(f"[entrypoint] DB not ready, retry {i+1}/30 -> {e}")
        time.sleep(1)
sys.exit(1)
PY

echo "[entrypoint] applying migrations..."
alembic upgrade head

echo "[entrypoint] starting api..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000