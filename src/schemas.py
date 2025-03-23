from pydantic import BaseModel, HttpUrl
from datetime import datetime


class LinkCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = None
    expires_at: datetime | None = None


class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    expires_at: datetime | None
    clicks: int

    class Config:
        from_attributes = True


class LinkStatsResponse(BaseModel):
    original_url: str
    created_at: datetime
    clicks: int
    last_used_at: datetime | None


class LinkStatsResponse(BaseModel):
    original_url: str
    created_at: datetime
    clicks: int
    last_used_at: datetime | None
