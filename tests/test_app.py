from copy import deepcopy

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def payload() -> dict:
    return {
        "topic": "Animals at the zoo",
        "primary_skill": "vocabulary",
        "target_words": ["lion", "monkey", "elephant", "giraffe"],
        "age_min": 6,
        "age_max": 8,
        "level_label": "A1",
        "reading_stage": "word",
        "latin_writing_stage": "write_words",
        "pencil_control": "age_appropriate",
        "student_count": 8,
        "session_duration_minutes": 40,
        "support_needs": ["visual_support"],
        "teacher_request": "",
    }


def test_health_reports_public_demo_boundary() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["appVersion"] == "1.1.0-showcase"
    assert data["externalAIConfigured"] is False
    assert "production prompts" in data["publicBoundary"]


def test_quick_review_has_stable_demo_stage_ids() -> None:
    response = client.post("/api/quick-review", json=payload())
    assert response.status_code == 200
    data = response.json()
    stage_ids = [stage["stage_id"] for stage in data["class_flow"]]
    assert len(stage_ids) == len(set(stage_ids))
    assert all(stage_id.startswith("demo_stage_") for stage_id in stage_ids)
    assert sum(stage["stage"] == "Student pages" for stage in data["class_flow"]) == 1
    assert data["worksheet_plan"]


def test_optional_teacher_note_can_be_blank() -> None:
    request = payload()
    request["teacher_request"] = ""
    response = client.post("/api/quick-review", json=request)
    assert response.status_code == 200


def test_demo_generation_uses_multiple_activity_types() -> None:
    response = client.post("/api/generate", json=payload())
    assert response.status_code == 200
    data = response.json()
    assert data["engine"] == "deterministic-portfolio-demo-v2"
    assert data["validation"]["valid"] is True
    assert data["validation"]["checks"]["uses_more_than_one_activity_type"] is True
    assert all(len(page["activities"]) == 3 for page in data["document"]["worksheets"])


def test_approved_flow_can_be_reordered_and_edited() -> None:
    review = client.post("/api/quick-review", json=payload()).json()
    flow = deepcopy(review["class_flow"])

    presentation = flow.pop(1)
    presentation["teacher_action"] = "Use a different public demo example."
    flow.insert(2, presentation)

    cursor = 0
    for stage in flow:
        minutes = stage["end_minute"] - stage["start_minute"]
        stage["start_minute"] = cursor
        stage["end_minute"] = cursor + minutes
        cursor += minutes

    difference = payload()["session_duration_minutes"] - cursor
    flow[-1]["end_minute"] += difference

    response = client.post(
        "/api/generate-approved",
        json={"request": payload(), "approved_flow": flow},
    )
    assert response.status_code == 200
    generated = response.json()["document"]["class_flow"]
    assert generated[2]["teacher_action"] == "Use a different public demo example."


def test_invalid_approved_flow_is_rejected() -> None:
    review = client.post("/api/quick-review", json=payload()).json()
    flow = [
        stage
        for stage in review["class_flow"]
        if stage["stage"] != "Student pages"
    ]
    response = client.post(
        "/api/generate-approved",
        json={"request": payload(), "approved_flow": flow},
    )
    assert response.status_code == 422
    assert "exactly one Student pages" in response.json()["detail"]


def test_invalid_age_range_is_rejected() -> None:
    invalid = payload()
    invalid["age_min"] = 10
    invalid["age_max"] = 6
    response = client.post("/api/quick-review", json=invalid)
    assert response.status_code == 422
