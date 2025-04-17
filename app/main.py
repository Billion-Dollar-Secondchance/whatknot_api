# app/main.py
from fastapi import FastAPI
from app.api.routes import auth
from app.config import settings

app = FastAPI(debug=settings.DEBUG)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
