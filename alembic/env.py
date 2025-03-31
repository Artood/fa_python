from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
from main import Base  # Импорт вашей модели

# Подключение конфигурации Alembic
config = context.config

# Настройка логов (если используется файл)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL базы данных (берется из alembic.ini или переменных окружения)
DATABASE_URL = config.get_main_option("sqlalchemy.url")

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

# Определение моделей
target_metadata = Base.metadata

async def run_migrations():
    """Функция для асинхронного выполнения миграций."""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

async def do_run_migrations(connection):
    """Запуск миграций в контексте Alembic."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

# Запуск миграций
if context.is_offline_mode():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
else:
    import asyncio
    asyncio.run(run_migrations())
