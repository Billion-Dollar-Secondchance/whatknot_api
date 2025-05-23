from app.db import engine, Base

# ✅ Referenced table first
from .mystery_moodbox_questions import MysteryMoodboxQuestion
from .mystery_moodbox import MysteryMoodbox
from .day_question_mapping import DayQuestionMapping
from .user import User
from .partner_pairing import PartnerPairing
from .mystery_moodbox_prompted_questions import MysteryMoodboxPromptedQuestion
from .vibe_match import VibeQuestion, VibeMatch, VibeMatchResponse, VibeQuestionDayMapping, VibeQuestionDateMapping
from .single_vibe_matched_pairs import SingleVibeMatchedPair
from .user_relationship_settings import UserRelationshipSettings
from .single_vibe_paired_users import SingleVibePairedUser

Base.metadata.create_all(bind=engine)
