# src/rental_compare/schemas/listing_data.py
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class ListingDataBase(BaseModel):
    scraped_at: datetime
    price: float
    currency: str
    listing_id: int
    platform_id: int
    rating: Optional[float] = None
    reviews_count: Optional[int] = None

    @validator('scraped_at')
    def check_not_future(cls, v: datetime) -> datetime:
        if v > datetime.utcnow():
            raise ValueError('scraped_at cannot be in the future')
        return v

    @validator('price')
    def price_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('price must be positive')
        return v

    @validator('currency')
    def currency_format(cls, v: str) -> str:
        code = v.strip().upper()
        if len(code) != 3 or not code.isalpha():
            raise ValueError('currency must be a 3-letter alphabetic code')
        return code

    @validator('listing_id', 'platform_id', 'reviews_count')
    def non_negative_int(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError('must be non-negative integer')
        return v

class ListingDataCreate(ListingDataBase):
    pass

class ListingDataUpdate(BaseModel):
    scraped_at: datetime | None = None
    price: float | None = None
    currency: str | None = None
    listing_id: int | None = None
    platform_id: int | None = None
    rating: float | None = None
    reviews_count: int | None = None

    @validator('price')
    def price_positive_optional(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError('if set, price must be positive')
        return v

    @validator('currency')
    def currency_optional_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        code = v.strip().upper()
        if len(code) != 3 or not code.isalpha():
            raise ValueError('currency must be a 3-letter alphabetic code')
        return code

class ListingDataRead(ListingDataBase):
    id: int

    class Config:
        orm_mode = True