from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ItemRarity(str, Enum):
    Poor = "Poor"
    Uncommon = "Uncommon"
    Rare = "Rare"
    Epic = "Epic"
    Legendary = "Legendary"
    Unique = "Unique"
    Artifact = "Artifact"


class MarketOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class MarketQueryParams(BaseModel):
    item_id: Optional[str] = Field(None, alias="item_id")
    item: Optional[str] = None
    archetype: Optional[str] = None
    rarity: Optional[ItemRarity] = None
    price: Optional[str] = None
    price_per_unit: Optional[str] = None
    seller: Optional[str] = None
    quantity: Optional[str] = None
    from_: Optional[datetime] = Field(None, alias="from")
    to: Optional[datetime] = None
    has_sold: Optional[bool] = None
    has_expired: Optional[bool] = None
    primary: Optional[dict[str, str]] = None
    secondary: Optional[dict[str, str]] = None
    order: MarketOrder = MarketOrder.asc
    cursor: Optional[int] = None
    limit: int = Field(default=25, ge=1, le=50)
    condense: Optional[bool] = None

    model_config = {
        "populate_by_name": True,
    }


class MarketPagination(BaseModel):
    count: int
    limit: int
    cursor: Optional[int] = None


class MarketItem(BaseModel):
    id: int
    cursor: int
    item_id: str
    item: str
    archetype: str
    rarity: ItemRarity
    price: int
    price_per_unit: int
    quantity: int
    created_at: datetime
    expires_at: datetime
    has_sold: bool
    has_expired: bool
    seller: Optional[str] = None

    model_config = {
        "extra": "allow",
    }


class MarketMeta(BaseModel):
    method: str
    request: str
    query: dict[str, Any]
    params: list[Any]

    model_config = {
        "extra": "allow",
    }


class MarketResponse(BaseModel):
    version: str
    status: str
    code: int
    query_time: float
    query_date: datetime
    stage: str
    build: str
    patch: int
    meta: MarketMeta
    pagination: MarketPagination
    body: list[MarketItem]
