import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Numeric, ForeignKey, DateTime,
    Enum, Text, Integer, Boolean, Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class OrderStatus(str, PyEnum):
    """Статусы жизненного цикла заказа"""
    PENDING = "pending"          # Создан, ожидает оплаты
    PAID = "paid"                # Оплачен
    PROCESSING = "processing"    # Передан в работу флористу
    DELIVERING = "delivering"    # Курьер в пути
    DELIVERED = "delivered"      # Доставлен
    CANCELLED = "cancelled"      # Отменён
    REFUNDED = "refunded"        # Возврат произведён


class PaymentStatus(str, PyEnum):
    """Статусы платежа в ЮKassa"""
    PENDING = "pending"
    WAITING_FOR_CAPTURE = "waiting_for_capture"
    SUCCEEDED = "succeeded"
    CANCELLED = "cancelled"


class BonusTransactionType(str, PyEnum):
    """Тип бонусной операции"""
    ACCRUAL = "accrual"      # Начисление
    DEDUCTION = "deduction"  # Списание
    REFUND = "refund"        # Возврат при отмене заказа


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Суммы
    items_total = Column(Numeric(10, 2), nullable=False)        # Сумма товаров
    delivery_cost = Column(Numeric(10, 2), default=Decimal("0"))
    bonus_deducted = Column(Numeric(10, 2), default=Decimal("0"))  # Списано бонусов
    final_amount = Column(Numeric(10, 2), nullable=False)       # К оплате рублями

    # Статус
    status = Column(
        Enum(OrderStatus, name="order_status_enum"),
        default=OrderStatus.PENDING,
        nullable=False
    )

    # Доставка
    delivery_address = Column(Text, nullable=True)
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    recipient_name = Column(String(200), nullable=True)
    recipient_phone = Column(String(20), nullable=True)
    gift_message = Column(Text, nullable=True)

    # Мета
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    payment = relationship("Payment", back_populates="order", uselist=False)
    items = relationship("OrderItem", back_populates="order")
    bonus_transactions = relationship("BonusTransaction", back_populates="order")
    user = relationship("User", back_populates="orders")

    __table_args__ = (
        Index("idx_orders_user_id", "user_id"),
        Index("idx_orders_status", "status"),
        Index("idx_orders_created_at", "created_at"),
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False,
        unique=True
    )

    # ЮKassa данные
    yookassa_payment_id = Column(String(100), unique=True, nullable=True)
    yookassa_idempotency_key = Column(String(100), unique=True, nullable=False)
    confirmation_url = Column(Text, nullable=True)      # URL для редиректа (если нужен)
    confirmation_token = Column(Text, nullable=True)    # Токен для embedded-виджета

    # Суммы
    amount = Column(Numeric(10, 2), nullable=False)     # Фактическая сумма платежа
    currency = Column(String(3), default="RUB")

    # Статус
    status = Column(
        Enum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING,
        nullable=False
    )

    # Возврат
    refund_id = Column(String(100), nullable=True)
    refunded_amount = Column(Numeric(10, 2), default=Decimal("0"))
    is_refunded = Column(Boolean, default=False)

    # Чек (54-ФЗ)
    receipt_sent = Column(Boolean, default=False)
    receipt_id = Column(String(100), nullable=True)

    # Мета
    raw_response = Column(Text, nullable=True)          # JSON ответа ЮKassa для дебага
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    order = relationship("Order", back_populates="payment")

    __table_args__ = (
        Index("idx_payments_yookassa_id", "yookassa_payment_id"),
        Index("idx_payments_order_id", "order_id"),
    )


class BonusTransaction(Base):
    __tablename__ = "bonus_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)

    transaction_type = Column(
        Enum(BonusTransactionType, name="bonus_transaction_type_enum"),
        nullable=False
    )
    amount = Column(Integer, nullable=False)             # Количество баллов (целое)
    balance_after = Column(Integer, nullable=False)      # Баланс после операции

    description = Column(String(500), nullable=True)    # Пояснение операции
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    order = relationship("Order", back_populates="bonus_transactions")
    user = relationship("User", back_populates="bonus_transactions")

    __table_args__ = (
        Index("idx_bonus_user_id", "user_id"),
        Index("idx_bonus_created_at", "created_at"),
    )


class OrderItem(Base):
    """Позиции заказа (нужны для чека 54-ФЗ)"""
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    bouquet_id = Column(UUID(as_uuid=True), ForeignKey("bouquets.id"), nullable=False)

    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Цена на момент покупки
    total_price = Column(Numeric(10, 2), nullable=False)

    # Для чека
    bouquet_name = Column(String(300), nullable=False)  # Сохраняем название на момент покупки
    vat_code = Column(Integer, default=1)               # Код НДС: 1=без НДС

    order = relationship("Order", back_populates="items")