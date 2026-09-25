import pytest
from fastapi.testclient import TestClient
from universal_ai.api.app import create_app

@pytest.fixture
def client(): return TestClient(create_app())

def test_health(client):
    assert client.get("/health").status_code == 200

def test_ready(client):
    assert client.get("/ready").status_code == 200

def test_get_modules(client):
    res = client.get("/v1/modules")
    assert res.status_code == 200
    assert any(m["id"] == "echo_module" for m in res.json())
def test_request_success(client):
    headers = {"X-Request-ID": "req-123", "X-Tenant-ID": "tenant-1", "X-Subject-ID": "user-1"}
    res = client.post("/v1/request", json={"message": "hello", "target_module": "echo_module"}, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["request_id"] == "req-123"
    assert data["payload"]["echo"] == "hello"
    assert data["provenance"]["generated"] is False

def test_request_missing_headers(client):
    res = client.post("/v1/request", json={"message": "hello"})
    assert res.status_code == 400
    assert "Missing X-Request-ID" in res.json()["detail"]

def test_request_unknown_module(client):
    headers = {"X-Request-ID": "req-456", "X-Tenant-ID": "tenant-1"}
    res = client.post("/v1/request", json={"message": "hello", "target_module": "fake"}, headers=headers)
    assert res.status_code == 400
    assert "ROUTING_ERROR" in str(res.json()["detail"])