from __future__ import annotations

from math import ceil

from app.compatibility import evaluate_compatibility
from app.models import (
    Activity,
    GeneratedPack,
    GenerationResponse,
    LessonFlowStage,
    QuickReview,
    ValidationSummary,
    WorksheetPage,
    WorksheetRequest,
)


def _worksheet_count(duration: int) -> int:
    return min(4, max(1, ceil(duration / 30)))


def _flow(request: WorksheetRequest) -> list[LessonFlowStage]:
    duration = request.session_duration_minutes
    warm_up_end = max(4, round(duration * 0.15))
    presentation_end = max(warm_up_end + 4, round(duration * 0.35))
    guided_end = max(presentation_end + 5, round(duration * 0.60))
    worksheet_end = max(guided_end + 5, duration - max(4, round(duration * 0.15)))

    return [
        LessonFlowStage(
            start_minute=0,
            end_minute=warm_up_end,
            stage="Warm-up",
            teacher_action="Introduce the goal with gestures and oral modelling.",
            student_action="Listen, copy the gesture, and respond as a group.",
            materials=[],
        ),
        LessonFlowStage(
            start_minute=warm_up_end,
            end_minute=presentation_end,
            stage="Presentation",
            teacher_action="Model the target language with clear examples and visual support.",
            student_action="Watch, listen, repeat, and identify examples.",
            materials=["picture cards", "board"],
        ),
        LessonFlowStage(
            start_minute=presentation_end,
            end_minute=guided_end,
            stage="Guided practice",
            teacher_action="Run a supported sorting or matching task before independent work.",
            student_action="Sort, point, move, and repeat with teacher support.",
            materials=["picture cards"],
        ),
        LessonFlowStage(
            start_minute=guided_end,
            end_minute=worksheet_end,
            stage="Student pages",
            teacher_action="Model the first item and use only compatible response modes.",
            student_action="Complete the worksheet pages at the selected level.",
            materials=["printed worksheets", "pencils or stickers"],
        ),
        LessonFlowStage(
            start_minute=worksheet_end,
            end_minute=duration,
            stage="Review and close",
            teacher_action="Check one final example and revisit any confusion.",
            student_action="Give a final oral, pointing, or written response.",
            materials=[],
        ),
    ]


def build_quick_review(request: WorksheetRequest) -> QuickReview:
    compatibility = evaluate_compatibility(request)
    count = _worksheet_count(request.session_duration_minutes)
    progression = [
        "recognise the target",
        "compare or sort examples",
        "complete a supported worksheet task",
    ]
    if count >= 3:
        progression.append("apply the target in a short review task")

    return QuickReview(
        title=request.topic,
        interpretation=(
            f"A {request.session_duration_minutes}-minute {request.primary_skill} lesson for "
            f"ages {request.age_min}–{request.age_max}, level {request.level_label}."
        ),
        worksheet_count=count,
        session_duration_minutes=request.session_duration_minutes,
        progression=progression,
        visual_plan="Use simple reusable picture prompts and avoid decorative clutter.",
        class_flow=_flow(request),
        compatibility=compatibility,
    )


def _activity_for_page(request: WorksheetRequest, page_number: int, mode: str) -> Activity:
    words = request.target_words
    if page_number == 1:
        return Activity(
            instruction="Listen and choose the matching picture.",
            response_mode=mode,
            items=words,
            answer=", ".join(words),
        )
    if page_number == 2:
        return Activity(
            instruction="Sort the examples into two teacher-labelled groups.",
            response_mode=mode,
            items=words,
            answer="Accept the teacher-modelled grouping for the selected target.",
        )
    if page_number == 3:
        return Activity(
            instruction="Complete the supported review using the same target language.",
            response_mode=mode,
            items=list(reversed(words)),
            answer=", ".join(reversed(words)),
        )
    return Activity(
        instruction="Choose two examples and explain or demonstrate the difference.",
        response_mode=mode,
        items=words[:4],
        answer="Responses should match the lesson target and teacher model.",
    )


def validate_pack(pack: GeneratedPack, duration: int) -> ValidationSummary:
    checks = {
        "flow_starts_at_zero": bool(pack.class_flow) and pack.class_flow[0].start_minute == 0,
        "flow_ends_at_duration": bool(pack.class_flow) and pack.class_flow[-1].end_minute == duration,
        "flow_is_contiguous": all(
            current.end_minute == following.start_minute
            for current, following in zip(pack.class_flow, pack.class_flow[1:])
        ),
        "has_worksheets": bool(pack.worksheets),
        "all_pages_have_activities": all(page.activities for page in pack.worksheets),
        "answers_cover_pages": len(pack.answer_key) == len(pack.worksheets),
    }
    warnings: list[str] = []
    if sum(page.estimated_minutes for page in pack.worksheets) > duration:
        warnings.append("Worksheet time exceeds the full session duration.")
    return ValidationSummary(valid=all(checks.values()), checks=checks, warnings=warnings)


def build_demo_pack(request: WorksheetRequest) -> GenerationResponse:
    review = build_quick_review(request)
    if review.compatibility.blocking_issues:
        raise ValueError("; ".join(review.compatibility.blocking_issues))

    mode = review.compatibility.allowed_response_modes[0]
    page_minutes = max(5, round(request.session_duration_minutes * 0.30 / review.worksheet_count))
    pages: list[WorksheetPage] = []
    answers: list[str] = []

    for page_number in range(1, review.worksheet_count + 1):
        activity = _activity_for_page(request, page_number, mode)
        pages.append(
            WorksheetPage(
                page_number=page_number,
                title=f"{request.topic} — Page {page_number}",
                estimated_minutes=page_minutes,
                activities=[activity],
            )
        )
        answers.append(f"Page {page_number}: {activity.answer}")

    pack = GeneratedPack(
        title=request.topic,
        learner_summary=(
            f"Ages {request.age_min}–{request.age_max}; {request.level_label}; "
            f"reading={request.reading_stage}; writing={request.latin_writing_stage}."
        ),
        class_flow=review.class_flow,
        worksheets=pages,
        answer_key=answers,
    )
    return GenerationResponse(
        engine="deterministic-portfolio-demo",
        document=pack,
        validation=validate_pack(pack, request.session_duration_minutes),
    )
