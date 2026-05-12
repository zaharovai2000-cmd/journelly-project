from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Bouquet(Base):
    __tablename__ = "bouquets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    composition = Column(Text, nullable=True)  # Состав букета

    price = Column(Numeric(10, 2), nullable=False)

    # Изображения: главное + галерея
    image_url = Column(String(500), nullable=True)
    gallery_urls = Column(Text, nullable=True)  # JSON строка с массивом URL

    # Категоризация
    category = Column(String(100), nullable=True, index=True)  # roses, mixed, etc.
    occasion = Column(String(100), nullable=True, index=True)  # birthday, wedding, etc.
    size = Column(String(20), nullable=True)     # small, medium, large
    color_scheme = Column(String(100), nullable=True)  # red, white, mixed

    # Статусы
    in_stock = Column(Boolean, default=True, nullable=False, index=True)
    is_hit = Column(Boolean, default=False, nullable=False)    # Хит продаж
    is_new = Column(Boolean, default=False, nullable=False)    # Новинка
    is_active = Column(Boolean, default=True, nullable=False)  # Видимость

    # Метрики
    sort_order = Column(Integer, default=0)  # Ручная сортировка
    views_count = Column(Integer, default=0)
    orders_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи
    order_items = relationship("OrderItem", back_populates="bouquet")

    def __repr__(self):
        return f"<Bouquet id={self.id} name={self.name} price={self.price}>"