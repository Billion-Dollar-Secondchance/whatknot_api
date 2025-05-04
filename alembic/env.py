import os
import sys
import pkgutil
import importlib
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- Load values from alembic.ini ---
config = context.config
fileConfig(config.config_file_name)

# --- Add your app's base path ---
sys.path.append(os.getcwd())

# --- Load all models dynamically ---
models_dir = os.path.join(os.getcwd(), "app", "db", "models")
for _, module_name, _ in pkgutil.iter_modules([models_dir]):
    if not module_name.startswith("__"):
        importlib.import_module(f"app.db.models.{module_name}")

# --- Load Base metadata ---
from app.db.base import Base
target_metadata = Base.metadata

# --- Offline Migration ---
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()

# --- Online Migration ---
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        echo=True,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# --- Entry Point ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
