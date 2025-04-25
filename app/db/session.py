# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Add this function to fix your import error
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
