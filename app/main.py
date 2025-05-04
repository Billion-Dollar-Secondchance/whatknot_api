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
# app.include_router(prompt_question.router, prefix="/mystery-moodbox")
app.include_router(mystery_moodbox_prompted_question.router, prefix="/mystery-moodbox", tags=["Prompted Questions"])
app.include_router(prompt_question.router, prefix="/mystery-moodbox")

app.include_router(badges.router, tags=["Badges"])

