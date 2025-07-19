from sqlalchemy.orm import sessionmaker

from src.app.infrastructure.db.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
