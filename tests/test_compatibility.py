from app.compatibility import evaluate_compatibility
from app.models import WorksheetRequest


def test_large_spacing_removes_long_written_modes() -> None:
    request = WorksheetRequest(
        topic="Animal vocabulary",
        primary_skill="vocabulary",
        target_words=["cat", "dog", "bird", "fish"],
        age_min=5,
        age_max=6,
        level_label="Pre-A1",
        reading_stage="word",
        latin_writing_stage="guided_sentences",
        pencil_control="needs_large_spaces",
        session_duration_minutes=20,
        teacher_request="Create an accessible activity with large visual targets.",
    )
    result = evaluate_compatibility(request)
    assert "guided_writing" not in result.allowed_response_modes
    assert any("generous spacing" in warning for warning in result.warnings)


def test_extended_writing_can_be_blocked_for_very_young_learners() -> None:
    request = WorksheetRequest(
        topic="My favourite toy",
        primary_skill="vocabulary",
        target_words=["ball", "doll", "car", "train"],
        age_min=3,
        age_max=4,
        level_label="Pre-A1",
        reading_stage="pre_reader",
        latin_writing_stage="extended_writing",
        pencil_control="age_appropriate",
        session_duration_minutes=20,
        teacher_request="Create a long independent writing task about favourite toys.",
    )
    result = evaluate_compatibility(request)
    assert result.blocking_issues
