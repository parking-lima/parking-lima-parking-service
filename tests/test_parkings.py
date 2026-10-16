
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app
from app.models.parking import Parking
from app.models.parking_space import ParkingSpace


def test_get_parkings():
    db = MagicMock()
    db.scalars.return_value.all.return_value = [
        Parking(
            id=1,
            district_id=1,
            name="Parking Demo",
            address="Dirección de prueba",
        )
    ]

    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/parkings")

        assert response.status_code == 200
        assert response.json()[0]["name"] == "Parking Demo"
    finally:
        app.dependency_overrides.clear()


def test_get_parking_not_found():
    db = MagicMock()
    db.get.return_value = None

    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/parkings/999")

        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_get_parking_spaces():
    db = MagicMock()

    db.get.return_value = Parking(
        id=1,
        district_id=1,
        name="Parking Demo",
        address="Dirección de prueba",
    )

    db.scalars.return_value.all.return_value = [
        ParkingSpace(
            id=1,
            parking_id=1,
            code="A01",
            is_active=True,
        )
    ]

    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as client:
            response = client.get("/api/v1/parkings/1/spaces")

        assert response.status_code == 200
        assert response.json()[0]["code"] == "A01"
    finally:
        app.dependency_overrides.clear()


def test_get_parkings_by_district():
    db = MagicMock()
    db.scalars.return_value.all.return_value = [
        Parking(
            id=1,
            district_id=1,
            name="Parking Demo Miraflores",
            address="Dirección ficticia",
        )
    ]

    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/parkings?district_id=1"
            )

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["district_id"] == 1

        # Verifica que la consulta SQL incluya el filtro.
        statement = db.scalars.call_args.args[0]
        assert "parkings.district_id" in str(statement)
    finally:
        app.dependency_overrides.clear()


def test_get_parkings_invalid_district():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/parkings?district_id=-1"
        )

    assert response.status_code == 422


def test_get_parking_spaces_not_found():
    db = MagicMock()
    db.get.return_value = None

    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as client:
            response = client.get(
                "/api/v1/parkings/999/spaces"
            )

        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()
