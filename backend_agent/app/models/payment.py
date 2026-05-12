from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"        # Создан, ожидает оплаты
    SUCCEEDED = "succeeded"    # Успешно оплачен
    CANCELED = "canceled"      # Отменён (пользователем или таймаутом)
    REFUNDED = "refunded"      # Возврат средств


class BonusType(str, enum.Enum):
    ACCRUAL = "accrual"  # Начисление
    DEBIT = "debit"      # Списание


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)

    # Данные от ЮKassa
    yookassa_payment_id = Column(String(100), unique=True, nullable=True, index=True)
    yookassa_confirmation_url = Column(String(500), nullable=True)  # Ссылка на оплату

    status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
        index=True
    )
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")

    # Метаданные платежа
    payment_method_type = Column(String(50), nullable=True)  # bank_card, yoo_money, sbp
    error_code = Column(String(100), nullable=True)
    error_description = Column(Text, nullable=True)

    paid_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    order = relationship("Order", back_populates="payment")

    def __repr__(self):
        return f"<Payment id={self.id} yookassa_id={self.yookassa_payment_id} status={self.status}>"


class BonusTransaction(Base):
    __tablename__ = "bonus_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)  # nullable для ручных начислений

    amount = Column(Numeric(10, 2), nullable=False)  # Сумма операции (всегда положительная)
    type = Column(Enum(BonusType), nullable=False)   # accrual или debit
    balance_after = Column(Numeric(10, 2), nullable=False)  # Баланс ПОСЛЕ операции

    description = Column(String(255), nullable=True)  # Описание для пользователя

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    user = relationship("User", back_populates="bonus_transactions")
    order = relationship("Order", back_populates="bonus_transactions")

    def __repr__(self):
        return f"<BonusTransaction user={self.user_id} type={self.type} amount={self.amount}>"