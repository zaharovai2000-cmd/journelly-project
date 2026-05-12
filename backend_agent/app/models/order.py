from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    Numeric, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"           # Ожидает оплаты
    PAID = "paid"                 # Оплачен
    PROCESSING = "processing"     # В обработке
    DELIVERING = "delivering"     # Доставляется
    DELIVERED = "delivered"       # Доставлен
    CANCELLED = "cancelled"       # Отменён
    REFUNDED = "refunded"         # Возврат


class DeliveryType(str, enum.Enum):
    DELIVERY = "delivery"         # Доставка курьером
    PICKUP = "pickup"             # Самовывоз


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # nullable для гостевых

    # Статус и тип
    status = Column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True
    )
    delivery_type = Column(
        Enum(DeliveryType),
        default=DeliveryType.DELIVERY,
        nullable=False
    )

    # Финансы
    subtotal = Column(Numeric(10, 2), nullable=False)       # Сумма без скидок
    bonus_deducted = Column(Numeric(10, 2), default=0.00)  # Списанные бонусы
    total_amount = Column(Numeric(10, 2), nullable=False)   # Итоговая сумма к оплате

    # Получатель
    recipient_name = Column(String(100), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    recipient_email = Column(String(255), nullable=True)

    # Доставка
    delivery_address = Column(Text, nullable=True)
    delivery_city = Column(String(100), nullable=True)
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    delivery_time_from = Column(String(5), nullable=True)   # "10:00"
    delivery_time_to = Column(String(5), nullable=True)     # "14:00"
    courier_comment = Column(Text, nullable=True)

    # Подарок
    is_gift = Column(Boolean, default=False)
    gift_message = Column(Text, nullable=True)

    # Технические поля
    payment_method = Column(String(50), nullable=True)   # yookassa, cash
    notes = Column(Text, nullable=True)                  # Внутренние заметки

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи ORM
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)
    bonus_transactions = relationship("BonusTransaction", back_populates="order")

    def __repr__(self):
        return f"<Order id={self.id} status={self.status} total={self.total_amount}>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    bouquet_id = Column(Integer, ForeignKey("bouquets.id"), nullable=False)

    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)  # Цена на момент заказа (фиксируется!)
    name = Column(String(200), nullable=False)       # Название на момент заказа

    # Связи
    order = relationship("Order", back_populates="items")
    bouquet = relationship("Bouquet", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem order_id={self.order_id} bouquet_id={self.bouquet_id}>"