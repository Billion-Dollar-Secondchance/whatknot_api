from typing import Optional, List
from pydantic import BaseModel

class MoodboxQuestionCreate(BaseModel):
    question_text: str
    question_type: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    created_by_type: Optional[str] = "user"

    class Config:
        from_attributes = True