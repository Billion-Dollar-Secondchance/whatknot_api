# migration.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# your DB URL
DATABASE_URL = "postgresql://postgres:Financepeer%40123@localhost:5432/whatknotdb"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

sql = """
-- 1) Make sure gen_random_uuid() is available
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 2) Drop the FK in mystery_moodbox so we can drop questions table
ALTER TABLE mystery_moodbox
  DROP CONSTRAINT IF EXISTS fk_question_id;

-- 3) Drop the old questions table
DROP TABLE IF EXISTS mystery_moodbox_questions;

-- 4) Recreate questions with all the columns you need
CREATE TABLE mystery_moodbox_questions (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    pair_id          VARCHAR     NOT NULL,
    created_by_type  VARCHAR     NOT NULL,
    submitted_by    VARCHAR,
    question_type    VARCHAR     NOT NULL  DEFAULT 'input_text',
    question_text    TEXT        NOT NULL,
    options          JSONB,
    correct_answer   TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- reference back to partner_pairing
    CONSTRAINT fk_pair
      FOREIGN KEY(pair_id)
      REFERENCES partner_pairing(pair_id)
      ON DELETE CASCADE
);

-- 5) Add question_id back onto mystery_moodbox (if missing)
ALTER TABLE mystery_moodbox
  ADD COLUMN IF NOT EXISTS question_id UUID;

-- 6) Re-create the FK between mystery_moodbox → questions
ALTER TABLE mystery_moodbox
  ADD CONSTRAINT fk_question_id
    FOREIGN KEY(question_id)
    REFERENCES mystery_moodbox_questions(id)
    ON DELETE CASCADE;
"""

try:
    session.execute(text(sql))
    session.commit()
    print("✅ Schema updated!")
except Exception as err:
    session.rollback()
    print("❌ Migration failed:", err)
finally:
    session.close()
