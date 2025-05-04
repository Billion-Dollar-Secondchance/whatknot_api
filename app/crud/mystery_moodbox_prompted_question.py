from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.models.mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion
from app.schemas.mystery_moodbox_prompted_question import MysteryMoodboxPromptedQuestionCreate


def create_prompted_question(
    db: Session,
    data: MysteryMoodboxPromptedQuestionCreate
) -> MysteryMoodboxPromptedQuestion:
    db_prompt = MysteryMoodboxPromptedQuestion(
        prompt_id=uuid4(),
        pair_id=data.pair_id,
        question_id=data.question_id,
        prompted_user_id=data.prompted_user_id,
        prompt_status=data.prompt_status,
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt
