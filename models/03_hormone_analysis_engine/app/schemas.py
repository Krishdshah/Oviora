"""
Oviora Hormone Intelligence
Pydantic Schemas
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OCRWord(BaseModel):
    text: str
    confidence: float = Field(ge=0.0, le=1.0)


class Biomarker(BaseModel):
    canonical_name: str
    original_name: str
    value: float | None = None
    unit: str | None = None
    reference_range: str | None = None
    status: Literal["low", "normal", "borderline_low", "borderline_high", "high", "unknown"] = "unknown"
    category: str
    ocr_confidence: float = Field(ge=0.0, le=1.0)
    parser_confidence: float = Field(ge=0.0, le=1.0)
    notes: str | None = None


class PatientMetadata(BaseModel):
    patient_name: str | None = None
    age: int | None = None
    sex: str | None = None
    laboratory: str | None = None
    physician: str | None = None
    report_date: datetime | None = None


class ParsedReport(BaseModel):
    metadata: PatientMetadata = Field(default_factory=PatientMetadata)
    biomarkers: list[Biomarker] = Field(default_factory=list)
    missing_biomarkers: list[str] = Field(default_factory=list)
    overall_parser_confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class LLMInput(BaseModel):
    report: ParsedReport
    derived_metrics: dict[str, float | str] = Field(default_factory=dict)


class LLMOutput(BaseModel):
    executive_summary: str
    hormonal_assessment: str
    thyroid_assessment: str
    metabolic_assessment: str
    vitamin_assessment: str
    pcos_insights: str
    doctor_questions: list[str]
    follow_up_tests: list[str]
    limitations: list[str]


class AnalysisReport(BaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    parser_output: ParsedReport
    llm_output: LLMOutput | None = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    llm_provider: str = "rule_engine"


class APIResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None
