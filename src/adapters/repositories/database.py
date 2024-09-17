import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.infrastructure.utils.extensions import config

options = {
    "pool_size": 20,
    "max_overflow": 10,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}
engine = create_engine(
    config.get("SQLALCHEMY_DATABASE_URI"),
)
env = os.environ.get("JOUNCE_ENV").lower()
if env != "test":
    engine = create_engine(
        config.get("SQLALCHEMY_DATABASE_URI"),
        **options
    )


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        return session
    finally:
        session.close()
