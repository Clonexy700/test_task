# src/app/infrastructure/db/engine.py

from sqlalchemy import create_engine, event
from src.app.infrastructure.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True, 
    connect_args={"check_same_thread": False}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.close()
