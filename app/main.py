# app/main.py
from fastapi import FastAPI, HTTPException
from app.core.exception_handlers import http_exception_handler
from starlette.middleware.sessions import SessionMiddleware

from app.api.routes import auth, auth_google
from app.config import settings
from app.api.routes import user,pairing


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
