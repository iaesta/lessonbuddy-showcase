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
    WorksheetPlanPage,
    WorksheetRequest,
)


def _worksheet_count(duration: int) -> int:
    return min(3, max(1, ceil(duration / 30)))


def _stage(
    stage_id: str,
    start: int,
    end: int,
    title: str,
    teacher_action: str,
    student_action: str,
    materials: list[str] | None = None,
) -> LessonFlowStage:
    return LessonFlowStage(
        stage_id=stage_id,
        start_minute=start,
        end_minute=end,
        stage=title,
        teacher_action=teacher_action,
        student_action=student_action,
        materials=materials or [],
    )


def _flow(request: WorksheetRequest) -> list[LessonFlowStage]:
    duration = request.session_duration_minutes
    warm = max(2, round(duration * 0.15))
    presentation = max(3, round(duration * 0.20))
    guided = max(3, round(duration * 0.20))
    review = max(2, round(duration * 0.15))
    student_pages = duration - warm - presentation - guided - review

    if student_pages < 4:
        student_pages = 4
        guided = max(2, duration - warm - presentation - review - student_pages)

    marks = [0]
    for minutes in [warm, presentation, guided, student_pages, review]:
        marks.append(marks[-1] + minutes)
    marks[-1] = duration

    return [
        _stage(
            "demo_stage_warm_up",
            marks[0],
            marks[1],
            "Warm-up",
            "Introduce the topic with gestures and one clear oral model.",
            "Listen, copy the gesture, and respond together.",
        ),
        _stage(
            "demo_stage_presentation",
            marks[1],
            marks[2],
            "Presentation",
            "Model the target language with simple visual support.",
            "Watch, listen, repeat, and identify examples.",
            ["picture cards", "board"],
        ),
        _stage(
            "demo_stage_guided_practice",
            marks[2],
            marks[3],
            "Guided practice",
            "Run a supported sorting or matching task.",
            "Sort, point, move, and repeat with teacher support.",
            ["picture cards"],
        ),
        _stage(
            "demo_stage_student_pages",
            marks[3],
            marks[4],
            "Student pages",
            "Model the first item, then release learners gradually.",
            "Complete the worksheet tasks at the selected reading and writing level.",
            ["printed worksheets", "pencils"],
        ),
        _stage(
            "demo_stage_review",
            marks[4],
            marks[5],
            "Review and close",
            "Check one final example and revisit any confusion.",
            "Give a final oral, pointing, or written response.",
        ),
    ]


def _activity_types(request: WorksheetRequest) -> list[str]:
    if request.reading_stage == "pre_reader":
        return ["picture_choice", "sort", "picture_choice"]
    if request.latin_writing_stage in {
        "no_latin_writing",
        "trace_latin_letters",
        "copy_latin_letters",
    }:
        return ["picture_choice", "sort", "complete_word"]
    return ["picture_choice", "complete_word", "write_word"]


def _worksheet_plan(
    request: WorksheetRequest,
    count: int,
) -> list[WorksheetPlanPage]:
    activity_types = _activity_types(request)
    pages: list[WorksheetPlanPage] = []
    for page_number in range(1, count + 1):
        pages.append(
            WorksheetPlanPage(
                page_number=page_number,
                title=f"{request.topic} — Practice {page_number}",
                purpose=(
                    "Recognise the target, complete one supported step, "
                    "and finish with a short review."
                ),
                planned_activities=activity_types,
            )
        )
    return pages


def build_quick_review(request: WorksheetRequest) -> QuickReview:
    compatibility = evaluate_compatibility(request)
    count = _worksheet_count(request.session_duration_minutes)
    goal = (
        f"Learners will recognise and use {len(request.target_words)} "
        f"target item{'s' if len(request.target_words) != 1 else ''} "
        f"through age-appropriate {request.primary_skill} practice."
    )

    return QuickReview(
        title=request.topic,
        lesson_goal=goal,
        interpretation=(
            f"A {request.session_duration_minutes}-minute {request.primary_skill} lesson "
            f"for ages {request.age_min}–{request.age_max}, level {request.level_label}."
        ),
        worksheet_count=count,
        session_duration_minutes=request.session_duration_minutes,
        progression=[
            "recognise the target",
            "compare or complete with support",
            "retrieve the target in a short review",
        ],
        visual_plan=(
            "Use a compact, readable layout with visual cues and no decorative clutter."
        ),
        class_flow=_flow(request),
        worksheet_plan=_worksheet_plan(request, count),
        compatibility=compatibility,
    )


def _mask_word(word: str) -> str:
    for index, character in enumerate(word):
        if character in "aeiou":
            return f"{word[:index]}_{word[index + 1:]}"
    return f"{word[:-1]}_" if len(word) > 1 else "_"


def _activities_for_page(
    request: WorksheetRequest,
    page_number: int,
    mode: str,
) -> list[Activity]:
    words = request.target_words
    kinds = _activity_types(request)
    activities: list[Activity] = []

    instructions = {
        "picture_choice": "Look at each picture and choose the matching word.",
        "sort": "Sort the words into two teacher-labelled groups.",
        "complete_word": "Complete each word using the visual clue.",
        "write_word": "Write each target word beside its visual clue.",
    }

    for index, kind in enumerate(kinds, start=1):
        section = "extra" if index == len(kinds) else "core"
        items = words if index != 2 else list(reversed(words))
        answer = (
            ", ".join(_mask_word(word) for word in items)
            if kind == "complete_word"
            else ", ".join(items)
        )
        activities.append(
            Activity(
                activity_id=f"demo_activity_{page_number}_{index}",
                activity_type=kind,
                section=section,
                instruction=instructions[kind],
                response_mode=mode,
                items=items,
                answer=answer,
            )
        )
    return activities


def validate_approved_flow(
    flow: list[LessonFlowStage],
    duration: int,
) -> None:
    if not flow:
        raise ValueError("The approved flow cannot be empty.")
    if sum(stage.stage == "Student pages" for stage in flow) != 1:
        raise ValueError("The approved flow must contain exactly one Student pages stage.")
    if flow[0].start_minute != 0 or flow[-1].end_minute != duration:
        raise ValueError("The approved flow must cover the complete lesson duration.")
    if any(
        current.end_minute != following.start_minute
        for current, following in zip(flow, flow[1:])
    ):
        raise ValueError("The approved flow must be contiguous.")
    stage_ids = [stage.stage_id for stage in flow]
    if len(stage_ids) != len(set(stage_ids)):
        raise ValueError("Every approved flow stage must have a unique stage_id.")


def validate_pack(pack: GeneratedPack, duration: int) -> ValidationSummary:
    activities = [
        activity
        for page in pack.worksheets
        for activity in page.activities
    ]
    checks = {
        "flow_starts_at_zero": bool(pack.class_flow)
        and pack.class_flow[0].start_minute == 0,
        "flow_ends_at_duration": bool(pack.class_flow)
        and pack.class_flow[-1].end_minute == duration,
        "flow_is_contiguous": all(
            current.end_minute == following.start_minute
            for current, following in zip(pack.class_flow, pack.class_flow[1:])
        ),
        "stage_ids_are_unique": len({stage.stage_id for stage in pack.class_flow})
        == len(pack.class_flow),
        "has_one_student_pages_stage": sum(
            stage.stage == "Student pages" for stage in pack.class_flow
        )
        == 1,
        "has_worksheets": bool(pack.worksheets),
        "all_pages_have_activities": all(page.activities for page in pack.worksheets),
        "activity_ids_are_unique": len({activity.activity_id for activity in activities})
        == len(activities),
        "uses_more_than_one_activity_type": len(
            {activity.activity_type for activity in activities}
        )
        >= 2,
        "answers_cover_pages": len(pack.answer_key) == len(pack.worksheets),
    }
    warnings: list[str] = []
    if sum(page.practice_minutes for page in pack.worksheets) > duration:
        warnings.append("Worksheet time exceeds the full session duration.")
    return ValidationSummary(
        valid=all(checks.values()),
        checks=checks,
        warnings=warnings,
    )


def build_demo_pack(
    request: WorksheetRequest,
    approved_flow: list[LessonFlowStage] | None = None,
) -> GenerationResponse:
    review = build_quick_review(request)
    if review.compatibility.blocking_issues:
        raise ValueError("; ".join(review.compatibility.blocking_issues))

    flow = approved_flow or review.class_flow
    validate_approved_flow(flow, request.session_duration_minutes)

    mode = review.compatibility.allowed_response_modes[0]
    page_minutes = max(
        5,
        round(
            request.session_duration_minutes
            * 0.40
            / review.worksheet_count
        ),
    )
    pages: list[WorksheetPage] = []
    answers: list[str] = []

    for page_plan in review.worksheet_plan:
        activities = _activities_for_page(
            request,
            page_plan.page_number,
            mode,
        )
        pages.append(
            WorksheetPage(
                page_number=page_plan.page_number,
                title=page_plan.title,
                purpose=page_plan.purpose,
                practice_minutes=page_minutes,
                activities=activities,
            )
        )
        answers.append(
            f"Page {page_plan.page_number}: "
            + " | ".join(activity.answer for activity in activities)
        )

    pack = GeneratedPack(
        title=request.topic,
        learner_summary=(
            f"Ages {request.age_min}–{request.age_max}; {request.level_label}; "
            f"reading={request.reading_stage}; writing={request.latin_writing_stage}."
        ),
        class_flow=flow,
        worksheets=pages,
        answer_key=answers,
    )
    return GenerationResponse(
        engine="deterministic-portfolio-demo-v2",
        document=pack,
        validation=validate_pack(
            pack,
            request.session_duration_minutes,
        ),
    )
