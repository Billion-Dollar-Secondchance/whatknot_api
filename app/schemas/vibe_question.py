from typing import Optional, Dict,List
from pydantic import BaseModel, model_validator
from uuid import UUID
from datetime import datetime,date

class VibeQuestionCreate(BaseModel):
    question_text: str
    question_type: str
    options: Optional[Dict[str, str]] = None

    @model_validator(mode="after")
    def validate_options_by_type(self):
        q_type = self.question_type
        options = self.options

        option_required_types = [
            "single_choice", "multi_choice", "emoji_choice", "image_choice", "true_false", "swipe"
        ]
        exact_two_required_types = ["true_false", "swipe"]
        no_options_types = ["text", "date_picker", "time_picker", "scale_rating"]

        if q_type in option_required_types:
            if not options or not isinstance(options, dict) or len(options) == 0:
                raise ValueError(f"Options are required for question_type '{q_type}'.")

        if q_type in exact_two_required_types and options and len(options) != 2:
            raise ValueError(f"question_type '{q_type}' must have exactly 2 options.")

        if q_type in no_options_types and options:
            raise ValueError(f"question_type '{q_type}' should not include options.")

        return self

class VibeQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    options: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = None

class VibeDayMappingBulkCreate(BaseModel):
    question_ids: List[UUID]
    days_condition: Optional[str] = None
    scheduled_date: Optional[date] = None

class VibeDateMappingBulkCreate(BaseModel):
    question_ids: List[UUID]
    scheduled_date: date

class VibeMatchResponseOut(BaseModel):
    vibe_response_id: UUID
    vibe_match_id: UUID
    question_id: UUID
    user_id: str
    answer: str
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2