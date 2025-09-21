import os

from fastapi.testclient import TestClient

from src.api.main import app

# مطمئن می‌شویم APP_ENV یک مقدار دارد
os.environ.setdefault("APP_ENV", "dev")

client = TestClient(app)


def test_health_status_ok():
    """سرویس باید روی /health وضعیت ok برگرداند"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["env"] == "dev"
