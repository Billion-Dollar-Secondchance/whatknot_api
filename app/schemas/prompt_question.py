from pydantic import BaseModel
from typing import Dict

class PromptQuestionMap(BaseModel):
    question_map: Dict[str, str]