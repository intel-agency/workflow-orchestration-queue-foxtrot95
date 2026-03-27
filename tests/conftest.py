"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    from orchestrator.main import app

    return TestClient(app)


@pytest.fixture
def mock_github_token(monkeypatch: pytest.MonkeyPatch) -> str:
    """Set a mock GitHub token for testing."""
    token = "FAKE-GITHUB-TOKEN-FOR-TESTING-00000000"
    monkeypatch.setenv("GITHUB_TOKEN", token)
    return token


@pytest.fixture
def mock_webhook_secret(monkeypatch: pytest.MonkeyPatch) -> str:
    """Set a mock webhook secret for testing."""
    secret = "FAKE-WEBHOOK-SECRET-FOR-TESTING-00000000"
    monkeypatch.setenv("WEBHOOK_SECRET", secret)
    return secret
