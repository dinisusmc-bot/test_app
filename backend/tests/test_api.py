"""
Tests for Command & Control API.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "docs" in data


def test_list_devices_empty():
    """Test listing devices when none exist."""
    response = client.get("/api/v1/devices")
    assert response.status_code == 200
    data = response.json()
    assert "devices" in data
    assert "total" in data


def test_create_device():
    """Test creating a new device."""
    device_data = {
        "name": "Test Drone",
        "device_type": "drone",
        "status": "online",
        "zone": "LA",
    }
    
    response = client.post("/api/v1/devices", json=device_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Drone"
    assert "id" in data


def test_list_locations():
    """Test listing locations."""
    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_events():
    """Test listing events."""
    response = client.get("/api/v1/events")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_commands():
    """Test listing commands."""
    response = client.get("/api/v1/commands")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
