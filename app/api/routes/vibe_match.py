# File: app/api/routes/vibe_match.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, date
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.db.models.user import User
from app.db.models.vibe_match import VibeQuestion, VibeQuestionDayMapping, VibeQuestionDateMapping, VibeMatch, VibeMatchResponse
from app.db.models.partner_pairing import PartnerPairing
from app.db.models.pair_streak import PairStreak  # ✅ NEW
from app.utils.response_format import success_response, failure_response

router = APIRouter()

@router.get("/start")
def start_vibe_match(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == 'active'
    ).first()

    if not pair:
        return failure_response("Active pair not found", status_code=404)

    created_at = pair.created_at
    days_since_paired = (datetime.utcnow().date() - created_at.date()).days
    today = datetime.utcnow().date()

    # --- Fetch question_ids by days_condition ---
    day_mappings = db.query(VibeQuestionDayMapping).all()
    day_question_ids = set()
    for m in day_mappings:
        condition = m.days_condition.strip()
        try:
            if condition.startswith("<"):
                if days_since_paired < int(condition[1:]):
                    day_question_ids.add(m.question_id)
            elif condition.startswith(">="):
                if days_since_paired >= int(condition[2:]):
                    day_question_ids.add(m.question_id)
            elif condition.startswith(">"):
                if days_since_paired > int(condition[1:]):
                    day_question_ids.add(m.question_id)
            elif condition.startswith("="):
                if days_since_paired == int(condition[1:]):
                    day_question_ids.add(m.question_id)
            elif "and" in condition:
                parts = condition.replace(" ", "").split("and")
                low = int(parts[0].split(">=")[1])
                high = int(parts[1].split("<=")[1])
                if low <= days_since_paired <= high:
                    day_question_ids.add(m.question_id)
        except Exception:
            continue

    # --- Fetch question_ids by today's date ---
    date_question_ids = {
        row.question_id
        for row in db.query(VibeQuestionDateMapping).filter(
            VibeQuestionDateMapping.scheduled_date == today
        ).all()
    }

    combined_question_ids = list(day_question_ids.union(date_question_ids))

    questions = db.query(VibeQuestion).filter(
        VibeQuestion.question_id.in_(combined_question_ids),
        VibeQuestion.is_active == True
    ).all()

    # --- Get or create today's VibeMatch ---
    existing_match = db.query(VibeMatch).filter(
        VibeMatch.pair_id == pair.pair_id,
        VibeMatch.created_at >= datetime.combine(today, datetime.min.time())
    ).first()

    if existing_match:
        vibe_match_id = existing_match.vibe_match_id
    else:
        new_match = VibeMatch(
            vibe_match_id=uuid4(),
            pair_id=pair.pair_id,
            num_questions=len(questions),
            started_by=current_user.user_id,
            status="started",
            created_at=datetime.utcnow()
        )
        db.add(new_match)
        db.commit()
        vibe_match_id = new_match.vibe_match_id

    answered_question_ids = {
        str(row.question_id)
        for row in db.query(VibeMatchResponse.question_id).filter(
            VibeMatchResponse.vibe_match_id == vibe_match_id,
            VibeMatchResponse.user_id == current_user.user_id
        ).all()
    }

    questions_payload = [
        {
            "question_id": str(q.question_id),
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options": q.options,
            "answered": str(q.question_id) in answered_question_ids
        } for q in questions
    ]

    return success_response(
        message="Vibe match questions fetched",
        data={
            "vibe_match_id": str(vibe_match_id),
            "pair_id": str(pair.pair_id),
            "days_since_paired": days_since_paired,
            "questions": questions_payload
        }
    )


@router.post("/submit-response")
def submit_vibe_response(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vibe_match_id = payload.get("vibe_match_id")
    question_id = payload.get("question_id")
    answer = payload.get("answer")

    if not (vibe_match_id and question_id and answer):
        return failure_response("vibe_match_id, question_id and answer are required", status_code=400)

    existing_response = db.query(VibeMatchResponse).filter_by(
        vibe_match_id=vibe_match_id,
        question_id=question_id,
        user_id=current_user.user_id
    ).first()

    if existing_response:
        existing_response.answer = answer
        existing_response.created_at = datetime.utcnow()
    else:
        new_response = VibeMatchResponse(
            vibe_response_id=uuid4(),
            vibe_match_id=vibe_match_id,
            question_id=question_id,
            user_id=current_user.user_id,
            answer=answer,
            created_at=datetime.utcnow()
        )
        db.add(new_response)

    db.commit()
    return success_response(message="Response submitted successfully")


@router.get("/results/today")
def get_today_match_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = datetime.utcnow().date()
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == 'active'
    ).first()

    if not pair:
        return failure_response("Active pair not found", status_code=404)

    vibe_match = db.query(VibeMatch).filter(
        VibeMatch.pair_id == pair.pair_id,
        VibeMatch.created_at >= datetime.combine(today, datetime.min.time())
    ).first()

    if not vibe_match:
        return failure_response("No match found for today", status_code=404)

    responses = db.query(VibeMatchResponse).filter(
        VibeMatchResponse.vibe_match_id == vibe_match.vibe_match_id
    ).all()

    # group answers by question_id
    answers_map = {}
    for r in responses:
        qid = str(r.question_id)
        if qid not in answers_map:
            answers_map[qid] = {}
        answers_map[qid][r.user_id] = r.answer

    matched = 0
    total = len(answers_map)
    details = []

    for qid, user_answers in answers_map.items():
        question = db.query(VibeQuestion).filter_by(question_id=qid).first()
        user_answer = user_answers.get(current_user.user_id)
        partner_answer = [v for k, v in user_answers.items() if k != current_user.user_id]
        partner_answer = partner_answer[0] if partner_answer else None

        is_match = user_answer and partner_answer and str(user_answer).strip().lower() == str(partner_answer).strip().lower()
        if is_match:
            matched += 1

        details.append({
            "question_text": question.question_text if question else "",
            "user_answer": user_answer,
            "partner_answer": partner_answer,
            "matched": is_match
        })

    return success_response(
        message="Match results fetched",
        data={
            "vibe_match_id": str(vibe_match.vibe_match_id),
            "total_questions": total,
            "matched_answers": matched,
            "match_score": int((matched / total) * 100) if total > 0 else 0,
            "questions": details
        }
    )


@router.get("/history")
def get_vibe_match_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == 'active'
    ).first()

    if not pair:
        return failure_response("Active pair not found", status_code=404)

    matches = db.query(VibeMatch).filter(
        VibeMatch.pair_id == pair.pair_id
    ).order_by(VibeMatch.created_at.desc()).all()

    history = []
    for match in matches:
        responses = db.query(VibeMatchResponse).filter(
            VibeMatchResponse.vibe_match_id == match.vibe_match_id
        ).all()

        answers_map = {}
        for r in responses:
            qid = str(r.question_id)
            if qid not in answers_map:
                answers_map[qid] = {}
            answers_map[qid][r.user_id] = r.answer

        matched = 0
        total = len(answers_map)
        for qid, user_answers in answers_map.items():
            values = list(user_answers.values())
            if len(values) == 2 and values[0].strip().lower() == values[1].strip().lower():
                matched += 1

        history.append({
            "date": match.created_at.strftime("%Y-%m-%d"),
            "vibe_match_id": str(match.vibe_match_id),
            "total_questions": total,
            "matched_answers": matched,
            "match_score": int((matched / total) * 100) if total > 0 else 0
        })

    return success_response(message="Match history fetched", data=history)


@router.get("/{vibe_match_id}/results")
def get_match_result_by_id(
    vibe_match_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    match = db.query(VibeMatch).filter_by(vibe_match_id=vibe_match_id).first()

    if not match:
        return failure_response("Match not found", status_code=404)

    # Check that user belongs to this pair
    pair = db.query(PartnerPairing).filter_by(pair_id=str(match.pair_id)).first()
    if not pair or current_user.user_id not in [pair.user_id, pair.partner_id]:
        return failure_response("Unauthorized access to this match", status_code=403)

    responses = db.query(VibeMatchResponse).filter(
        VibeMatchResponse.vibe_match_id == match.vibe_match_id
    ).all()

    answers_map = {}
    for r in responses:
        qid = str(r.question_id)
        if qid not in answers_map:
            answers_map[qid] = {}
        answers_map[qid][r.user_id] = r.answer

    matched = 0
    total = len(answers_map)
    details = []

    for qid, user_answers in answers_map.items():
        question = db.query(VibeQuestion).filter_by(question_id=qid).first()
        user_answer = user_answers.get(current_user.user_id)
        partner_answer = [v for k, v in user_answers.items() if k != current_user.user_id]
        partner_answer = partner_answer[0] if partner_answer else None

        is_match = user_answer and partner_answer and str(user_answer).strip().lower() == str(partner_answer).strip().lower()
        if is_match:
            matched += 1

        details.append({
            "question_text": question.question_text if question else "",
            "user_answer": user_answer,
            "partner_answer": partner_answer,
            "matched": is_match
        })

    return success_response(
        message="Match results fetched",
        data={
            "vibe_match_id": str(match.vibe_match_id),
            "total_questions": total,
            "matched_answers": matched,
            "match_score": int((matched / total) * 100) if total > 0 else 0,
            "questions": details
        }
    )



# --- Endpoint: /update-streak ---
@router.post("/update-streak")
def update_pair_streak(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == 'active'
    ).first()

    if not pair:
        return failure_response("Active pair not found", status_code=404)

    today = datetime.utcnow().date()
    match = db.query(VibeMatch).filter(
        VibeMatch.pair_id == pair.pair_id,
        VibeMatch.created_at >= datetime.combine(today, datetime.min.time())
    ).first()

    if not match:
        return failure_response("No match found for today", status_code=404)

    responses = db.query(VibeMatchResponse).filter(
        VibeMatchResponse.vibe_match_id == match.vibe_match_id
    ).all()

    # Calculate matched score
    answers_map = {}
    for r in responses:
        qid = str(r.question_id)
        if qid not in answers_map:
            answers_map[qid] = {}
        answers_map[qid][r.user_id] = r.answer

    matched = 0
    total = len(answers_map)
    for user_answers in answers_map.values():
        values = list(user_answers.values())
        if len(values) == 2 and values[0].strip().lower() == values[1].strip().lower():
            matched += 1

    full_match = total > 0 and matched == total

    streak = db.query(PairStreak).filter_by(pair_id=str(pair.pair_id)).first()

    if full_match:
        if streak:
            streak.current_streak += 1
            streak.last_updated = datetime.utcnow()
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
        else:
            streak = PairStreak(
                pair_id=str(pair.pair_id),
                current_streak=1,
                longest_streak=1,
                last_updated=datetime.utcnow()
            )
            db.add(streak)
    else:
        if streak:
            streak.current_streak = 0
            streak.last_updated = datetime.utcnow()

    db.commit()

    return success_response(
        message="Streak updated",
        data={
            "current_streak": streak.current_streak if streak else 0,
            "longest_streak": streak.longest_streak if streak else 0
        }
    )

# --- NOTE: Start of Mystery Moodbox date-mapping implementation plan ---
# This code will help us align Vibe Match and Mystery Moodbox scheduling.
# We will implement similar logic in mystery_moodbox routes after adding:
# - mystery_moodbox_date_mapping table
# - fallback to days_since_paired
# --- END NOTE ---

# --- GET /vibe-match/vibe-meter ---
@router.get("/vibe-meter")
def get_vibe_meter_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pair = db.query(PartnerPairing).filter(
        ((PartnerPairing.user_id == current_user.user_id) |
         (PartnerPairing.partner_id == current_user.user_id)),
        PartnerPairing.pair_status == 'active'
    ).first()

    if not pair:
        return failure_response("Active pair not found", status_code=404)

    matches = db.query(VibeMatch).filter(
        VibeMatch.pair_id == pair.pair_id
    ).all()

    total_matched = 0
    total_attempts = 0

    for match in matches:
        responses = db.query(VibeMatchResponse).filter(
            VibeMatchResponse.vibe_match_id == match.vibe_match_id
        ).all()

        answers_map = {}
        for r in responses:
            qid = str(r.question_id)
            if qid not in answers_map:
                answers_map[qid] = {}
            answers_map[qid][r.user_id] = r.answer

        for user_answers in answers_map.values():
            if len(user_answers) == 2:
                total_attempts += 1
                values = list(user_answers.values())
                if values[0].strip().lower() == values[1].strip().lower():
                    total_matched += 1

    score = int((total_matched / total_attempts) * 100) if total_attempts > 0 else 0

    return success_response(
        message="Vibe meter fetched",
        data={
            "vibe_meter_score": score,
            "matched_answers": total_matched,
            "total_answers": total_attempts
        }
    )
