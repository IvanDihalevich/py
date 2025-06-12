# src/rental_compare/schemas/platform.py
from pydantic import BaseModel, HttpUrl, validator

class PlatformBase(BaseModel):
    name: str
    search_url_template: HttpUrl

    @validator('name')
    def name_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('name must be a non-empty string')
        return v

class PlatformCreate(PlatformBase):
    pass

class PlatformRead(PlatformBase):
    id: int

    class Config:
        orm_mode = True
