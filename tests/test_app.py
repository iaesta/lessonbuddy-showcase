from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def payload() -> dict:
    return {
        "topic": "Phonics: sh and ch",
        "primary_skill": "phonics",
        "target_words": ["ship", "shoe", "chair", "cheese"],
        "age_min": 6,
        "age_max": 8,
        "level_label": "Pre-A1",
        "reading_stage": "pre_reader",
        "latin_writing_stage": "no_latin_writing",
        "pencil_control": "age_appropriate",
        "student_count": 8,
        "session_duration_minutes": 40,
        "support_needs": ["visual_support"],
        "teacher_request": "Create a visual sound-discrimination lesson with no independent reading.",
    }


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["externalAIConfigured"] is False


def test_quick_review_respects_pre_reader_profile() -> None:
    response = client.post("/api/quick-review", json=payload())
    assert response.status_code == 200
    data = response.json()
    assert "picture_choice" in data["compatibility"]["allowed_response_modes"]
    assert any("independent English word reading" in warning for warning in data["compatibility"]["warnings"])


def test_demo_generation_is_valid() -> None:
    response = client.post("/api/generate", json=payload())
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "deterministic-portfolio-demo"
    assert data["validation"]["valid"] is True
    assert len(data["document"]["worksheets"]) == 2
    assert len(data["document"]["answer_key"]) == 2


def test_invalid_age_range_is_rejected() -> None:
    invalid = payload()
    invalid["age_min"] = 10
    invalid["age_max"] = 6
    response = client.post("/api/quick-review", json=invalid)
    assert response.status_code == 422
