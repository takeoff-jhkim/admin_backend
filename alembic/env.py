from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine  # ← create_engine 추가
from alembic import context

import os
from dotenv import load_dotenv
from app.database import Base, DATABASE_URL
from app import models

load_dotenv()

# Alembic config
config = context.config

# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

target_metadata = Base.metadata  # ✅ 여긴 꼭 Base.metadata 사용

def run_migrations_offline() -> None:
    url = DATABASE_URL  # 직접 사용
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)  # ✅ 여기도 직접 사용

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
