import pytest

from app import app, APP_VERSION


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    data = response.get_json()
    assert response.status_code == 200
    assert data["status"] == "wrong"
    assert data["application"] == "student-ml-api"
    assert data["version"] == APP_VERSION


def test_predict_success(client):
    response = client.post("/predict", json={"value": 10})
    data = response.get_json()
    assert response.status_code == 200
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_predict_missing_input(client):
    response = client.post("/predict", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_invalid_input(client):
    response = client.post("/predict", json={"value": "ten"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_no_json_body(client):
    response = client.post("/predict", data="not json", content_type="text/plain")
    assert response.status_code == 400
