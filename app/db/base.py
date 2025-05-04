from sqlalchemy.ext.declarative import declarative_base
import importlib

Base = declarative_base()

# Delaying the import of models
def import_models():
    importlib.import_module('app.db.models.user')
    importlib.import_module('app.db.models.partner_pairing')
    importlib.import_module('app.db.models.user')
    importlib.import_module('app.db.models.partner_pairing')
    importlib.import_module('app.db.models.mystery_moodbox')
    importlib.import_module('app.db.models.mystery_moodbox_questions')
    importlib.import_module('app.db.models.day_question_mapping')
    # Add more models as needed

import_models()

