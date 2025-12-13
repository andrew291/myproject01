from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from storage.models import Base


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    future=True,
)


# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def init_db():
    """
    Create all tables in the database.
    This uses the models defined in storage/models.py
    """
    Base.metadata.create_all(bind=engine)
