from pydantic import BaseModel, HttpUrl

class PlatformBase(BaseModel):
    name: str
    search_url_template: HttpUrl

class PlatformCreate(PlatformBase):
    pass

class PlatformRead(PlatformBase):
    id: int
    class Config:
        from_attributes = True
