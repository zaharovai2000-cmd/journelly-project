from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=True)  # nullable для OAuth
    name = Column(String(100), nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Бонусный баланс — храним в БД для быстрого доступа
    # Актуальность поддерживается через триггеры или сервисный слой
    bonus_balance = Column(Numeric(10, 2), default=0.00, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Связи ORM
    orders = relationship("Order", back_populates="user", lazy="select")
    bonus_transactions = relationship(
        "BonusTransaction", back_populates="user", lazy="select"
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} phone={self.phone}>"