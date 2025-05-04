from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from typing import List
from datetime import datetime

class PromptStatusEnum(str, Enum):
    prompted = "prompted"
    guessed = "guessed"
    answered_by_one = "answered_by_one"
    answered_by_both = "answered_by_both"


class MysteryMoodboxPromptedQuestionCreate(BaseModel):
    pair_id: str
    question_id: UUID
    prompted_user_id: str
    # prompt_status: PromptStatusEnum = PromptStatusEnum.prompted


class MysteryMoodboxPromptedQuestionOut(MysteryMoodboxPromptedQuestionCreate):
    prompt_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class MysteryMoodboxPromptedQuestionResponse(BaseModel):
    prompt_id: UUID
    pair_id: str
    question_id: UUID
    prompted_user_id: str
    question_text: str
    options: List[str]
    created_at: datetime
    prompt_status: str

    class Config:
        from_attributes = True 

class SubmitPromptResponse(BaseModel):
    prompt_id: UUID
    answer: str 

class SubmitGuessRequest(BaseModel):
    prompt_id: UUID
    guess_text: str

