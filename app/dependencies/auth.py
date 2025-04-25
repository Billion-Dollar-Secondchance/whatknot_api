# app/dependencies/auth.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User

def get_current_user(db: Session = Depends(get_db)) -> User:
    # Mocked current user. Replace with actual auth logic.
    user = db.query(User).first()  # Replace with real query based on token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user
