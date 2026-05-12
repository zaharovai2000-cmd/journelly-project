## 📋 Что сделано

1. **Структура проекта** — создаём папку `app/` с модулями `models/`, `routers/`, `services/`, `schemas/`, `core/` — это стандартная архитектура FastAPI, где каждая папка отвечает за свой слой (данные, маршруты, бизнес-логика, валидация, настройки)

2. **База данных** — используем PostgreSQL через SQLAlchemy ORM с async-драйвером `asyncpg`. Все таблицы описаны в `models/` — Users, Bouquets, Orders, OrderItems, BonusTransactions, Payments

3. **Миграции** — Alembic автоматически генерирует SQL-миграции из моделей SQLAlchemy, файл `alembic/versions/001_initial.py` создаёт все таблицы с нуля

4. **Аутентификация** — JWT токены (access на 30 минут + refresh на 30 дней), пароли хешируются через bcrypt, реализовано в `core/security.py` и `routers/auth.py`

5. **Каталог букетов** — простые GET-эндпоинты с фильтрацией по категории, цене, наличию. Пагинация через `limit/offset`

6. **Заказы** — при создании заказа проверяется наличие товара, считается итоговая сумма, опционально списываются бонусные баллы (до 30% суммы)

7. **Интеграция ЮМани** — `services/yoomoney.py` создаёт платёж через API YooKassa, webhook-эндпоинт принимает уведомления, верифицирует SHA-1 подпись и меняет статус заказа

8. **Система бонусов** — `services/bonus.py` начисляет 5% от суммы заказа после успешной оплаты, списывает баллы при оформлении, ведёт историю транзакций в таблице `bonus_transactions`

9. **Docker Compose** — поднимает три контейнера: FastAPI приложение, PostgreSQL база данных, Redis для кеширования сессий и rate-limiting

10. **Зависимости между файлами**: `main.py` → подключает роутеры → роутеры вызывают сервисы → сервисы работают с моделями → модели описывают таблицы БД → схемы Pydantic валидируют входные/выходные данные на каждом уровне

---

## 📁 Структура проекта

---

## ⚙️ Core — Конфигурация и безопасность

---

## 🗄️ Модели базы данных

---

## 📐 Pydantic Схемы (валидация данных)

```python
# app/schemas/order.py
from pydantic import BaseModel, field_validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

class OrderItemRequest(BaseModel):
    bouquet_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v):
        if v < 1:
            raise ValueError("Количество должно быть не менее 1")
        if v > 99:
            raise ValueError("Максимальное количество — 99")
        return v

class CreateOrderRequest(BaseModel):
    items: List[OrderItemRequest]

    # Получатель
    recipient_name: str
    recipient_phone: str
    recipient_email: Optional[str] = None

    # Доставка
    delivery_type: str = "delivery"   # delivery / pickup
    delivery_address: Optional[str] = None
    delivery_city: Optional[str] = None
    delivery_date: Optional[datetime] = None
    delivery_time_from: Optional[str] = None
    delivery_time_to: Optional[str] = None
    courier_comment: Optional[str] = None

    # Подарок
    is_gift: bool = False
    gift_message: Optional[str] = None

---
## 📁 Созданные файлы
- [requirements-2.txt](requirements-2.txt)
- [config.py](config.py)
- [database.py](database.py)
- [security.py](security.py)
- [dependencies.py](dependencies.py)
- [__init__.py](__init__.py)
- [user.py](user.py)
- [bouquet.py](bouquet.py)
- [order.py](order.py)
- [payment.py](payment.py)
- [auth.py](auth.py)
- [user-2.py](user-2.py)
- [bouquet-2.py](bouquet-2.py)