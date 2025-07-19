# tests/conftest.py
import sys
from pathlib import Path

# Корректно добавляем корень проекта в sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 2) Теперь импортируем из src.app…
from src.app.main import app
from src.app.infrastructure.db.base import Base
from src.app.infrastructure.db.session import get_bd

# 3) In-memory SQLite
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
    )()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    # Переопределяем зависимость get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Сессия закрывается в фикстуре db_session

    app.dependency_overrides[get_bd] = override_get_db

    # Очищаем базу перед каждым тестом
    with db_session.begin():
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())
        db_session.commit()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

