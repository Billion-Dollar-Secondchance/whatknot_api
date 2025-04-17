# app/init_db.py
from app.db import engine, Base

# Import all models to register them with Base metadata
from app.db.models import user
# from app.db.models import digital_letter, daily_checkin, etc.

def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done.")

if __name__ == "__main__":
    init()
