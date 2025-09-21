import os

from fastapi import FastAPI
from pydantic import BaseModel
from src.api import users

app = FastAPI(title="DevOps Local Starter", version="0.1.0")

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
