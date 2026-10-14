
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.models.district import District


def override_get_db():
    db = MagicMock()

    db.scalars.return_value.all.return_value = [
        District(id=1, name="Miraflores"),
        District(id=2, name="San Isidro"),
    ]

    yield db


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "UP"


def test_get_districts():
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/districts")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2
        assert data[0]["name"] == "Miraflores"
        assert data[1]["name"] == "San Isidro"
    finally:
        app.dependency_overrides.clear()
