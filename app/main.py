# app/main.py
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.routes import auth, auth_google
from app.config import settings

app = FastAPI(debug=settings.DEBUG)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(auth_google.router, prefix="/oauth", tags=["Google OAuth"])  # Changed prefix
