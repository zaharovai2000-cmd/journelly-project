from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal


class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_verified: bool
    bonus_balance: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None


class BonusHistoryItem(BaseModel):
    id: int
    amount: Decimal
    type: str          # accrual / debit
    balance_after: Decimal
    description: Optional[str]
    order_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


class BonusBalanceResponse(BaseModel):
    balance: Decimal
    transactions: list[BonusHistoryItem]
    total_accrued: Decimal    # Всего начислено за всё время
    total_spent: Decimal      # Всего потрачено бонусов