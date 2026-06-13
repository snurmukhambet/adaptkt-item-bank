from __future__ import annotations
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime
import json

from pydantic import BaseModel, validator, root_validator

ExerciseType = Literal["cloze", "multiple_choice", "error_correction", "word_formation"]
CefrLevel = Literal["A1", "A2", "A2+", "B1", "B1+", "B2"]

_taxonomy_cache: dict | None = None


def _load_taxonomy(path: str = "taxonomy_v2.json") -> dict:
    global _taxonomy_cache
    if _taxonomy_cache is None:
        with open(path) as f:
            _taxonomy_cache = json.load(f)
    return _taxonomy_cache


def get_valid_skill_ids(taxonomy_path: str = "taxonomy_v2.json") -> set:
    tax = _load_taxonomy(taxonomy_path)
    ids = {s["id"] for s in tax["grammar_skills"]}
    ids |= {s["id"] for s in tax["vocabulary_domains"]}
    return ids


class ExerciseContent(BaseModel):
    instruction: str
    prompt: str
    correct_answer: str
    distractors: Optional[List[str]] = None
    distractor_rationale: Optional[List[str]] = None
    error_sentence: Optional[str] = None
    corrected_sentence: Optional[str] = None
    base_word: Optional[str] = None

    @validator("distractors")
    @classmethod
    def validate_distractors_count(cls, v):
        if v is not None and len(v) != 3:
            raise ValueError(f"distractors must have exactly 3 items, got {len(v)}")
        return v


class DifficultyFeatures(BaseModel):
    gse_target: int
    sentence_length_tokens: Optional[int] = None
    target_form_complexity: Optional[str] = None


class AutoChecks(BaseModel):
    schema_valid: bool = True
    skill_match: Optional[bool] = None
    ambiguity_check: Optional[bool] = None
    duplicate_check: Optional[bool] = None


class Provenance(BaseModel):
    generator_model: str
    generation_timestamp: str
    template_id: str
    batch_id: str
    auto_checks: AutoChecks = AutoChecks()


class Exercise(BaseModel):
    id: str
    skill_ids: List[str]
    exercise_type: ExerciseType
    cefr_level: CefrLevel
    gse_target: int

    content: ExerciseContent
    difficulty_features: DifficultyFeatures
    provenance: Provenance

    @root_validator
    @classmethod
    def validate_type_fields(cls, values):
        ex_type = values.get("exercise_type")
        content = values.get("content")
        if content is None:
            return values
        if ex_type == "error_correction":
            if not content.error_sentence or not content.corrected_sentence:
                raise ValueError("error_correction requires error_sentence and corrected_sentence")
        if ex_type == "word_formation":
            if not content.base_word:
                raise ValueError("word_formation requires base_word")
        if ex_type in ("multiple_choice", "cloze"):
            if not content.distractors:
                raise ValueError(f"{ex_type} requires distractors")
        return values

    @root_validator
    @classmethod
    def validate_no_distractor_collision(cls, values):
        content = values.get("content")
        if content is None:
            return values
        if content.distractors:
            answer_lower = (content.correct_answer or "").strip().lower()
            for d in content.distractors:
                if d.strip().lower() == answer_lower:
                    raise ValueError(
                        f"Distractor '{d}' matches correct_answer '{content.correct_answer}'"
                    )
        return values

    def model_dump(self) -> dict:
        return self.dict()

    @classmethod
    def model_validate(cls, obj: dict) -> "Exercise":
        return cls(**obj)


class FilterResult(BaseModel):
    item_id: str
    passed: bool
    checks: Dict[str, Any]
