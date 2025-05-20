from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserUpdateRequest, WrappedResponse, UserResponse
from app.db.session import get_db
from app.db.models.user import User
from app.services.auth import get_current_user
from fastapi.responses import JSONResponse

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

