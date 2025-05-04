from app.db import engine, Base

# ✅ Referenced table first
from .mystery_moodbox_questions import MysteryMoodboxQuestion
from .mystery_moodbox import MysteryMoodbox
from .day_question_mapping import DayQuestionMapping
from .user import User
from .partner_pairing import PartnerPairing
from .mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion


Base.metadata.create_all(bind=engine)
