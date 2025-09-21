from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import database_url

# Global Engine based on environment-driven settings
ENGINE = create_engine(database_url(), future=True, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False, future=True)

# Declarative Base for models
Base = declarative_base()

# Optional: FastAPI dependency helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
