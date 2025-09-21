#!/usr/bin/env bash
set -euo pipefail
echo "[deploy] pulling latest images..."
docker-compose pull
echo "[deploy] restarting stack..."
docker-compose up -d
echo "[deploy] done. Health:"
curl -sS http://127.0.0.1:8080/health || true