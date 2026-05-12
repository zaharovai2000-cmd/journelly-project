from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class BouquetResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    composition: Optional[str]
    price: Decimal
    image_url: Optional[str]
    gallery_urls: Optional[str]  # JSON строка
    category: Optional[str]
    occasion: Optional[str]
    size: Optional[str]
    color_scheme: Optional[str]
    in_stock: bool
    is_hit: bool
    is_new: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class BouquetListResponse(BaseModel):
    items: List[BouquetResponse]
    total: int
    page: int
    per_page: int
    pages: int


class BouquetFilter(BaseModel):
    category: Optional[str] = None
    occasion: Optional[str] = None
    size: Optional[str] = None
    color_scheme: Optional[str] = None
    price_min: Optional[Decimal] = None
    price_max: Optional[Decimal] = None
    in_stock: Optional[bool] = True
    is_hit: Optional[bool] = None
    search: Optional[str] = None