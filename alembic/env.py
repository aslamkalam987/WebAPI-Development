from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Base  # Assuming your models are in app.models
from app.config import settings
from urllib.parse import quote

# Alembic Config object to access values within the .ini file.
config = context.config

# URL-encode the password to handle special characters
password = quote(settings.database_password, safe='')
sqlalchemy_url = f"postgresql+psycopg2://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Setup logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata from your models to support autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=sqlalchemy_url,  # Directly use the URL
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {"sqlalchemy.url": sqlalchemy_url},  # Pass the URL here
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
