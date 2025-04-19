from fastapi import APIRouter,Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.config import settings

from app.db.session import SessionLocal
from app.services.auth import get_or_create_guest_user, create_token
from app.schemas.user import LoginResponse, UserResponse, WrappedResponse

from app.db.session import SessionLocal
from app.schemas.user import (
    UserCreate,
    UserResponse,
    LoginResponse,
    WrappedResponse,
)
from app.services.auth import (
    create_user,
    authenticate_user,
    create_token,
    get_or_create_google_user,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/guest-login")
async def guest_login(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    device_id = body.get("device_id")

    if not device_id:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "failure", "message": "Device ID is required", "data": None}
        )

    user = get_or_create_guest_user(db, device_id=device_id)
    jwt = create_token(user)
    return WrappedResponse(
        status="success",
        message="Guest login successful",
        data=LoginResponse(
            access_token=jwt,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )
    )


# Register user
@router.post("/register", response_model=WrappedResponse)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    create_user(
        db,
        email=payload.email,
        password=payload.password,
        login_type=payload.login_type,
        vibe_as=payload.vibe_as,
        guest_token=payload.guest_token,
    )
    return WrappedResponse(
        status="success",
        message="User registered successfully",
        data=None,
    )


# Login with username and password
@router.post("/login", response_model=WrappedResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": "failure", "message": "Invalid credentials", "data": None}
        )

    token = create_token(user)
    login_data = LoginResponse(
        access_token=token,
        token_type="bearer",
        data=UserResponse.model_validate(user),
    )
    return WrappedResponse(
        status="success",
        message="Login successful",
        data=login_data,
    )


# Login with Google (OAuth)
@router.get("/google-login", response_model=WrappedResponse)
def google_login(
    db: Session = Depends(get_db)
):
    # This is where you'll initiate the OAuth login flow.
    # You can redirect the user to Google OAuth for login.
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    # Replace this with your OAuth library integration for Google login
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success", "message": "Redirecting to Google for login", "data": {"redirect_uri": redirect_uri}},
    )


# Callback after Google login
@router.get("/google-auth", response_model=WrappedResponse)
def google_auth(
    token: str,  # You can pass the token or authorization code received from Google
    db: Session = Depends(get_db)
):
    # Handle Google OAuth callback and user authentication
    if not token:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "failure", "message": "Google authentication failed", "data": None}
        )

    # Handle token exchange and user creation/lookup here
    user = get_or_create_google_user(
        db,
        token=token,  # Or you can pass specific user info like email, name, etc. from Google
    )

    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "failure", "message": "User creation failed", "data": None}
        )

    token = create_token(user)
    login_data = LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )

    return WrappedResponse(
        status="success",
        message="Google login successful",
        data=login_data,
    )
