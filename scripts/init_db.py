
from app.db.base import Base
from app.db.session import engine

# Import models here so Base.metadata knows about them
import app.db.models.user
import app.db.models.partner_pairing
import app.db.models.mystery_moodbox
import app.db.models.mystery_moodbox_questions 
import app.db.models.day_question_mapping

def init():
    Base.metadata.create_all(bind=engine)
    print("✅ Done.")

if __name__ == "__main__":
    init()
