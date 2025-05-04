from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, PyJWTError
from app.config import settings
from app.crud.user import get_user_by_id
from app.db.session import get_db
from jose import jwt, JWTError
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_token(token: str):
    print("🔑 verify_token called with token:", token)
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        print("payload==>", payload)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except (jwt.InvalidSignatureError, jwt.PyJWTError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )



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

