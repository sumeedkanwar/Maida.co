import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_db
from datetime import datetime
import mongomock


client = TestClient(app)


@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    db = client["moderation_db"]
    # Add admin token for testing
    db.tokens.insert_one({
        "token": "admin-token",
        "isAdmin": True,
        "createdAt": datetime.utcnow()
    })
    return db


@pytest.fixture(autouse=True)
def override_get_db(mock_db):
    def mock_get_db():
        return mock_db
    app.dependency_overrides[get_db] = mock_get_db
    yield
    app.dependency_overrides.clear()


def test_create_token_success():
    response = client.post(
        "/auth/tokens",
        headers={"Authorization": "Bearer admin-token"},
        json={"isAdmin": False}
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_create_token_unauthorized():
    response = client.post(
        "/auth/tokens",
        headers={"Authorization": "Bearer invalid-token"},
        json={"isAdmin": False}
    )
    assert response.status_code == 401


def test_list_tokens():
    response = client.get(
        "/auth/tokens",
        headers={"Authorization": "Bearer admin-token"}
    )
    assert response.status_code == 200
    tokens = response.json()
    assert isinstance(tokens, list)
    assert len(tokens) >= 1


def test_delete_token_success():
    # First create a token
    create_response = client.post(
        "/auth/tokens",
        headers={"Authorization": "Bearer admin-token"},
        json={"isAdmin": False}
    )
    token = create_response.json()["token"]

    # Then delete it
    response = client.delete(
        f"/auth/tokens/{token}",
        headers={"Authorization": "Bearer admin-token"}
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Token deleted"


def test_delete_token_not_found():
    response = client.delete(
        "/auth/tokens/nonexistent-token",
        headers={"Authorization": "Bearer admin-token"}
    )
    assert response.status_code == 404
