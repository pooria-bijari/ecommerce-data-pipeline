import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


def get_database_url():
    """
    Return the PostgreSQL database URL from environment variables.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set.")

    return database_url


def get_engine():
    """
    Create and return a SQLAlchemy database engine.
    """
    return create_engine(get_database_url())