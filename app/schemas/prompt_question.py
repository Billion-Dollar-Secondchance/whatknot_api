from pydantic import BaseModel
from typing import Dict,List
from uuid import UUID
from datetime import date

class PromptQuestionMap(BaseModel):
    question_map: Dict[str, str]


class SchedulePromptQuestionRequest(BaseModel):
    scheduled_date: date
    question_ids: List[UUID]
    pair_days_condition: str  # e.g. "all", "=1", ">5", ">=2 and <=7"

class MysteryScheduleEntry(BaseModel):
    question_id: UUID
    scheduled_date: date
    pair_days_condition: str

class MysteryScheduleBulkRequest(BaseModel):
    schedule: List[MysteryScheduleEntry]

class MysteryPromptSchedule(BaseModel):
    question_id: UUID
    scheduled_date: date
    pair_days_condition: str