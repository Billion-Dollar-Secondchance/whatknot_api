# from sqlalchemy.orm import declarative_base

# # Create a single shared Base for all models
# Base = declarative_base()

# # Import all models here so that they get registered with Base.metadata
# # e.g.,
# from app.db.models.user import User
# # from app.db.models.partner import PartnerPairing
# # from app.db.models.checkin import DailyCheckIn
# # etc.

from sqlalchemy.ext.declarative import declarative_base
import importlib

Base = declarative_base()

# Delaying the import of models
def import_models():
    importlib.import_module('app.db.models.user')
    # Add more models as needed

import_models()
