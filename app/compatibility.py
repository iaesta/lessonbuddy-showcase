from __future__ import annotations

from app.models import CompatibilityResult, WorksheetRequest


def evaluate_compatibility(request: WorksheetRequest) -> CompatibilityResult:
    modes: list[str] = []
    warnings: list[str] = []
    blocking: list[str] = []

    if request.reading_stage == "pre_reader":
        modes.extend(["listen_and_point", "picture_choice", "oral_repeat"])
        warnings.append("Do not require independent English word reading.")
    else:
        modes.extend(["read_and_match", "short_written_response"])

    if request.latin_writing_stage == "no_latin_writing":
        modes = [mode for mode in modes if mode != "short_written_response"]
        modes.extend(["circle", "sticker_or_mark"])
        warnings.append("Do not require Latin-letter writing.")
    elif request.latin_writing_stage in {"trace_latin_letters", "copy_latin_letters"}:
        modes.extend(["trace", "copy_letter"])
    elif request.latin_writing_stage in {"copy_words", "write_words"}:
        modes.append("write_word")
    else:
        modes.append("guided_writing")

    if request.pencil_control == "needs_large_spaces":
        warnings.append("Use large targets, few items per page, and generous spacing.")
        modes = [mode for mode in modes if mode not in {"guided_writing", "short_written_response"}]

    if request.age_max <= 4 and request.latin_writing_stage in {
        "independent_sentences",
        "extended_writing",
    }:
        blocking.append("Extended independent writing is incompatible with the selected age range.")

    if request.primary_skill == "phonics" and request.reading_stage == "pre_reader":
        warnings.append("Present target words orally; pictures carry the task meaning.")

    unique_modes = list(dict.fromkeys(modes))
    return CompatibilityResult(
        allowed_response_modes=unique_modes,
        warnings=warnings,
        blocking_issues=blocking,
    )
