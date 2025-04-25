# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.schemas.user import UserUpdateRequest, WrappedResponse, UserResponse
# from app.services.auth import update_user_details
# from app.dependencies.auth import get_current_user
# from app.db.models.user import User

# router = APIRouter()

# @router.post("/update-profile", response_model=WrappedResponse)
# def update_profile(
#     payload: UserUpdateRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     user = update_user_details(
#        db=db,
#         user=current_user,
#         name=payload.name,
#         email=payload.email,
#         profile_image=payload.profile_image,
#         gender=payload.gender,
#         date_of_birth=payload.date_of_birth,
#         vibe_as=payload.vibe_as,
#     )

#     return WrappedResponse(
#         status="success",
#         message="Profile updated successfully",
#         data=UserResponse.model_validate(user) 
#     )


# from fastapi import APIRouter, Depends, HTTPException, status
# from pydantic import EmailStr
# from app.schemas.user import UserUpdateRequest, WrappedResponse, UserResponse
# from app.services.auth import get_current_user
# from app.db.models.user import User
# from fastapi.responses import JSONResponse

# router = APIRouter()

# @router.post("/update_profile", response_model=WrappedResponse)
# async def update_profile(
#     update_request: UserUpdateRequest, 
#     current_user: UserResponse = Depends(get_current_user)
# ):
#     try:
#         # Get the current user from DB
#         user = await User.get(id=current_user.user_id)

#         # Update fields only if provided in the request
#         if update_request.name:
#             user.name = update_request.name
#         if update_request.email:
#             user.email = update_request.email
#         if update_request.profile_image:
#             user.profile_image = update_request.profile_image
#         if update_request.gender:
#             user.gender = update_request.gender
#         if update_request.date_of_birth:
#             user.date_of_birth = update_request.date_of_birth
#         if update_request.vibe_as:
#             user.vibe_as = update_request.vibe_as

#         # Save the updated user to the DB
#         await user.save()

#         # Return the updated user response
#         updated_user_response = UserResponse.from_orm(user)

#         return WrappedResponse(
#             status="success",
#             message="Profile updated successfully",
#             data=updated_user_response
#         )

#     except Exception as e:
#          return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"status": "failure", "message": "An error occurred while updating profile", "data": None}
#         )
#         # raise HTTPException(
#         #     status_code=status.HTTP_400_BAD_REQUEST,
#         #     detail="An error occurred while updating profile"
            
#         # )
    
    
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

        db.commit()
        db.refresh(user)

        return WrappedResponse(
            status="success",
            message="Profile updated successfully",
            data=UserResponse.model_validate(user)
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "status": "failure",
                "message": "An error occurred while updating profile",
                "data": None
            }
        )

