# src/rental_compare/schemas/listing.py
from pydantic import BaseModel, HttpUrl, validator

class ListingBase(BaseModel):
    external_id: str
    url: HttpUrl
    title: str
    location: str
    platform_id: int

    @validator('external_id', 'title', 'location')
    def non_empty_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('must be a non-empty string')
        return v

    @validator('platform_id')
    def platform_id_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('platform_id must be a positive integer')
        return v

class ListingCreate(ListingBase):
    pass

class ListingUpdate(BaseModel):
    external_id: str | None = None
    url: HttpUrl | None = None
    title: str | None = None
    location: str | None = None
    platform_id: int | None = None

    @validator('external_id', 'title', 'location', pre=True, always=True)
    def strip_or_none(cls, v):
        if v is None:
            return None
        if not v.strip():
            raise ValueError('if set, must be a non-empty string')
        return v

    @validator('platform_id')
    def platform_id_optional_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('if set, platform_id must be a positive integer')
        return v

class ListingRead(ListingBase):
    id: int

    class Config:
        orm_mode = True
