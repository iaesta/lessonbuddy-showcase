from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

EnglishLevel = Literal["Pre-A1", "A1", "A2", "B1", "B2", "C1"]
ReadingStage = Literal[
    "pre_reader",
    "word",
    "sentence",
    "short_paragraph",
    "short_story",
]
LatinWritingStage = Literal[
    "no_latin_writing",
    "trace_latin_letters",
    "copy_latin_letters",
    "copy_words",
    "write_words",
    "guided_sentences",
    "independent_sentences",
    "extended_writing",
]
PencilControl = Literal[
    "needs_large_spaces",
    "standard_marking",
    "age_appropriate",
]
SessionDuration = Literal[20, 30, 40, 45, 60, 75, 90, 120]
PrimarySkill = Literal["phonics", "vocabulary"]


class LessonFlowStage(BaseModel):
    start_minute: int = Field(ge=0)
    end_minute: int = Field(gt=0)
    stage: str = Field(min_length=1, max_length=80)
    teacher_action: str = Field(min_length=1, max_length=500)
    student_action: str = Field(min_length=1, max_length=500)
    materials: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_times(self) -> "LessonFlowStage":
        if self.end_minute <= self.start_minute:
            raise ValueError("Flow stage end time must be after its start time.")
        return self


class WorksheetRequest(BaseModel):
    topic: str = Field(default="Phonics: sh and ch", min_length=3, max_length=120)
    primary_skill: PrimarySkill = "phonics"
    target_words: list[str] = Field(
        default_factory=lambda: ["ship", "shoe", "chair", "cheese"]
    )
    age_min: int = Field(default=6, ge=2, le=18)
    age_max: int = Field(default=8, ge=2, le=18)
    level_label: EnglishLevel = "Pre-A1"
    reading_stage: ReadingStage = "pre_reader"
    latin_writing_stage: LatinWritingStage = "no_latin_writing"
    pencil_control: PencilControl = "age_appropriate"
    student_count: int = Field(default=8, ge=1, le=60)
    session_duration_minutes: SessionDuration = 40
    support_needs: list[str] = Field(default_factory=lambda: ["visual_support"])
    teacher_request: str = Field(
        default="Create a clear visual lesson with no ambiguous items.",
        min_length=10,
        max_length=800,
    )

    @model_validator(mode="after")
    def validate_request(self) -> "WorksheetRequest":
        if self.age_min > self.age_max:
            raise ValueError("Minimum age cannot be greater than maximum age.")

        cleaned_words: list[str] = []
        for raw_word in self.target_words:
            word = " ".join(str(raw_word).strip().lower().split())
            if not word:
                continue
            if len(word) > 24:
                raise ValueError("Each target word must be 24 characters or fewer.")
            if word not in cleaned_words:
                cleaned_words.append(word)

        if not 2 <= len(cleaned_words) <= 8:
            raise ValueError("Provide between 2 and 8 unique target words.")
        self.target_words = cleaned_words
        return self


class CompatibilityResult(BaseModel):
    allowed_response_modes: list[str]
    warnings: list[str] = Field(default_factory=list)
    blocking_issues: list[str] = Field(default_factory=list)


class QuickReview(BaseModel):
    title: str
    interpretation: str
    worksheet_count: int
    session_duration_minutes: int
    progression: list[str]
    visual_plan: str
    class_flow: list[LessonFlowStage]
    compatibility: CompatibilityResult


class Activity(BaseModel):
    instruction: str
    response_mode: str
    items: list[str]
    answer: str


class WorksheetPage(BaseModel):
    page_number: int = Field(ge=1)
    title: str
    estimated_minutes: int = Field(gt=0)
    activities: list[Activity]


class GeneratedPack(BaseModel):
    title: str
    learner_summary: str
    class_flow: list[LessonFlowStage]
    worksheets: list[WorksheetPage]
    answer_key: list[str]


class ValidationSummary(BaseModel):
    valid: bool
    checks: dict[str, bool]
    warnings: list[str] = Field(default_factory=list)


class GenerationResponse(BaseModel):
    engine: str
    document: GeneratedPack
    validation: ValidationSummary
