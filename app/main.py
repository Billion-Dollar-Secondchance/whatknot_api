# app/main.py
from fastapi import FastAPI, HTTPException
from app.core.exception_handlers import http_exception_handler
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings

# ✅ Ensure all models are loaded — this line is crucial
import app.db.models  # Triggers app/db/models/__init__.py

# Your routers
from app.api.routes import auth, auth_google
from app.api.routes import user, pairing, mystery_moodbox, admin_moodbox,prompt_question,mystery_moodbox_prompted_question
from app.api.routes import badges
from app.api.routes.earned_badges import router as earned_badges_router
from app.api.routes import streak
from app.api.routes import admin_vibe,user_relationship_settings,single_pairing
from app.api.routes import vibe_match,admin_single_vibe,admin_single_prompts,admin_single_prompt_schedule,vibe_single_prompt_today,single_vibe_prompt_response

app = FastAPI(debug=settings.DEBUG)

# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="whatknot_session"
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(auth_google.router, prefix="/oauth", tags=["Google OAuth"]) 
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(pairing.router, prefix="/pairing", tags=["Pairing"])
app.include_router(mystery_moodbox.router, prefix="/mystery-moodbox", tags=["MysteryMoodbox"])
app.include_router(
    admin_moodbox.router,
    prefix="/admin",
    tags=["Admin Moodbox"]
)
app.include_router(mystery_moodbox_prompted_question.router, prefix="/mystery-moodbox", tags=["Prompted Questions"])
app.include_router(prompt_question.router, prefix="/mystery-moodbox")
app.include_router(badges.router, tags=["Badges"])
app.include_router(earned_badges_router, prefix="/mystery-moodbox")
app.include_router(streak.router, prefix="/mystery-moodbox", tags=["Streak"])
app.include_router(admin_vibe.router,prefix="/admin", tags=["Admin Vibe Match"])
app.include_router(vibe_match.router, prefix="/vibe-match", tags=["Vibe Match"])
app.include_router(admin_single_vibe.router, prefix="/admin", tags=["Admin single Vibe Match"])
app.include_router(admin_single_prompts.router, prefix="/admin", tags=["Admin single Vibe Match"])
app.include_router(admin_single_prompt_schedule.router, prefix="/admin", tags=["Admin single Vibe Match"])
app.include_router(vibe_single_prompt_today.router, prefix="/single", tags=["single Vibe Match"])
app.include_router(single_vibe_prompt_response.router, prefix="/single", tags=["single Vibe response"])
app.include_router(user_relationship_settings.router, prefix="/settings", tags=["user settings"])
app.include_router(single_pairing.router, prefix="/singles", tags=["Pairing"])









