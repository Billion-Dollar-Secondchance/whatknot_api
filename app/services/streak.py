# app/services/streak.py

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from app.db.models.pair_streak import PairStreak
from app.db.models.badge_definition import BadgeDefinition
from app.db.models.pair_badges import PairBadge
from app.db.models.mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion


def update_streak_logic(db: Session, pair_id: str, is_match: bool):
    print(f"🔁 update_streak_logic triggered for pair_id={pair_id}, is_match={is_match}")

    # 1. Update streak
    streak = db.query(PairStreak).filter(PairStreak.pair_id == pair_id).first()
    if not streak:
        print("🆕 No streak found. Creating new streak entry.")
        streak = PairStreak(
            pair_id=pair_id,
            current_streak=1,
            longest_streak=1,
            last_updated=datetime.utcnow()
        )
        db.add(streak)
    else:
        streak.current_streak += 1
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.last_updated = datetime.utcnow()
        print(f"📊 Updated streak: current_streak={streak.current_streak}, longest_streak={streak.longest_streak}")

    db.commit()

    unlocked_badge = None

    if is_match:
        total_matches = db.query(MysteryMoodboxPromptedQuestion).filter(
            MysteryMoodboxPromptedQuestion.pair_id == pair_id,
            MysteryMoodboxPromptedQuestion.answer_matched == True
        ).count()

        print(f"✅ Total correct matches for pair: {total_matches}")
        print(f"🔥 Checking for eligible badges with streak >= {streak.current_streak} or matches >= {total_matches}")

        eligible_badges = db.query(BadgeDefinition).filter(
            or_(
                and_(BadgeDefinition.min_streak != None, BadgeDefinition.min_streak <= streak.current_streak),
                and_(BadgeDefinition.min_matches != None, BadgeDefinition.min_matches <= total_matches)
            )
        ).all()

        print(f"🏅 Eligible badges count: {len(eligible_badges)}")
        for badge in eligible_badges:
            print(f"➡️ Checking badge: {badge.name}")
            already_awarded = db.query(PairBadge).filter(
                and_(
                    PairBadge.pair_id == pair_id,
                    PairBadge.badge_id == badge.badge_id
                )
            ).first()

            if not already_awarded:
                print(f"🎉 Unlocking new badge: {badge.name}")
                new_pair_badge = PairBadge(
                    pair_id=pair_id,
                    badge_id=badge.badge_id
                )
                db.add(new_pair_badge)
                unlocked_badge = {
                    "name": badge.name,
                    "image_url": badge.image_url,
                    "description": badge.description,
                    "badge_type": badge.badge_type
                }

        db.commit()
    else:
        print("❌ Not a match — badge eligibility check skipped.")

    print(f"✅ Final streak: {streak.current_streak}, Unlocked badge: {unlocked_badge}")
    return {
        "streak_count": streak.current_streak,
        "badge": unlocked_badge
    }
