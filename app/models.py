from __future__ import annotations

from pydantic import BaseModel


class ProjectSnapshot(BaseModel):
    name: str
    edition: str
    status: str
    summary: str
    engineering_highlights: list[str]
    qa_principles: list[str]
    private_by_design: list[str]
