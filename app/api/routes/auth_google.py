from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from app.config import settings
from app.db.session import SessionLocal
from app.services.auth import get_or_create_google_user
from app.schemas.user import UserResponse, LoginResponse, WrappedResponse
from app.core.security import create_access_token  # Ensure this is the correct path

router = APIRouter()

# --- OAuth Setup ---
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Step 1: Redirect to Google ---
@router.get("/google-login")
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    request.session["custom_debug_state"] = "check_this"
    print("Session set:", request.session)
    return await oauth.google.authorize_redirect(request, redirect_uri)

# --- Step 2: Google Callback & Token Generation ---
@router.get("/google-auth")
async def google_auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
        user_info = resp.json()
        print("User Info from Google:", user_info)
    except Exception as e:
        print("Google OAuth Error:", str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "failure", "message": "Google authentication failed", "data": None}
        )

    user = get_or_create_google_user(
        db=db,
        email=user_info["email"],
        name=user_info.get("name"),
        profile_image=user_info.get("picture"),
        gender=user_info.get("gender"),
        date_of_birth=None,
        google_id=user_info.get("sub"),
        vibe_as=None,
        guest_token=None
    )

    # ✅ Include role in token payload
    jwt = create_access_token(data={
        "sub": user.user_id,
        "role": user.role
    })

    login_data = LoginResponse(
        access_token='Bearer ' + jwt,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

    return WrappedResponse(
        status="success",
        message="Google login successful",
        data=login_data
    )


