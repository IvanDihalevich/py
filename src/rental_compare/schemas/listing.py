from pydantic import BaseModel, HttpUrl

class ListingBase(BaseModel):
    external_id: str
    url: HttpUrl
    title: str
    location: str
    platform_id: int

class ListingCreate(ListingBase):
    pass

class ListingUpdate(BaseModel):
    external_id: str | None = None
    url: HttpUrl | None = None
    title: str | None = None
    location: str | None = None
    platform_id: int | None = None

class ListingRead(ListingBase):
    id: int

    class Config:
        orm_mode = True
