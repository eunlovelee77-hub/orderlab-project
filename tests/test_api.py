import pytest
from fastapi.testclient import TestClient

from orderlab.api import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_create_and_get(client):
    response = client.post(
        "/orders",
        json={"price": 10000, "quantity": 2},
    )

    assert response.status_code == 201
    assert response.json() == {"id": 1, "subtotal": 20000}

    result = client.get("/orders/1")

    assert result.status_code == 200
    assert result.json() == {"id": 1, "subtotal": 20000}


def test_invalid_quantity(client):
    response = client.post(
        "/orders",
        json={"price": 100, "quantity": 0},
    )

    assert response.status_code == 422


def test_not_found(client):
    response = client.get("/orders/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
