# app/api/routes/mystery_moodbox.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.db.models.mystery_moodbox import MysteryMoodbox, MoodStatusEnum
from app.db.models.mystery_moodbox_questions import MysteryMoodboxQuestion
from app.db.models.partner_pairing import PartnerPairing
from app.schemas.mystery_moodbox import SubmitMoodRequest,MoodPromptAnswerRequest,AddMoodboxQuestionRequest
from app.dependencies.auth import get_current_user, get_db
from app.db.models.user import User
from sqlalchemy import or_
from uuid import uuid4
from app.utils.response_format import success_response, failure_response

router = APIRouter()


@router.post("/questions/add")
async def add_moodbox_question(
    body: AddMoodboxQuestionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        new_question = MysteryMoodboxQuestion(
            id=str(uuid4()),
            question_text=body.question.strip(),
            question_type=body.question_type,
            options=body.options,
            created_by_type=current_user.type,   # or map from user object
            created_by_id=current_user.user_id,
        )
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        return success_response(
            message="Question saved successfully.",
            data={"question_id": new_question.id}
        )
    except Exception as e:
        return failure_response(message="Failed to save question.", data=str(e))
    

@router.get("/get-question")
def get_today_question(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    # 1) Find the user's active pairing
    pairing = db.query(PartnerPairing).filter(
        or_(
            PartnerPairing.user_id == current_user.user_id,
            PartnerPairing.partner_id == current_user.user_id,
        ),
        PartnerPairing.pair_status == "active"
    ).first()

    if not pairing:
        return failure_response(message="User is not paired with anyone.")

    # 2) Find today's mood prompt for the current user
    moodbox = db.query(MysteryMoodbox).filter(
        MysteryMoodbox.pair_id == pairing.pair_id,
        MysteryMoodbox.prompt_date == today,
        MysteryMoodbox.prompted_user_id == current_user.user_id
    ).first()

    if not moodbox:
        return failure_response(message="No question has been prompted to you today.")

    # 3) Get the associated question
    question = db.query(MysteryMoodboxQuestion).filter(
        MysteryMoodboxQuestion.id == moodbox.question_id
    ).first()

    if not question:
        return failure_response(message="Question not found.")

    return success_response(
        message="Question fetched successfully.",
        data={
            "mood_id": str(moodbox.mood_id),
            "question_id": question.id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "options": question.options,
            "mood_status": moodbox.mood_status
        }
    )

    
# @router.post("/question")
# def submit_mood(
#     body: SubmitMoodRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     today = date.today()
#     print("🔑 current_user:", current_user.user_id)
#     # 1) Find the user's active pairing
#     pairing = db.query(PartnerPairing).filter(or_(
#         PartnerPairing.user_id == current_user.user_id,
#         PartnerPairing.partner_id == current_user.user_id
#     ),
#     PartnerPairing.pair_status == "active").first()
    

#     # Debug: print the pairing query result
#     print(f"Pairing result: {pairing}")

#     if not pairing:
#         return {"status": "failure", "message": "User is not paired with anyone."}

#     pair_id = pairing.pair_id

#     # 2) Look up today's prompt for *this* user
#     moodbox = (
#         db.query(MysteryMoodbox)
#           .filter(
#               MysteryMoodbox.pair_id == pair_id,
#               MysteryMoodbox.prompt_date == today,
#               MysteryMoodbox.prompted_user_id == current_user.user_id
#           )
#           .first()
#     )
#     if not moodbox:
#         return {"status": "failure", "message": "No mood prompt for you today."}

#     # 3) Check whether they've already answered
#     if moodbox.mood_status != MoodStatusEnum.PROMPTED:
#         return {"status": "failure", "message": "Mood already submitted or guessed."}

#     # 4) Save their answer
#     moodbox.mood = body.mood
#     moodbox.explanation = body.explanation
#     moodbox.mood_status = MoodStatusEnum.ANSWERED
#     moodbox.updated_at = datetime.utcnow()

#     db.add(moodbox)
#     db.commit()
#     db.refresh(moodbox)

#     return {
#         "status": "success",
#         "data": {
#             "mood_id": str(moodbox.mood_id),
#             "mood": moodbox.mood,
#             "explanation": moodbox.explanation,
#         }
#     }

# @router.post("/answer")
# def submit_mood_prompt_answer(
#     body: MoodPromptAnswerRequest,
#     db: Session = Depends(get_db),
#     current_user = Depends(get_current_user)
# ):
#     # Validate prompt exists and is meant for this user
#     prompt = db.query(MoodPrompt).filter(
#         MoodPrompt.prompt_id == body.prompt_id,
#         MoodPrompt.receiver_id == current_user.user_id
#     ).first()

#     if not prompt:
#         return failure_response(message="Invalid prompt or not authorized.")

#     # Check if already answered
#     existing = db.query(MoodPromptResponse).filter(
#         MoodPromptResponse.prompt_id == body.prompt_id,
#         MoodPromptResponse.user_id == current_user.user_id
#     ).first()
#     if existing:
#         return failure_response(message="You have already answered this prompt.")

#     # Save answer
#     new_response = MoodPromptResponse(
#         response_id=str(uuid4()),
#         prompt_id=body.prompt_id,
#         user_id=current_user.user_id,
#         answer=body.answer,
#         created_at=datetime.utcnow()
#     )
#     db.add(new_response)
#     db.commit()

#     return success_response(message="Answer submitted successfully.")
