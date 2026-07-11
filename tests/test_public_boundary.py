from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT / "app"


def application_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in APP_ROOT.rglob("*")
        if path.suffix in {".py", ".js", ".html"}
    ).casefold()


def test_public_app_contains_no_private_product_markers() -> None:
    source = application_source()
    forbidden_fragments = (
        "google.genai",
        "gemini_api_key",
        "generate_content(",
        "planning_bridge",
        "creative_bridge",
        "lessonbuddy_db_path",
        "worksheet-generation-v1.schema",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_browser_code_is_read_only() -> None:
    source = (APP_ROOT / "static" / "app.js").read_text(encoding="utf-8")
    assert "method: 'POST'" not in source
    assert 'method: "POST"' not in source
    assert "/api/generate" not in source
    assert "/api/quick-review" not in source


def test_private_generation_modules_are_not_public() -> None:
    assert not (APP_ROOT / "demo_generator.py").exists()
    assert not (APP_ROOT / "compatibility.py").exists()
