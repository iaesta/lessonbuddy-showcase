from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_app_contains_no_provider_or_production_markers() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "app").rglob("*")
        if path.suffix in {".py", ".js", ".html"}
    ).casefold()

    forbidden_fragments = (
        "google.genai",
        "gemini_api_key",
        "generate_content(",
        "planning_bridge",
        "creative_bridge",
        "lessonbuddy_db_path",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_student_renderer_does_not_show_internal_sections() -> None:
    source = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")
    student_renderer = source.split(
        "function renderStudentActivity",
        1,
    )[1].split(
        "function renderStudentView",
        1,
    )[0]

    assert "activity.section" not in student_renderer
    assert "Core practice" not in student_renderer
    assert "finish later" not in student_renderer
