from decimal import Decimal
from functools import lru_cache
from typing import Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ===== Приложение =====
    APP_NAME: str = "Flower Shop"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FRONTEND_URL: str = "https://flowers.example.ru"

    # ===== База данных =====
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # ===== Redis =====
    REDIS_URL: str = "redis://redis:6379/0"

    # ===== ЮKassa / YooMoney =====
    YOOKASSA_SHOP_ID: str           # Идентификатор магазина
    YOOKASSA_SECRET_KEY: str        # Секретный ключ магазина
    # Секрет для верификации вебхука (настраивается в ЛК ЮKassa)
    YOOKASSA_WEBHOOK_SECRET: Optional[str] = None

    # ===== Бонусная система =====
    BONUS_ACCRUAL_PERCENT: float = 5.0       # 5% от суммы = бонусы
    BONUS_MAX_DEDUCT_PERCENT: float = 30.0   # Макс 30% суммы можно оплатить бонусами
    BONUS_MIN_ORDER_AMOUNT: Decimal = Decimal("500")  # Мин. сумма для начисления бонусов

    # ===== Уровни лояльности =====
    LOYALTY_SILVER_THRESHOLD: int = 1000   # баллов для уровня Серебро
    LOYALTY_GOLD_THRESHOLD: int = 5000     # баллов для уровня Золото

    # ===== Налогообложение (54-ФЗ) =====
    TAX_SYSTEM_CODE: int = 1   # 1 = ОСН, 2 = УСН доходы, ...

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Для Alembic миграций"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()