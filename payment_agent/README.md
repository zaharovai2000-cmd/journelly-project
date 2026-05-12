# Интеграция ЮMoney (YooKassa) для лендинга букетов

## 📋 Что сделано

1. **Модели базы данных** (`app/models/`) — созданы три взаимосвязанных таблицы: `payments` (платёж ЮKassa с идентификатором транзакции), `orders` (заказ со статусами и полем для бонусного списания), `bonus_transactions` (история начислений и списаний баллов). Связи: один заказ → один платёж → много бонусных транзакций

2. **Сервис ЮKassa** (`app/services/yookassa_service.py`) — инкапсулирует всю логику работы с API: создание платежа, проверку SHA-1 подписи вебхука, запрос статуса, возврат средств. Используем официальный SDK `yookassa` вместо прямых HTTP-запросов — это снижает риск ошибок

3. **Webhook-обработчик** (`app/routers/payments.py`) — принимает POST-уведомления от ЮKassa, верифицирует подпись, атомарно обновляет статус заказа и начисляет бонусы в одной транзакции БД. Идемпотентный — повторный вебхук не создаёт дублей

4. **Сервис бонусов** (`app/services/bonus_service.py`) — логика начисления (5% от суммы заказа), списания (максимум 30% суммы заказа), проверки баланса. Все операции атомарны через `SELECT FOR UPDATE` чтобы избежать гонки при параллельных запросах

5. **Роуты платежей** — три эндпоинта: `POST /create` (создать платёж с учётом бонусов), `POST /webhook` (вебхук от ЮKassa), `GET /status/{order_id}` (статус заказа для фронтенда), `POST /refund/{order_id}` (возврат)

6. **React компонент `CheckoutForm`** — встроенный виджет ЮKassa через динамически загружаемый `checkout.js`, без редиректа. Форма в три шага: данные доставки → списание бонусов → оплата. Состояние управляется через Zustand

7. **Хук `useYooKassa`** (`src/hooks/useYooKassa.ts`) — инкапсулирует инициализацию виджета, обработку токена подтверждения, polling статуса заказа каждые 3 секунды после оплаты

8. **Хук `useBonusDeduction`** (`src/hooks/useBonusDeduction.ts`) — логика ползунка для выбора суммы списания, реальный расчёт скидки и итоговой суммы к оплате картой

9. **Соответствие 54-ФЗ** — в payload создания платежа передаётся объект `receipt` с позициями чека, ставкой НДС, системой налогообложения. ЮKassa автоматически отправляет чек в ОФД и покупателю на email

10. **Docker и миграции** — `Dockerfile` для продакшена, Alembic-миграция создаёт все три таблицы с индексами, `.env.example` с полным набором переменных окружения

---

## 🗄 Модели базы данных

---

## ⚙️ Конфигурация

---

## 🏦 Сервис ЮKassa

---

## 🎁 Сервис бонусов

```python
# app/services/bonus_service.py
import logging
from decimal import Decimal, ROUND_DOWN
from typing import Optional
from uuid import UUID

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.payment import BonusTransaction, BonusTransactionType, Order

logger = logging.getLogger(__name__)

class BonusService:
    """
    Сервис управления бонусными баллами.

    Правила:
    - 1 рубль = 1 бонусный балл
    - Начисляется 5% от суммы ОПЛАЧЕННОГО заказа (после списания бонусов)
    - Можно оплатить до 30% суммы заказа бонусами
    - Минимальная сумма заказа для начисления: 500 руб.
    - Бонусы начисляются только после успешной оплаты (не при создании заказа)
    """

    @staticmethod
    async def get_user_balance(
        user_id: UUID,
        session: AsyncSession,
    ) -> int:
        """Получить текущий баланс бонусов пользователя"""
        # Берём последнюю транзакцию для получения актуального баланса
        result = await session.execute(
            select(BonusTransaction.balance_after)
            .where(BonusTransaction.user_id == user_id)
            .order_by(BonusTransaction.created_at.desc())
            .limit(1)
        )
        row = result.scalar_one_or_none()
        return row or 0

    @staticmethod
    async def get_user_total_accrued(
        user_id: UUID,
        session: AsyncSession,
    ) -> int:
        """Сумма всех начислений — для определения уровня лояльности"""
        result = await session.execute(
            select(func.sum(BonusTransaction.amount))
            .where(
                BonusTransaction.user_id == user_id,
                BonusTransaction.transaction_type == BonusTransactionType.ACCRUAL,
            )
        )
        return result.scalar_one_or_none() or 0

    @staticmethod
    def calculate_max_deductible(order_amount: Decimal) -> int:
        """
        Рассчитать максимальное количество бонусов, которое можно списать.

        Правило: не более 30% суммы заказа.
        Например: заказ 1000 руб → можно списать до 300 баллов.
        """
        max_deduct = order_amount * Decimal(str(settings.BONUS_MAX_DEDUCT_PERCENT / 100))
        # Округляем вниз до целого (баллы — целые числа)
        return int(max_deduct.quantize(Decimal("1"), rounding=ROUND_DOWN))

    @staticmethod
    def calculate_accrual(paid_amount: Decimal) -> int:
        """
        Рассчитать количество начисляемых бонусов.

        5% от фактически оплаченной суммы (рублями, не бонусами).
        """
        if paid_amount < settings.BONUS_MIN_ORDER_AMOUNT:
            return 0

        accrual = paid_amount * Decimal(str(settings.BONUS_ACCRUAL_PERCENT / 100))
        return int(accrual.quantize(Decimal("1"), rounding=ROUND_DOWN))

    @staticmethod
    async def validate_deduction(
        user_id: UUID,
        bonus_to_deduct: int,
        order_amount: Decimal,
        session: AsyncSession,
    ) -> dict:
        """
        Валидация запроса на списание бонусов.

        Возвращает:
        - is_valid: можно ли провести списание
        - max_allowed: максимально допустимое списание
        - actual_deduct: фактическое количество к списанию
        - final_amount: итоговая сумма к оплате рублями
        - error: текст ошибки если is_valid=False
        """
        if bonus_to_deduct < 0:
            return {"is_valid": False, "error": "Количество бонусов не может быть отрицательным"}

        if bonus_to_deduct == 0:
            return {
                "is_valid": True,
                "actual_deduct": 0,
                "final_amount": order_amount,
                "max_allowed": BonusService.calculate_max_deductible(order_amount),
            }

        # Проверяем баланс
        current_balance = await BonusService.get_user_balance(user_id, session)
        if bonus_to_deduct > current_balance:
            return {
                "is_valid": False,
                "error": f"Недостаточно бонусов. Доступно: {current_balance}",
                "current_balance": current_balance,
            }

        # Проверяем лимит 30%
        max_deductible = BonusService.calculate_max_deductible(order_amount)
        actual_deduct = min(bonus_to_deduct, max_deductible)

        final_amount = order_amount - Decimal(str(actual_deduct))
        # Минимальная сумма к оплате рублями — 1 копейка
        if final_amount < Decimal("0.01"):
            final_amount = Decimal("0.01")
            actual_deduct = int(order_amount - Decimal("0.01"))

        return {
            "is_valid": True,
            "actual_deduct": actual_deduct,
            "final_amount": final_amount,
            "max_allowed": max_deductible,
            "current_balance": current_balance,
        }

    @staticmethod
    async def deduct_bonuses(
        user_id: UUID,
        order_id: UUID,
        amount: int,
        session: AsyncSession,
    ) -> BonusTransaction:
        """
        Списать бонусы при создании заказа.

        ВАЖНО: вызывать внутри транзакции БД.
        Использует SELECT FOR UPDATE для предотвращения гонки.
        """
        # Блокируем строки для этого пользователя
        result = await session.execute(
            select(BonusTransaction)
            .where(BonusTransaction.user_id == user_id)
            .order_by(BonusTransaction.created_at.desc())
            .limit(1)
            .with_for_update()  # Блокировка на время транзакции
        )

---
## 📁 Созданные файлы
- [payment.py](payment.py)
- [config.py](config.py)
- [yookassa_service.py](yookassa_service.py)