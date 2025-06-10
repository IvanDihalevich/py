from pydantic import BaseModel
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


class ListingDataCreate(ListingDataBase):
    pass


class ListingDataUpdate(BaseModel):
    scraped_at: Optional[datetime] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    listing_id: Optional[int] = None
    platform_id: Optional[int] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None


class ListingDataRead(ListingDataBase):
    id: int

    class Config:
        orm_mode = True
