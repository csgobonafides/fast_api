from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from src.db.models import Base
from src.core.settings import get_db_settings

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def run_migrations_online() -> None:
    db_conf = get_db_settings()
    connectable = create_engine(db_conf.dsn())

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
