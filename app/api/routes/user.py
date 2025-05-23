from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserUpdateRequest, WrappedResponse, UserResponse
from app.db.session import get_db
from app.db.models.user import User
from app.services.auth import get_current_user
from fastapi.responses import JSONResponse
from app.utils.response_format import success_response

router = APIRouter()

@router.post("/update_profile", response_model=WrappedResponse)
def update_profile(
    update_request: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        user = db.query(User).filter(User.user_id == current_user.user_id).first()

        if not user:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "failure",
                    "message": "User not found",
                    "data": None
                }
            )

        if update_request.name:
            user.name = update_request.name
        if update_request.email:
            user.email = update_request.email
        if update_request.profile_image:
            user.profile_image = update_request.profile_image
        if update_request.gender:
            user.gender = update_request.gender
        if update_request.date_of_birth:
            user.date_of_birth = update_request.date_of_birth
        if update_request.vibe_as:
            user.vibe_as = update_request.vibe_as
        if update_request.interested_in:
            user.interested_in = update_request.interested_in 
        if update_request.mobile_number:
            user.mobile_number = update_request.mobile_number
        if update_request.height:
            user.height = update_request.height
        if update_request.audio_intro:
            user.audio_intro = update_request.audio_intro
        if update_request.video_intro:
            user.video_intro = update_request.video_intro
        if update_request.image_gallery:
            user.image_gallery = ",".join(update_request.image_gallery)
        if update_request.vibe_keywords:
            user.vibe_keywords = ",".join(update_request.vibe_keywords)
        if update_request.education:
            user.education = update_request.education
        if update_request.location:
            user.location = update_request.location
        if update_request.relationship_goal:
            user.relationship_goal = update_request.relationship_goal

        user.onboarded = True  # ✅ Final flag


        db.commit()
        db.refresh(user)

        return WrappedResponse(
            status="success",
            message="Profile updated successfully",
            data=UserResponse.model_validate(user)
        )

    except Exception as e:
        db.rollback()
        print("UPDATE PROFILE ERROR:", str(e))
        return JSONResponse(
            status_code=400,
            content={
                "status": "failure",
                "message": "An error occurred while updating profile",
                "data": None
            }
        )


@router.get("/profile")
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.user_id == current_user.user_id).first()

    if not user:
        return success_response("User not found", None)

    profile_data = {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "profile_image": user.profile_image,
        "gender": user.gender,
        "date_of_birth": user.date_of_birth,
        "vibe_as": user.vibe_as,
        "interested_in": user.interested_in,
        "mobile_number": user.mobile_number,
        "height": user.height,
        "audio_intro": user.audio_intro,
        "video_intro": user.video_intro,
        "image_gallery": user.image_gallery.split(",") if user.image_gallery else [],
        "vibe_keywords": user.vibe_keywords.split(",") if user.vibe_keywords else [],
        "education": user.education,
        "location": user.location,
        "relationship_goal": user.relationship_goal,
        "onboarded": user.onboarded
    }

    return success_response("User profile fetched successfully", profile_data)
