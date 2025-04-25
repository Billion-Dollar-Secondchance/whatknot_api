import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# this loads the values from alembic.ini
config = context.config
fileConfig(config.config_file_name)

# add your app's path so Python can import it
import sys
sys.path.append(os.getcwd())

# import your Base (and all models, indirectly)
from app.db.base import Base
# make sure app/db/models/user.py is importable so Base.metadata is populated
import app.db.models.user
from app.db.models import partner_pairing 

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

