from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Создаём async движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,       # SQL логи в DEBUG режиме
    pool_size=10,               # Размер пула соединений
    max_overflow=20,            # Максимум дополнительных соединений
    pool_pre_ping=True,         # Проверка соединения перед использованием
    pool_recycle=3600,          # Пересоздавать соединения каждый час
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,     # Не сбрасывать объекты после commit
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


async def get_db() -> AsyncSession:
    """
    Dependency для FastAPI — создаёт сессию БД на время запроса,
    автоматически закрывает и откатывает при ошибке
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()