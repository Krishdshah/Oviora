"""
Oviora Hormone Intelligence
API Tests
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == settings.APP_NAME


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["live"] is True


def test_ready():
    response = client.get("/health/ready")
    assert response.status_code in (200, 503)
    assert "checks" in response.json()


def test_upload_invalid_extension():
    response = client.post(
        "/upload",
        files={
            "file": (
                "sample.exe",
                b"invalid",
                "application/octet-stream",
            )
        },
    )
    assert response.status_code == 400


def test_reports_listing():
    response = client.get("/reports")
    assert response.status_code == 200
    assert "reports" in response.json()


@pytest.mark.parametrize("fmt", ["json", "markdown", "html", "pdf"])
def test_missing_report_download(fmt):
    response = client.get(f"/reports/does_not_exist/{fmt}")
    assert response.status_code == 404


def test_delete_missing_report():
    response = client.delete("/reports/does_not_exist")
    assert response.status_code == 404
