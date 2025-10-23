import os

from fastapi import FastAPI
from prometheus_client import (CONTENT_TYPE_LATEST, REGISTRY,
                               CollectorRegistry, generate_latest,
                               multiprocess)
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from starlette.responses import Response

from src.api import users

app = FastAPI(title="DevOps Local Starter", version="0.1.0")
Instrumentator().instrument(app)


class Health(BaseModel):
    status: str
    env: str


@app.get("/", tags=["root"])
def root():
    return {"message": "Hello DevOps 👋", "docs": "/docs"}


@app.get("/health", response_model=Health, tags=["ops"])
def health():
    return Health(status="ok", env=os.getenv("APP_ENV", "dev"))


# Include users router
app.include_router(users.router)


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    """Expose Prometheus metrics.

    If PROMETHEUS_MULTIPROC_DIR is set, use the multiprocess registry,
    otherwise use the default process registry.
    """
    if os.getenv("PROMETHEUS_MULTIPROC_DIR"):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    data = generate_latest(registry)
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
