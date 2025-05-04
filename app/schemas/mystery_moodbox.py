# app/schemas/mystery_moodbox.py

from pydantic import BaseModel
from datetime import date, time
from typing import Optional
from enum import Enum as PyEnum

class QuestionType(str, PyEnum):
    input_text = "input_text"
    single_choice = "single_choice"
    multi_choice = "multi_choice"


class SubmitMoodRequest(BaseModel):
    mood: str
    explanation: Optional[str] = None

class MoodPromptAnswerRequest(BaseModel):
    prompt_id: str
    answer: str


class AddMoodboxQuestionRequest(BaseModel):
    question: str
    question_type: QuestionType
    options: list[str] | None = None  # only for choice types

    class Config:
        from_attributes = True

class PromptQuestionRequest(BaseModel):
    pair_id: str