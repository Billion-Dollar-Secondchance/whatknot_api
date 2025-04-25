from datetime import date
from sqlalchemy.orm import Session
from app.db.models.user import User, generate_incremental_user_id
from app.utils.auth import get_password_hash

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_guest_token(db: Session, guest_token: str) -> User | None:
    return db.query(User).filter(User.guest_token == guest_token).first()

def create_guest_user(db: Session, guest_token: str, vibe_as: str | None = None) -> User:
    user = User(
        user_id=generate_incremental_user_id(db),
        login_type="guest",
        guest_token=guest_token,
        vibe_as=vibe_as
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_email_user(db: Session, email: str, password: str, login_type: str, vibe_as: str | None = None) -> User:
    hashed_password = get_password_hash(password)
    user = User(
        user_id=generate_incremental_user_id(db),
        email=email,
        hashed_password=hashed_password,
        login_type=login_type,
        vibe_as=vibe_as
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# def create_google_user(
#     db: Session,
#     email: str,
#     name: str | None = None,
#     vibe_as: str | None = None,
#     guest_token: str | None = None
# ) -> User:
#     user = User(
#         user_id=generate_incremental_user_id(db),
#         email=email,
#         name=name,
#         login_type="google",
#         vibe_as=vibe_as,
#         guest_token=guest_token
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

def create_google_user(
    db: Session,
    email: str,
    name: str | None = None,
    profile_image: str | None = None,
    gender: str | None = None,
    date_of_birth: str | None = None,
    google_id: str | None = None,
    vibe_as: str | None = None,
    guest_token: str | None = None
) -> User:
    user = User(
        user_id=generate_incremental_user_id(db),
        email=email,
        name=name,
        profile_image=profile_image,
        gender=gender,
        date_of_birth=date_of_birth,
        google_id=google_id,
        login_type="google",
        vibe_as=vibe_as,
        guest_token=guest_token
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_profile(
    db: Session,
    user: User,
    vibe_as: str = None,
    gender: str = None,
    date_of_birth: date = None
) -> User:
    if vibe_as is not None:
        user.vibe_as = vibe_as
    if gender is not None:
        user.gender = gender
    if date_of_birth is not None:
        user.date_of_birth = date_of_birth

    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_pairing_code(db: Session, code: str) -> User | None:
    return db.query(User).filter(User.pairing_code == code).first()

def update_pairing_status(db: Session, user_id: str, status: str) -> None:
    db.query(User).filter(User.user_id == user_id).update({"pairing_status": status})
    db.commit()