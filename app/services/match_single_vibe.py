from sqlalchemy.orm import Session
from datetime import date
from app.db.models.single_vibe_prompt_response import SingleVibePromptResponse
from app.db.models.single_vibe_matched_pairs import SingleVibeMatchedPair
from app.db.models.single_vibe_prompt_schedule import SingleVibePromptSchedule
from app.db.models.user import User
from app.utils.id_generator import generate_single_vibe_match_id

def match_users_by_vibe(db: Session):
    today = date.today()
    schedules = db.query(SingleVibePromptSchedule).filter_by(scheduled_date=today).all()

    for schedule in schedules:
        responses = db.query(SingleVibePromptResponse).filter_by(
            prompt_schedule_id=schedule.prompt_schedule_id
        ).all()

        answer_map = {}
        for r in responses:
            answer_map.setdefault(r.answer, []).append(r.user_id)

        for answer, user_ids in answer_map.items():
            if len(user_ids) < 2:
                continue

            # Load user objects in one go
            users = db.query(User).filter(User.user_id.in_(user_ids)).all()
            user_map = {u.user_id: u for u in users}

            user_ids = sorted(user_map.keys())
            for i in range(len(user_ids)):
                for j in range(i + 1, len(user_ids)):
                    u1_id, u2_id = user_ids[i], user_ids[j]
                    u1, u2 = user_map[u1_id], user_map[u2_id]

                    # ✅ Gender & Orientation filter
                    if not u1.gender or not u2.gender or not u1.interested_in or not u2.interested_in:
                        continue

                    if (u1.gender not in u2.interested_in) or (u2.gender not in u1.interested_in):
                        continue

                    # ✅ Avoid duplicate matches
                    existing = db.query(SingleVibeMatchedPair).filter(
                        ((SingleVibeMatchedPair.user_1_id == u1_id) & (SingleVibeMatchedPair.user_2_id == u2_id)) |
                        ((SingleVibeMatchedPair.user_1_id == u2_id) & (SingleVibeMatchedPair.user_2_id == u1_id)),
                        SingleVibeMatchedPair.prompt_schedule_id == schedule.prompt_schedule_id
                    ).first()
                    if existing:
                        continue

                    match = SingleVibeMatchedPair(
                        single_vibe_match_id=generate_single_vibe_match_id(db),
                        user_1_id=u1_id,
                        user_2_id=u2_id,
                        prompt_schedule_id=schedule.prompt_schedule_id,
                        matched_on=today
                    )
                    db.add(match)

    db.commit()
