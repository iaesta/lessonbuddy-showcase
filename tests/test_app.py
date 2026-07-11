from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_is_read_only_portfolio_mode() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["appVersion"] == "1.1.0-portfolio"
    assert data["mode"] == "portfolio-only"
    assert data["writeOperations"] is False


def test_project_snapshot_contains_public_metadata_only() -> None:
    response = client.get("/api/project-snapshot")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "LessonBuddy"
    assert data["edition"] == "Sanitised portfolio showcase"
    assert data["engineering_highlights"]
    assert data["qa_principles"]
    assert data["private_by_design"]


def test_public_api_has_no_post_routes() -> None:
    schema = client.get("/openapi.json").json()
    public_paths = {
        path: methods
        for path, methods in schema["paths"].items()
        if path.startswith("/api/")
    }
    assert public_paths
    assert all("post" not in methods for methods in public_paths.values())
