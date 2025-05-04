# app/schemas/prompt.py
from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Dict

class PromptQuestionRequest(BaseModel):
    question_map: Dict[str, str]  # like { ">5": "<question_id>" }

class WrappedResponse(BaseModel):
    status: str
    message: str
    data: dict | None = None