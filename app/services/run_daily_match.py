import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.db.session import SessionLocal
from app.services.match_single_vibe import match_users_by_vibe

db = SessionLocal()
match_users_by_vibe(db)
db.close()
