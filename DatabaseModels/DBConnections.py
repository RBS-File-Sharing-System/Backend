from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Format: postgresql+psycopg2://username:password@host:port/database
DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/erp"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


def get_connection():
    return engine.connect()


def release_connection(conn):
    if conn:
        conn.close()


def get_session():
    return SessionLocal()


def close_session(session):
    if session:
        session.close()
