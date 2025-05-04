from datetime import timedelta
import random
import string
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,Depends
from app.db.models.user import User, generate_incremental_user_id
from app.utils.auth import verify_password, get_password_hash
from app.core.security import create_access_token
from app.crud.user import update_user_profile
from app.core.config import settings 
from app.db.session import get_db
# from app.services.auth import generate_unique_pairing_code 
from app.crud.user import (
    get_user_by_email,
    get_user_by_guest_token,
    create_guest_user,
    create_email_user,
    create_google_user,
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 15 * 24 * 60

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

def generate_unique_pairing_code(db: Session):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exists = db.query(User).filter(User.pairing_code == code).first()
        if not exists:
            print(f"Generated pairing code: {code}")
            return code

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
    guest_token: str = None,
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
        guest_token=guest_token,
        pairing_code=generate_unique_pairing_code(db)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_or_create_guest_user(db: Session, device_id: str) -> User:
    # look up by your existing guest_token column
    user = db.query(User).filter(User.guest_token == device_id).first()
    if user:
        return user

    # create a brand-new guest user
    user = User(
        user_id=generate_incremental_user_id(db),
        login_type="guest",
        device_id=device_id,
        guest_token=device_id,
        vibe_as=None,        # or whatever your default is
        is_active=True       # assuming you have this field
        # CREATED_AT will be autofilled by your model’s server_default
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
def update_user_details(
    db: Session,
    user: User,
    name: str | None = None,
    email: str | None = None,
    profile_image: str | None = None,
    gender: str | None = None,
    date_of_birth: str | None = None,
    vibe_as: str | None = None
) -> User:
    if name is not None:
        user.name = name
    if email is not None:
        user.email = email
    if profile_image is not None:
        user.profile_image = profile_image
    if gender is not None:
        user.gender = gender
    if date_of_birth is not None:
        user.date_of_birth = date_of_birth
    if vibe_as is not None:
        user.vibe_as = vibe_as

    db.commit()
    db.refresh(user)
    return user

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = db.query(User).filter(User.user_id == user_id).first()
#     if user is None:
#         raise credentials_exception
#     return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user_id: str = payload.get("sub")
    role: str = payload.get("role")  # ← pull role claim
    print("role")
    if not user_id:
        raise HTTPException(401, "Invalid token payload")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    # Attach the role from the token onto the SQLAlchemy object so your guard can see it:
    setattr(user, "role", role)
    return user

