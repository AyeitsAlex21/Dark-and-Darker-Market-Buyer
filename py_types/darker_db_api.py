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
    rarity: Optional[str] = None
    price: Optional[str] = None
    price_per_unit: Optional[float] = None
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

    def to_query_params(self) -> dict[str, Any]:
        """Convert model to query params, handling nested primary/secondary attributes.
        
        Transforms nested dicts like secondary={"strength": "2:3"} into 
        secondary[strength]=2:3 format expected by the API.
        """
        params = self.model_dump(by_alias=True, exclude_none=True)
        
        # Handle primary attributes
        if "primary" in params and params["primary"]:
            primary_dict = params.pop("primary")
            for key, value in primary_dict.items():
                params[f"primary[{key}]"] = value
        
        # Handle secondary attributes
        if "secondary" in params and params["secondary"]:
            secondary_dict = params.pop("secondary")
            for key, value in secondary_dict.items():
                params[f"secondary[{key}]"] = value
        
        return params


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
    price_per_unit: float
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
