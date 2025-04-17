from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, email: str, password: str, login_type: str, vibe_as: str):
    hashed_pw = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_pw, login_type=login_type, vibe_as=vibe_as)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_token(user: User):
    data = {"sub": user.email}
    return create_access_token(data=data, expires_delta=timedelta(minutes=60))
