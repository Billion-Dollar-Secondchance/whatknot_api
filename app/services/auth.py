# from datetime import timedelta
# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from app.db.models.user import User, generate_incremental_user_id
# from app.utils.auth import verify_password, get_password_hash
# from app.core.security import create_access_token
# from app.crud.user import (
#     get_user_by_email,
#     get_user_by_guest_token,
#     create_guest_user,
#     create_email_user,
#     create_google_user
# )

# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# def create_user(
#     db: Session,
#     email: str | None,
#     password: str | None,
#     login_type: str,
#     vibe_as: str | None,
#     guest_token: str | None = None,
#     name: str | None = None 
# ) -> User:
#     if login_type in ("email", "google"):
#         if login_type == "email" and not password:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password required")
#         existing = get_user_by_email(db, email)
#         if existing:
#             return existing
#         return create_email_user(db, email, password, login_type, vibe_as)

#     if login_type == "guest":
#         if not guest_token:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="guest_token required")
#         existing = get_user_by_guest_token(db, guest_token)
#         if existing:
#             return existing
#         return create_guest_user(db, guest_token, vibe_as)

#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login_type")

# def authenticate_user(db: Session, email: str, password: str) -> User | None:
#     user = get_user_by_email(db, email)
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user

# def create_token(user: User) -> str:
#     data = {"sub": user.user_id}
#     return create_access_token(data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

# def get_or_create_google_user(
#     db: Session,
#     email: str,
#     name: str = None,
#     profile_image: str = None,
#     gender: str = None,
#     date_of_birth: str = None,
#     google_id: str = None,
#     vibe_as: str = None,
#     guest_token: str = None
# ) -> User:
#     user = get_user_by_email(db, email)
#     if user:
#         return user
#     return create_google_user(
#         db,
#         email=email,
#         name=name,
#         profile_image=profile_image,
#         gender=gender,
#         date_of_birth=date_of_birth,
#         google_id=google_id,
#         vibe_as=vibe_as,
#         guest_token=guest_token
#     )

# def create_google_user(
#     db: Session,
#     email: str,
#     name: str = None,
#     profile_image: str = None,
#     gender: str = None,
#     date_of_birth: str = None,
#     google_id: str = None,
#     vibe_as: str = None,
#     guest_token: str = None
# ) -> User:
#     user = User(
#         user_id=generate_incremental_user_id(db),
#         email=email,
#         name=name,
#         profile_image=profile_image,
#         gender=gender,
#         date_of_birth=date_of_birth,
#         google_id=google_id,
#         login_type="google",
#         vibe_as=vibe_as,
#         guest_token=guest_token
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# def get_or_create_guest_user(db: Session, device_id: str):
#     user = db.query(User).filter(User.device_id == device_id).first()
    
#     if not user:
#         # Create new guest user if not found
#         user = User(device_id=device_id, is_guest=True)  # Assuming is_guest is a column to mark guest users
#         db.add(user)
#         db.commit()
#         db.refresh(user)
    
#     return user

from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.user import User, generate_incremental_user_id
from app.utils.auth import verify_password, get_password_hash
from app.core.security import create_access_token
from app.crud.user import (
    get_user_by_email,
    get_user_by_guest_token,
    create_guest_user,
    create_email_user,
    create_google_user,
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_user(
    db: Session,
    email: str | None,
    password: str | None,
    login_type: str,
    vibe_as: str | None,
    guest_token: str | None = None,
    name: str | None = None
) -> User:
    if login_type in ("email", "google"):
        if login_type == "email" and not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password required")
        existing = get_user_by_email(db, email)
        if existing:
            return existing
        return create_email_user(db, email, password, login_type, vibe_as)

    if login_type == "guest":
        if not guest_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="guest_token required")
        existing = get_user_by_guest_token(db, guest_token)
        if existing:
            return existing
        return create_guest_user(db, guest_token, vibe_as)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login_type")

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_token(user: User) -> str:
    data = {"sub": user.user_id}
    return create_access_token(data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

# def get_or_create_google_user(
#     db: Session,
#     email: str,
#     name: str = None,
#     profile_image: str = None,
#     gender: str = None,
#     date_of_birth: str = None,
#     google_id: str = None,
#     vibe_as: str = None,
#     guest_token: str = None
# ) -> User:
#     user = get_user_by_email(db, email)
#     if user:
#         return user
#     return create_google_user(
#         db=db,
#         email=email,
#         name=name,
#         profile_image=profile_image,
#         gender=gender,
#         date_of_birth=date_of_birth,
#         google_id=google_id,
#         vibe_as=vibe_as,
#         guest_token=guest_token
#     )

# services/auth.py

def get_or_create_google_user(
    db: Session,
    email: str,
    name: str = None,
    profile_image: str = None,
    gender: str = None,
    date_of_birth: str = None,
    google_id: str = None,
    vibe_as: str = None,
    guest_token: str = None
) -> User:
    user = get_user_by_email(db, email)
    if user:
        return user
    return create_google_user(
        db,
        email=email,
        name=name,
        profile_image=profile_image,
        gender=gender,
        date_of_birth=date_of_birth,
        google_id=google_id,
        vibe_as=vibe_as,
        guest_token=guest_token
    )

def create_google_user(
    db: Session,
    email: str,
    name: str = None,
    profile_image: str = None,
    gender: str = None,
    date_of_birth: str = None,
    google_id: str = None,
    vibe_as: str = None,
    guest_token: str = None
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

def get_or_create_guest_user(db: Session, device_id: str) -> User:
    user = db.query(User).filter(User.device_id == device_id).first()

    if not user:
        # Create new guest user if not found
        user = User(
            user_id=generate_incremental_user_id(db),
            device_id=device_id,
            is_guest=True  # Assuming `is_guest` exists in your User model
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
