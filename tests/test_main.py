"""Tests for the main FastAPI application."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test the root endpoint returns service information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "OS-APOW Orchestrator"
    assert data["version"] == "0.1.0"
    assert "docs" in data
    assert "health" in data


def test_health_endpoint(client: TestClient) -> None:
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "OS-APOW Orchestrator"


def test_readiness_endpoint(client: TestClient) -> None:
    """Test the readiness check endpoint."""
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["service"] == "OS-APOW Orchestrator"


def test_openapi_docs_available(client: TestClient) -> None:
    """Test that OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json_available(client: TestClient) -> None:
    """Test that OpenAPI JSON schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "OS-APOW Orchestrator"
