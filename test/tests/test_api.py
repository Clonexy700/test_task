import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from src.app.main import app
from src.app.infrastructure.db.base import Base
from src.app.infrastructure.db.session import engine, SessionLocal

@pytest.fixture(scope="session")
def setup_bd():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)

def test_shift_task_create_and_get(client):
    payload = [{
        "is_closed": False,
        "task_description": "Test",
        "work_center": "WC1",
        "shift": "morning",
        "team_name": "TeamA",
        "batch_id": 1,
        "batch_date": "2025-06-10",
        "nomenclature": "Item",
        "ekn_code": 100,
        "rc_id": 200,
        "shift_start": "2025-06-10T08:00:00",
        "shift_end": "2025-06-10T16:00:00"
    }]
    r = client.post("/api/v1/shift-tasks/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert isinstance(data, list) and len(data) == 1
    task = data[0]
    assert task["batch_id"] == 1
    tid = task["id"]

    r2 = client.get(f"/api/v1/shift-tasks/{tid}")
    assert r2.status_code == 200, r2.text
    assert r2.json()["id"] == tid

def test_product_create_and_aggregate(client):
    shift = [{
        "is_closed": False,
        "task_description": "Batch",
        "work_center": "WC",
        "shift": "eve",
        "team_name": "Team",
        "batch_id": 10,
        "batch_date": "2025-06-20",
        "nomenclature": "X",
        "ekn_code": 1,
        "rc_id": 1,
        "shift_start": "2025-06-20T08:00:00",
        "shift_end": "2025-06-20T16:00:00"
    }]
    r = client.post("/api/v1/shift-tasks/", json=shift)
    assert r.status_code == 201, r.text
    shift_task = r.json()[0]
    batch_id = shift_task["batch_id"]
    shift_task_id = shift_task["id"]

    unique_code = f"UC1-{uuid4().hex[:6]}"
    prod = [{
        "unique_code": unique_code,
        "batch_id": batch_id,
        "batch_date": "2025-06-20"
    }]
    r2 = client.post("/api/v1/products/", json=prod)
    assert r2.status_code == 201, r2.text
    product = r2.json()[0]
    pid = product["id"]

    r3 = client.post(f"/api/v1/products/aggregate/", json={
        "batch_pk": batch_id,
        "unique_code": unique_code
    })
    assert r3.status_code == 200, r3.text
    assert r3.json()["unique_code"] == unique_code

    r4 = client.post(f"/api/v1/products/aggregate/", json={
        "batch_pk": batch_id,
        "unique_code": unique_code
    })
    assert r4.status_code == 400
    assert "unique code already used" in r4.json()["detail"]

    r5 = client.post(f"/api/v1/products/aggregate/", json={
        "batch_pk": 99999,  # не тот batch_id
        "unique_code": unique_code
    })
    assert r5.status_code == 400
    assert "unique code is attached to another batch" in r5.json()["detail"].lower()

    r6 = client.post(f"/api/v1/products/aggregate/", json={
        "batch_pk": batch_id,
        "unique_code": "nonexistent-code"
    })
    assert r6.status_code == 404
    assert "Product not found" in r6.json()["detail"]