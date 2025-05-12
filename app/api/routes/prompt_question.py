from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone,date,timedelta
import random
import re
from typing import List
from uuid import uuid4
import sqlalchemy as sa
from app.db.models.user import User
from app.schemas.prompt_question import PromptQuestionMap,MysteryPromptSchedule
from app.dependencies.auth import get_current_user, get_db
from app.db.models.partner_pairing import PartnerPairing
from app.db.models.mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion,MysteryMoodboxDateMapping
from sqlalchemy import func

from app.utils.response_format import success_response, failure_response

router = APIRouter()


def evaluate_condition(condition: str, days_since: int) -> bool:
    try:
        # Normalize and extract operator and value
        condition = condition.strip()
        match = re.match(r"^(==|>=|<=|>|<|=)?\s*(\d+)$", condition)
        if not match:
            return False
        operator, value = match.groups()
        operator = operator or "=="
        if operator == "=":
            operator = "=="
        expression = f"{days_since} {operator} {value}"
        return eval(expression, {"__builtins__": {}})
    except Exception as e:
        print(f"Condition Eval Error: {condition} -> {e}")
        return False

@router.post("/prompt-question")
def prompt_question(payload: PromptQuestionMap, db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).date()
    created_count = 0

    active_pairs = db.query(PartnerPairing).filter(PartnerPairing.pair_status == 'active').all()

    for pair in active_pairs:
        days_since = (today - pair.created_at.date()).days
        selected_question_id = None
        print(f"Pair: {pair.pair_id}, Days Since: {days_since}")

        for condition_str, question_id in payload.question_map.items():
            print(f"Evaluating condition: {condition_str} with days_since: {days_since}")
            if evaluate_condition(condition_str, days_since):
                selected_question_id = question_id
                print(f"✔️ Condition matched! Using question ID: {question_id}")
                break
            else:
                print(f"❌ Condition did not match.")

        if not selected_question_id:
            continue

        # ✅ Prevent duplicate prompts for same pair on same day
        existing_prompt = db.query(MysteryMoodboxPromptedQuestion).filter(
            MysteryMoodboxPromptedQuestion.pair_id == pair.pair_id,
            sa.func.date(MysteryMoodboxPromptedQuestion.created_at) == today
        ).first()

        if existing_prompt:
            continue

        prompted_user_id = random.choice([pair.user_id, pair.partner_id])

        new_prompt = MysteryMoodboxPromptedQuestion(
            prompt_id=str(uuid4()),
            pair_id=pair.pair_id,
            question_id=selected_question_id,
            prompted_user_id=prompted_user_id,
            prompt_status='prompted'
        )
        db.add(new_prompt)
        created_count += 1

    db.commit()
    return {"message": f"{created_count} prompt questions inserted successfully"}



@router.post("/schedule-prompts")
def schedule_mystery_prompts(
    payload: List[MysteryPromptSchedule],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        mappings = [
            MysteryMoodboxDateMapping(
                mapping_id=uuid4(),
                question_id=item.question_id,
                scheduled_date=item.scheduled_date,
                pair_days_condition=item.pair_days_condition,
                created_at=datetime.utcnow()
            )
            for item in payload
        ]

        db.add_all(mappings)
        db.commit()
        return success_response(message="Scheduled prompt questions saved", data={"count": len(mappings)})

    except Exception as e:
        db.rollback()
        return failure_response(message="Error scheduling prompts", data=str(e))
    

@router.post("/trigger-scheduled-prompts")
def trigger_scheduled_prompt_questions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # today = datetime.now(timezone.utc).date()
    # IST = timezone(timedelta(hours=5, minutes=30))
    # today = datetime.now(IST).date()
    
    today = datetime.now(timezone.utc).date()
    print("DateTime==>",today)
    mappings = db.query(MysteryMoodboxDateMapping).filter(
        MysteryMoodboxDateMapping.scheduled_date == today
    ).all()

    if not mappings:
        return success_response(message="No scheduled questions for today.")

    active_pairs = db.query(PartnerPairing).filter(
        PartnerPairing.pair_status == 'active'
    ).all()

    inserted = 0

    for pair in active_pairs:
        days_since = (today - pair.created_at.date()).days
        for mapping in mappings:
            if not mapping.pair_days_condition or evaluate_condition(mapping.pair_days_condition, days_since):
                existing = db.query(MysteryMoodboxPromptedQuestion).filter(
                    MysteryMoodboxPromptedQuestion.pair_id == pair.pair_id,
                    MysteryMoodboxPromptedQuestion.question_id == mapping.question_id,
                    MysteryMoodboxPromptedQuestion.created_at >= datetime.combine(today, datetime.min.time())
                ).first()

                if existing:
                    continue

                prompted_user = random.choice([pair.user_id, pair.partner_id])
                prompt = MysteryMoodboxPromptedQuestion(
                    prompt_id=str(uuid4()),
                    pair_id=pair.pair_id,
                    question_id=mapping.question_id,
                    prompted_user_id=prompted_user,
                    prompt_status='prompted'
                )
                db.add(prompt)
                inserted += 1

    db.commit()
    return success_response(message="Scheduled prompts triggered", data={"inserted_count": inserted})

