# app/api/routes/streaks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models.user import User
from app.db.models.mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion
from app.db.models.pair_streak import PairStreak
from app.utils.response_format import success_response, failure_response
from app.dependencies.auth  import get_current_user,get_db

router = APIRouter()

@router.post("/update-streak")
def update_streak_after_guess(
    prompt_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch the prompted question
    prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
        MysteryMoodboxPromptedQuestion.prompt_id == prompt_id
    ).first()

    if not prompt:
        return failure_response("Prompt not found")

    if prompt.answer is None or prompt.guess_text is None:
        return failure_response("Answer or guess not submitted yet")

    # Determine pair_id
    pair_id = prompt.pair_id
    is_correct = prompt.answer.strip().lower() == prompt.guess_text.strip().lower()

    # Fetch or create streak record
    streak = db.query(PairStreak).filter(PairStreak.pair_id == pair_id).first()

    if not streak:
        streak = PairStreak(
            pair_id=pair_id,
            current_streak=1 if is_correct else 0,
            longest_streak=1 if is_correct else 0,
            last_updated=datetime.utcnow()
        )
        db.add(streak)
    else:
        if is_correct:
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
        else:
            streak.current_streak = 0  # streak broken on wrong guess

        streak.last_updated = datetime.utcnow()

    db.commit()

    return success_response("Streak updated", data={
        "pair_id": pair_id,
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak
    })
